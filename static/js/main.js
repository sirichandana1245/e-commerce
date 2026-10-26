/**
 * AURA ATELIER - LUXURY E-COMMERCE CORE SCRIPT
 * Handles Cart, Wishlist, Quick-View, Currency Converter, Live Checkout Card Preview & AJAX APIs
 */

document.addEventListener('DOMContentLoaded', () => {
    initNavbarScroll();
    initWishlist();
    initQuickView();
    initCurrencyConverter();
    initLiveSearch();
    initNewsletter();
});

// ==========================================
// Toast Notification Engine
// ==========================================
function showLuxuryToast(title, message, icon = 'bi-check-circle-fill') {
    let container = document.getElementById('luxuryToastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'luxuryToastContainer';
        container.className = 'toast-container-custom';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'luxury-toast';
    toast.innerHTML = `
        <i class="bi ${icon} fs-4 text-warning"></i>
        <div>
            <div class="fw-bold" style="font-size:0.9rem;">${title}</div>
            <div style="font-size:0.8rem; color:#D3CEC4;">${message}</div>
        </div>
    `;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.transition = 'all 0.35s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(15px)';
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}

// ==========================================
// Navbar Scroll Effect
// ==========================================
function initNavbarScroll() {
    const navbar = document.querySelector('.luxury-navbar');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ==========================================
// Shopping Bag (Cart) Operations
// ==========================================
async function addToCart(productId, quantity = 1, size = null, color = null) {
    // If not provided, fallback to active UI selections or defaults
    if (!size) {
        const activeSizeBtn = document.querySelector('.size-pill-btn.active');
        size = activeSizeBtn ? activeSizeBtn.dataset.size : 'M';
    }
    if (!color) {
        const activeColorBtn = document.querySelector('.color-swatch-btn.active');
        color = activeColorBtn ? activeColorBtn.dataset.color : 'Standard';
    }

    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id: productId,
                quantity: parseInt(quantity, 10),
                size: size,
                color: color
            })
        });

        const data = await response.json();
        if (data.success) {
            updateCartBadges(data.cart_count);
            renderCartDrawer();
            showLuxuryToast("Shopping Bag Updated", data.message, "bi-bag-check-fill");
            
            // Open the cart offcanvas drawer
            const cartDrawerEl = document.getElementById('cartDrawer');
            if (cartDrawerEl && typeof bootstrap !== 'undefined') {
                const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(cartDrawerEl);
                offcanvas.show();
            }
        } else {
            showLuxuryToast("Notice", data.message || "Could not add item.", "bi-exclamation-circle");
        }
    } catch (err) {
        console.error("Add to cart error:", err);
    }
}

async function updateCartItem(itemKey, delta, quantity = null) {
    try {
        const payload = { item_key: itemKey };
        if (quantity !== null) {
            payload.quantity = quantity;
        } else {
            payload.delta = delta;
        }

        const response = await fetch('/api/cart/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (data.success) {
            updateCartBadges(data.cart_count);
            renderCartDrawer();
            // If on cart page, reload or update DOM
            if (window.location.pathname === '/cart') {
                window.location.reload();
            }
        }
    } catch (err) {
        console.error("Cart update error:", err);
    }
}

async function removeCartItem(itemKey) {
    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item_key: itemKey })
        });

        const data = await response.json();
        if (data.success) {
            updateCartBadges(data.cart_count);
            renderCartDrawer();
            showLuxuryToast("Item Removed", "Removed item from your shopping bag.", "bi-trash3");
            if (window.location.pathname === '/cart') {
                window.location.reload();
            }
        }
    } catch (err) {
        console.error("Cart remove error:", err);
    }
}

function updateCartBadges(count) {
    document.querySelectorAll('.cart-badge-count').forEach(el => {
        el.textContent = count;
        el.style.display = count > 0 ? 'flex' : 'none';
    });
}

async function renderCartDrawer() {
    const listEl = document.getElementById('drawerCartItemsList');
    const totalsEl = document.getElementById('drawerCartTotals');
    if (!listEl) return;

    try {
        const response = await fetch('/api/cart');
        const data = await response.json();
        const items = data.items || [];
        const totals = data.totals || {};

        if (items.length === 0) {
            listEl.innerHTML = `
                <div class="text-center py-5">
                    <i class="bi bi-bag-x fs-1 text-muted"></i>
                    <p class="mt-3 text-muted fw-semibold">Your shopping bag is empty.</p>
                    <a href="/shop" class="btn btn-sm btn-luxury-primary mt-2">Discover Collections</a>
                </div>
            `;
            if (totalsEl) totalsEl.style.display = 'none';
            return;
        }

        if (totalsEl) totalsEl.style.display = 'block';

        let html = '';
        items.forEach(item => {
            html += `
                <div class="cart-item-row">
                    <img src="/static/images/${item.image}" alt="${item.name}" class="cart-item-thumb">
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-start">
                            <h6 class="mb-1" style="font-size:0.95rem; font-weight:600;">${item.name}</h6>
                            <button class="btn btn-sm text-muted p-0" onclick="removeCartItem('${item.item_key}')" title="Remove">
                                <i class="bi bi-x-lg"></i>
                            </button>
                        </div>
                        <div class="text-muted mb-2" style="font-size:0.78rem;">
                            Size: <span class="fw-semibold text-dark">${item.size}</span> | Color: <span class="fw-semibold text-dark">${item.color}</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="quantity-stepper" style="transform: scale(0.85); transform-origin: left center;">
                                <button class="quantity-btn" onclick="updateCartItem('${item.item_key}', -1)">-</button>
                                <input type="text" class="quantity-input" value="${item.quantity}" readonly>
                                <button class="quantity-btn" onclick="updateCartItem('${item.item_key}', 1)">+</button>
                            </div>
                            <span class="fw-bold price-val" data-base-price="${item.price * item.quantity}">$${(item.price * item.quantity).toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            `;
        });
        listEl.innerHTML = html;

        // Render progress towards free shipping ($150)
        const subtotal = totals.subtotal || 0;
        const freeShippingThreshold = totals.free_shipping_threshold || 150;
        const progressPct = Math.min(100, Math.round((subtotal / freeShippingThreshold) * 100));
        const shippingMsg = document.getElementById('drawerFreeShippingMsg');
        const progressBar = document.getElementById('drawerFreeShippingBar');
        
        if (shippingMsg && progressBar) {
            progressBar.style.width = `${progressPct}%`;
            if (totals.free_shipping_eligible) {
                shippingMsg.innerHTML = `<i class="bi bi-stars text-warning me-1"></i> <strong>Congratulations!</strong> You qualify for FREE Express Shipping!`;
            } else {
                const diff = (freeShippingThreshold - subtotal).toFixed(2);
                shippingMsg.innerHTML = `Add <span class="fw-bold text-dark">$${diff}</span> more to unlock <strong>FREE Express Shipping</strong>!`;
            }
        }

        // Subtotal & Grand total updates
        const subtotalEl = document.getElementById('drawerSubtotalVal');
        if (subtotalEl) {
            subtotalEl.dataset.basePrice = totals.subtotal;
            subtotalEl.textContent = `$${totals.subtotal.toFixed(2)}`;
        }
        const totalEl = document.getElementById('drawerGrandTotalVal');
        if (totalEl) {
            totalEl.dataset.basePrice = totals.grand_total;
            totalEl.textContent = `$${totals.grand_total.toFixed(2)}`;
        }

        applyCurrentCurrency();

    } catch (err) {
        console.error("Render cart drawer error:", err);
    }
}

// ==========================================
// Promo Code Application
// ==========================================
async function applyCouponCode() {
    const input = document.getElementById('couponInput');
    if (!input || !input.value.trim()) {
        showLuxuryToast("Notice", "Please enter a valid coupon code.", "bi-info-circle");
        return;
    }

    try {
        const response = await fetch('/api/coupon/apply', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: input.value.trim() })
        });

        const data = await response.json();
        if (data.success) {
            showLuxuryToast("Voucher Applied", data.message, "bi-tag-fill");
            renderCartDrawer();
            if (window.location.pathname === '/cart' || window.location.pathname === '/checkout') {
                window.location.reload();
            }
        } else {
            showLuxuryToast("Invalid Code", data.message, "bi-exclamation-triangle-fill");
        }
    } catch (err) {
        console.error("Apply coupon error:", err);
    }
}

// ==========================================
// Wishlist System (LocalStorage)
// ==========================================
function initWishlist() {
    updateWishlistUI();
}

function getWishlist() {
    try {
        return JSON.parse(localStorage.getItem('aura_wishlist') || '[]');
    } catch {
        return [];
    }
}

function toggleWishlist(productId, btnElement = null) {
    let list = getWishlist();
    const id = parseInt(productId, 10);
    const index = list.indexOf(id);

    if (index > -1) {
        list.splice(index, 1);
        showLuxuryToast("Wishlist Updated", "Item removed from your saved list.", "bi-heart");
        if (btnElement) btnElement.classList.remove('active-wishlist');
    } else {
        list.push(id);
        showLuxuryToast("Saved to Wishlist", "Item added to your private favorites.", "bi-heart-fill");
        if (btnElement) btnElement.classList.add('active-wishlist');
    }

    localStorage.setItem('aura_wishlist', JSON.stringify(list));
    updateWishlistUI();
}

function updateWishlistUI() {
    const list = getWishlist();
    document.querySelectorAll('.wishlist-badge-count').forEach(el => {
        el.textContent = list.length;
        el.style.display = list.length > 0 ? 'flex' : 'none';
    });

    document.querySelectorAll('.btn-wishlist-toggle').forEach(btn => {
        const id = parseInt(btn.dataset.productId, 10);
        if (list.includes(id)) {
            btn.classList.add('active-wishlist');
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = 'bi bi-heart-fill text-danger';
            }
        } else {
            btn.classList.remove('active-wishlist');
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = 'bi bi-heart';
            }
        }
    });

    // If on wishlist page, render saved items
    renderWishlistPage();
}

async function renderWishlistPage() {
    const container = document.getElementById('wishlistItemsContainer');
    if (!container) return;

    const list = getWishlist();
    if (list.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-heart fs-1 text-muted"></i>
                <h4 class="mt-3 font-serif">Your Wishlist is Empty</h4>
                <p class="text-muted">Explore our curated collections and save items you adore.</p>
                <a href="/shop" class="btn btn-luxury-primary mt-2">Explore Collections</a>
            </div>
        `;
        return;
    }

    try {
        const response = await fetch('/api/products');
        const allProducts = await response.json();
        const saved = allProducts.filter(p => list.includes(p.id));

        let html = '';
        saved.forEach(p => {
            html += `
                <div class="col-6 col-md-4 col-lg-3 mb-4">
                    <div class="product-card">
                        <div class="product-image-wrapper">
                            <img src="/static/images/${p.image}" alt="${p.name}">
                            <div class="card-floating-actions">
                                <button class="action-round-btn active-wishlist" onclick="toggleWishlist(${p.id})">
                                    <i class="bi bi-heart-fill text-danger"></i>
                                </button>
                            </div>
                        </div>
                        <div class="product-content">
                            <div class="product-category-text">${p.category}</div>
                            <h3 class="product-title">${p.name}</h3>
                            <div class="product-price-row">
                                <span class="price-current price-val" data-base-price="${p.price}">$${p.price.toFixed(2)}</span>
                            </div>
                            <button class="btn btn-sm btn-luxury-primary mt-3 w-100" onclick="addToCart(${p.id}, 1)">
                                <i class="bi bi-bag-plus me-1"></i> Move to Bag
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
        applyCurrentCurrency();
    } catch (err) {
        console.error("Wishlist render error:", err);
    }
}

// ==========================================
// Quick View Modal
// ==========================================
async function initQuickView() {
    document.querySelectorAll('.btn-quick-view').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.preventDefault();
            const id = btn.dataset.productId;
            openQuickViewModal(id);
        });
    });
}

async function openQuickViewModal(productId) {
    try {
        const response = await fetch('/api/products');
        const products = await response.json();
        const product = products.find(p => p.id == productId);
        if (!product) return;

        const modalEl = document.getElementById('quickViewModal');
        if (!modalEl) return;

        document.getElementById('qvImage').src = `/static/images/${product.image}`;
        document.getElementById('qvCategory').textContent = product.category;
        document.getElementById('qvTitle').textContent = product.name;
        document.getElementById('qvPrice').textContent = `$${product.price.toFixed(2)}`;
        document.getElementById('qvPrice').dataset.basePrice = product.price;
        document.getElementById('qvDesc').textContent = product.short_desc;
        document.getElementById('qvFabric').textContent = product.fabric;

        // Size pills
        const sizeContainer = document.getElementById('qvSizes');
        if (sizeContainer) {
            sizeContainer.innerHTML = product.sizes.map((s, idx) => `
                <button type="button" class="size-pill-btn ${idx === 0 ? 'active' : ''}" data-size="${s}" onclick="selectQvSize(this)">${s}</button>
            `).join('');
        }

        // Color swatches
        const colorContainer = document.getElementById('qvColors');
        if (colorContainer) {
            colorContainer.innerHTML = product.colors.map((c, idx) => `
                <button type="button" class="color-swatch-btn ${idx === 0 ? 'active' : ''}" style="background-color: ${c.hex};" data-color="${c.name}" title="${c.name}" onclick="selectQvColor(this)"></button>
            `).join('');
        }

        // Add to bag button setup
        const addBtn = document.getElementById('qvAddToCartBtn');
        if (addBtn) {
            addBtn.onclick = () => {
                const qty = parseInt(document.getElementById('qvQuantity').value || 1, 10);
                const activeSize = document.querySelector('#qvSizes .size-pill-btn.active')?.dataset.size || product.sizes[0];
                const activeColor = document.querySelector('#qvColors .color-swatch-btn.active')?.dataset.color || product.colors[0].name;
                addToCart(product.id, qty, activeSize, activeColor);
                bootstrap.Modal.getInstance(modalEl).hide();
            };
        }

        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
        applyCurrentCurrency();

    } catch (err) {
        console.error("Quick view error:", err);
    }
}

function selectQvSize(btn) {
    document.querySelectorAll('#qvSizes .size-pill-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

function selectQvColor(btn) {
    document.querySelectorAll('#qvColors .color-swatch-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

// ==========================================
// Currency Converter ($ USD, € EUR, £ GBP, ₹ INR)
// ==========================================
const CURRENCY_RATES = {
    'USD': { symbol: '$', rate: 1.0 },
    'EUR': { symbol: '€', rate: 0.92 },
    'GBP': { symbol: '£', rate: 0.79 },
    'INR': { symbol: '₹', rate: 84.5 }
};

function initCurrencyConverter() {
    const selector = document.getElementById('currencySelector');
    if (!selector) return;

    const saved = localStorage.getItem('aura_currency') || 'USD';
    selector.value = saved;

    selector.addEventListener('change', (e) => {
        const code = e.target.value;
        localStorage.setItem('aura_currency', code);
        applyCurrentCurrency();
        showLuxuryToast("Currency Changed", `Prices converted to ${code}`, "bi-currency-exchange");
    });

    applyCurrentCurrency();
}

function applyCurrentCurrency() {
    const code = localStorage.getItem('aura_currency') || 'USD';
    const config = CURRENCY_RATES[code] || CURRENCY_RATES['USD'];

    document.querySelectorAll('.price-val').forEach(el => {
        const base = parseFloat(el.dataset.basePrice);
        if (!isNaN(base)) {
            const converted = (base * config.rate).toFixed(2);
            el.textContent = `${config.symbol}${converted}`;
        }
    });
}

// ==========================================
// Live Search & Autocomplete
// ==========================================
function initLiveSearch() {
    const input = document.getElementById('headerSearchInput');
    const resultsBox = document.getElementById('headerSearchResults');
    if (!input || !resultsBox) return;

    let timeout;
    input.addEventListener('input', () => {
        clearTimeout(timeout);
        const query = input.value.trim();
        if (query.length < 2) {
            resultsBox.style.display = 'none';
            return;
        }

        timeout = setTimeout(async () => {
            try {
                const res = await fetch(`/api/products?q=${encodeURIComponent(query)}`);
                const items = await res.json();

                if (items.length === 0) {
                    resultsBox.innerHTML = `<div class="p-3 text-muted text-center" style="font-size:0.85rem;">No items found for "${query}"</div>`;
                } else {
                    resultsBox.innerHTML = items.slice(0, 5).map(p => `
                        <a href="/product/${p.id}" class="d-flex align-items-center gap-3 p-2 text-decoration-none border-bottom text-dark hover-gold">
                            <img src="/static/images/${p.image}" style="width:42px; height:50px; object-fit:cover; border-radius:4px;">
                            <div>
                                <div class="fw-semibold" style="font-size:0.88rem;">${p.name}</div>
                                <div class="text-gold fw-bold" style="font-size:0.82rem;">$${p.price.toFixed(2)}</div>
                            </div>
                        </a>
                    `).join('') + `
                        <div class="p-2 text-center bg-light">
                            <a href="/shop?q=${encodeURIComponent(query)}" class="small text-dark fw-bold text-uppercase">View all matches (${items.length})</a>
                        </div>
                    `;
                }
                resultsBox.style.display = 'block';
            } catch (err) {
                console.error("Search error:", err);
            }
        }, 250);
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !resultsBox.contains(e.target)) {
            resultsBox.style.display = 'none';
        }
    });
}

// ==========================================
// Newsletter Subscription
// ==========================================
function initNewsletter() {
    const form = document.getElementById('newsletterForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const input = document.getElementById('newsletterEmail');
        const email = input.value.trim();

        try {
            const res = await fetch('/api/newsletter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });
            const data = await res.json();
            if (data.success) {
                showLuxuryToast("Welcome to AURA Atelier", data.message, "bi-envelope-check-fill");
                input.value = '';
            } else {
                showLuxuryToast("Notice", data.message, "bi-exclamation-circle");
            }
        } catch (err) {
            console.error("Newsletter error:", err);
        }
    });
}

// ==========================================
// Interactive Checkout Live Card Preview
// ==========================================
function initCheckoutCardPreview() {
    const numberInput = document.getElementById('cardNumberInput');
    const nameInput = document.getElementById('cardNameInput');
    const expiryInput = document.getElementById('cardExpiryInput');
    const cvvInput = document.getElementById('cardCvvInput');

    const displayNum = document.getElementById('previewCardNumber');
    const displayName = document.getElementById('previewCardName');
    const displayExpiry = document.getElementById('previewCardExpiry');

    if (numberInput && displayNum) {
        numberInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 16);
            let formatted = val.match(/.{1,4}/g)?.join(' ') || '•••• •••• •••• ••••';
            displayNum.textContent = formatted;
        });
    }

    if (nameInput && displayName) {
        nameInput.addEventListener('input', (e) => {
            displayName.textContent = e.target.value.trim().toUpperCase() || 'YOUR NAME';
        });
    }

    if (expiryInput && displayExpiry) {
        expiryInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 4);
            if (val.length >= 2) {
                val = val.substring(0, 2) + '/' + val.substring(2);
            }
            displayExpiry.textContent = val || 'MM/YY';
        });
    }
}

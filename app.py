import os
import uuid
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from products_data import PRODUCTS, CATEGORIES, PROMO_CODES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aura_atelier_luxury_ecommerce_secret_key_2026'

# In-memory orders store (persisted during server lifetime)
ORDERS = {}

# In-memory reviews store to allow live customer reviews
PRODUCT_REVIEWS = {p['id']: list(p.get('reviews', [])) for p in PRODUCTS}


def get_cart():
    """Retrieve or initialize shopping cart in user session."""
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']


def calculate_cart_totals(cart, promo_code=None):
    """Compute subtotal, discounts, shipping, tax, and grand total."""
    subtotal = 0.0
    total_quantity = 0

    for item in cart:
        subtotal += item['price'] * item['quantity']
        total_quantity += item['quantity']

    discount_amount = 0.0
    discount_label = ""
    free_shipping = False

    if promo_code and promo_code.upper() in PROMO_CODES:
        promo = PROMO_CODES[promo_code.upper()]
        if promo.get('discount_percent', 0) > 0:
            discount_amount = round(subtotal * (promo['discount_percent'] / 100.0), 2)
            discount_label = f"{promo['discount_percent']}% Off ({promo_code.upper()})"
        if promo.get('free_shipping', False):
            free_shipping = True
            discount_label = "Free Express Shipping"

    # Free shipping on orders over $150 or if promo qualifies
    standard_shipping = 15.0 if subtotal > 0 else 0.0
    if subtotal >= 150.0 or free_shipping:
        shipping_cost = 0.0
    else:
        shipping_cost = standard_shipping

    # Estimated tax: 8.5%
    taxable_amount = max(0.0, subtotal - discount_amount)
    estimated_tax = round(taxable_amount * 0.085, 2) if subtotal > 0 else 0.0

    grand_total = round(taxable_amount + shipping_cost + estimated_tax, 2)

    return {
        'subtotal': round(subtotal, 2),
        'total_quantity': total_quantity,
        'discount_amount': round(discount_amount, 2),
        'discount_label': discount_label,
        'shipping_cost': round(shipping_cost, 2),
        'free_shipping_eligible': subtotal >= 150.0 or free_shipping,
        'free_shipping_threshold': 150.0,
        'amount_to_free_shipping': max(0.0, round(150.0 - subtotal, 2)),
        'estimated_tax': estimated_tax,
        'grand_total': grand_total,
        'applied_coupon': promo_code.upper() if promo_code else None
    }


@app.context_processor
def inject_global_data():
    """Make categories, cart count, and currency helper available to all templates."""
    cart = get_cart()
    cart_count = sum(item['quantity'] for item in cart)
    applied_coupon = session.get('promo_code', None)
    cart_totals = calculate_cart_totals(cart, applied_coupon)
    return {
        'categories': CATEGORIES,
        'cart_count': cart_count,
        'cart_items': cart,
        'cart_totals': cart_totals,
        'current_year': datetime.datetime.now().year
    }


# ==========================================
# PAGE ROUTES
# ==========================================

@app.route('/')
def index():
    """Homepage: Hero section, curated collections, featured products."""
    featured_products = PRODUCTS[:4]
    bestsellers = [p for p in PRODUCTS if p.get('badge') == 'Bestseller']
    trending = [p for p in PRODUCTS if p.get('badge') in ['Trending', 'Top Rated', 'Limited Edition']]
    return render_template('index.html',
                           featured_products=featured_products,
                           bestsellers=bestsellers,
                           trending=trending,
                           products=PRODUCTS)


@app.route('/shop')
def shop():
    """Catalog page with filters, search, and sorting."""
    category = request.args.get('category', 'all')
    search_query = request.args.get('q', '').strip().lower()
    sort_by = request.args.get('sort', 'featured')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 500))

    filtered = []
    for p in PRODUCTS:
        # Category filter
        if category != 'all':
            cat_match = False
            if category.lower() in p['category'].lower():
                cat_match = True
            elif category == 'dresses' and 'dress' in p['category'].lower():
                cat_match = True
            elif category == 'knitwear' and 'knitwear' in p['category'].lower():
                cat_match = True
            elif category == 'tops' and 'tops' in p['category'].lower():
                cat_match = True
            elif category == 'accessories' and ('accessories' in p['category'].lower() or 'shoes' in p['category'].lower()):
                cat_match = True
            elif category == 'new-season' and 'season' in p['category'].lower():
                cat_match = True
            if not cat_match:
                continue

        # Search filter
        if search_query:
            searchable = (p['name'] + ' ' + p['short_desc'] + ' ' + p['category'] + ' ' + ' '.join(p.get('tags', []))).lower()
            if search_query not in searchable:
                continue

        # Price filter
        if not (min_price <= p['price'] <= max_price):
            continue

        filtered.append(p)

    # Sorting
    if sort_by == 'price-low':
        filtered.sort(key=lambda x: x['price'])
    elif sort_by == 'price-high':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_by == 'name':
        filtered.sort(key=lambda x: x['name'])
    # default is 'featured' order

    return render_template('shop.html',
                           products=filtered,
                           current_category=category,
                           search_query=search_query,
                           sort_by=sort_by,
                           min_price=min_price,
                           max_price=max_price,
                           total_found=len(filtered))


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product showcase page."""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        flash("Product not found.", "warning")
        return redirect(url_for('shop'))

    # Retrieve live reviews
    reviews = PRODUCT_REVIEWS.get(product_id, product.get('reviews', []))
    
    # Related products
    related = [p for p in PRODUCTS if p['id'] != product_id and (p['category'] == product['category'] or any(t in product.get('tags', []) for t in p.get('tags', [])))][:3]
    if len(related) < 3:
        related = [p for p in PRODUCTS if p['id'] != product_id][:3]

    return render_template('product.html',
                           product=product,
                           reviews=reviews,
                           related_products=related)


@app.route('/cart')
def cart_page():
    """Dedicated Cart and Order calculation view."""
    cart = get_cart()
    promo_code = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo_code)
    return render_template('cart.html', cart=cart, totals=totals)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    """Checkout flow with payment mockup and instant validation."""
    cart = get_cart()
    if not cart:
        flash("Your shopping bag is empty. Please select an item to continue.", "info")
        return redirect(url_for('shop'))

    promo_code = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo_code)

    if request.method == 'POST':
        # Process order submission
        first_name = request.form.get('firstName', '').strip()
        last_name = request.form.get('lastName', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        city = request.form.get('city', '').strip()
        postal = request.form.get('postalCode', '').strip()
        payment_method = request.form.get('paymentMethod', 'credit-card')

        order_id = f"AUR-{uuid.uuid4().hex[:8].upper()}"
        order_date = datetime.datetime.now().strftime("%B %d, %Y - %I:%M %p")

        order_record = {
            'order_id': order_id,
            'date': order_date,
            'customer': {
                'name': f"{first_name} {last_name}",
                'email': email,
                'address': f"{address}, {city} - {postal}"
            },
            'items': list(cart),
            'order_items': list(cart),
            'totals': totals,
            'payment_method': payment_method.replace('-', ' ').title(),
            'status': 'Confirmed & Preparing for Dispatch',
            'estimated_delivery': (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%A, %B %d, %Y")
        }

        ORDERS[order_id] = order_record

        # Clear cart and session coupon
        session['cart'] = []
        session.pop('promo_code', None)
        session.modified = True

        return redirect(url_for('order_confirmation', order_id=order_id))

    return render_template('checkout.html', cart=cart, totals=totals)


@app.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    """Receipt and tracking summary."""
    order = ORDERS.get(order_id)
    if not order:
        flash("Order not found or session has expired.", "warning")
        return redirect(url_for('index'))
    return render_template('order_confirmation.html', order=order)


@app.route('/orders')
def orders_view():
    """Order tracking and lookup."""
    order_id = request.args.get('order_id', '').strip()
    order = ORDERS.get(order_id) if order_id else None
    return render_template('orders.html', order=order, searched_id=order_id, all_orders=list(ORDERS.values())[::-1])


@app.route('/wishlist')
def wishlist():
    """Wishlist page."""
    return render_template('wishlist.html')


@app.route('/about')
def about():
    """Brand ethos, sustainability, and atelier story."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Customer concierge and contact inquiry form."""
    success = False
    if request.method == 'POST':
        success = True
        flash("Thank you for reaching out! Our atelier concierge will respond within 24 hours.", "success")
    return render_template('contact.html', success=success)


# ==========================================
# REST API ENDPOINTS (AJAX / Real-time)
# ==========================================

@app.route('/api/products')
def api_products():
    """Return JSON list of products with optional query filtering."""
    q = request.args.get('q', '').lower()
    cat = request.args.get('category', 'all')
    res = PRODUCTS
    if cat != 'all':
        res = [p for p in res if cat in p['category'].lower()]
    if q:
        res = [p for p in res if q in p['name'].lower() or q in p['short_desc'].lower()]
    return jsonify(res)


@app.route('/api/cart', methods=['GET'])
def api_get_cart():
    """Return JSON payload of current cart and totals."""
    cart = get_cart()
    promo = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo)
    return jsonify({
        'items': cart,
        'totals': totals
    })


@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    """Add an item with specific size and color to cart."""
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    quantity = int(data.get('quantity', 1))
    size = data.get('size', 'M')
    color = data.get('color', 'Standard')

    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404

    cart = get_cart()

    # Look for existing item with matching id, size, and color
    item_key = f"{product_id}_{size}_{color}"
    found = False
    for item in cart:
        if item.get('item_key') == item_key:
            item['quantity'] += quantity
            found = True
            break

    if not found:
        cart.append({
            'item_key': item_key,
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'original_price': product.get('original_price', product['price']),
            'image': product['image'],
            'size': size,
            'color': color,
            'quantity': quantity
        })

    session['cart'] = cart
    session.modified = True

    promo = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo)

    return jsonify({
        'success': True,
        'message': f"Added '{product['name']}' to your shopping bag.",
        'cart_count': sum(i['quantity'] for i in cart),
        'totals': totals
    })


@app.route('/api/cart/update', methods=['POST'])
def api_update_cart():
    """Update quantity for a cart item."""
    data = request.get_json() or {}
    item_key = data.get('item_key')
    delta = int(data.get('delta', 0))
    set_quantity = data.get('quantity')

    cart = get_cart()
    for item in cart:
        if item.get('item_key') == item_key:
            if set_quantity is not None:
                item['quantity'] = max(1, int(set_quantity))
            else:
                item['quantity'] = max(1, item['quantity'] + delta)
            break

    session['cart'] = cart
    session.modified = True

    promo = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo)

    return jsonify({
        'success': True,
        'cart': cart,
        'cart_count': sum(i['quantity'] for i in cart),
        'totals': totals
    })


@app.route('/api/cart/remove', methods=['POST'])
def api_remove_from_cart():
    """Remove item from cart."""
    data = request.get_json() or {}
    item_key = data.get('item_key')

    cart = get_cart()
    cart = [item for item in cart if item.get('item_key') != item_key]
    session['cart'] = cart
    session.modified = True

    promo = session.get('promo_code', None)
    totals = calculate_cart_totals(cart, promo)

    return jsonify({
        'success': True,
        'cart': cart,
        'cart_count': sum(i['quantity'] for i in cart),
        'totals': totals
    })


@app.route('/api/cart/clear', methods=['POST'])
def api_clear_cart():
    """Empty the cart."""
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True, 'cart_count': 0})


@app.route('/api/coupon/apply', methods=['POST'])
def api_apply_coupon():
    """Apply discount voucher."""
    data = request.get_json() or {}
    code = data.get('code', '').strip().upper()

    if not code:
        return jsonify({'success': False, 'message': 'Please provide a valid code.'}), 400

    if code in PROMO_CODES:
        session['promo_code'] = code
        session.modified = True
        cart = get_cart()
        totals = calculate_cart_totals(cart, code)
        promo_info = PROMO_CODES[code]
        return jsonify({
            'success': True,
            'message': f"Coupon '{code}' applied: {promo_info['description']}!",
            'totals': totals
        })
    else:
        return jsonify({
            'success': False,
            'message': f"Coupon '{code}' is invalid or expired. Try 'AURA10', 'WELCOME20', or 'FREESHIP'."
        }), 400


@app.route('/api/coupon/remove', methods=['POST'])
def api_remove_coupon():
    """Remove active coupon."""
    session.pop('promo_code', None)
    session.modified = True
    cart = get_cart()
    totals = calculate_cart_totals(cart, None)
    return jsonify({
        'success': True,
        'message': 'Coupon removed.',
        'totals': totals
    })


@app.route('/api/reviews/add', methods=['POST'])
def api_add_review():
    """Add a customer review."""
    data = request.get_json() or {}
    product_id = int(data.get('product_id', 0))
    author = data.get('author', 'Anonymous').strip()
    comment = data.get('comment', '').strip()
    rating = float(data.get('rating', 5))

    if not comment:
        return jsonify({'success': False, 'message': 'Review text is required.'}), 400

    new_review = {
        'author': author if author else 'Verified Client',
        'rating': rating,
        'date': 'Just now',
        'comment': comment
    }

    if product_id not in PRODUCT_REVIEWS:
        PRODUCT_REVIEWS[product_id] = []
    PRODUCT_REVIEWS[product_id].insert(0, new_review)

    return jsonify({
        'success': True,
        'review': new_review,
        'total_reviews': len(PRODUCT_REVIEWS[product_id])
    })


@app.route('/api/newsletter', methods=['POST'])
def api_newsletter():
    """Handle newsletter subscription."""
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    if not email or '@' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400
    return jsonify({
        'success': True,
        'message': 'Thank you! You are now subscribed to the AURA Atelier Private Journal. Enjoy 20% off with code WELCOME20.'
    })


if __name__ == '__main__':
    print("Starting AURA Atelier E-Commerce Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

"""
Product catalog and static store data for the AURA Atelier E-Commerce Platform.
"""

PRODUCTS = [
    {
        "id": 1,
        "name": "Flora Cascade Wrap Midi Dress",
        "category": "Dresses",
        "tagline": "Ethereal pastel silhouette with romantic flutter accents",
        "price": 128.00,
        "original_price": 160.00,
        "on_sale": True,
        "discount_percent": 20,
        "rating": 4.9,
        "review_count": 142,
        "image": "pexels-ron-lach-8386652.jpg",
        "badge": "Bestseller",
        "stock": 7,
        "short_desc": "Delicate blush pink wrap dress woven from featherlight organic cotton muslin, adorned with golden wildflower embroidery and a tailored sash tie.",
        "description": "Inspired by Mediterranean botanicals, the Flora Cascade Wrap Midi Dress blends effortless vacation elegance with mindful artisan craftsmanship. Featuring tiered butterfly flutter sleeves, a flattering crossover V-neckline, and an adjustable cinched waist, it transitions seamlessly from sun-drenched daytime garden strolls to intimate evening cocktail gatherings.",
        "fabric": "100% GOTS Certified Organic Cotton Voile",
        "care": "Gentle hand wash cold or eco dry clean. Line dry in shade.",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": [
            {"name": "Blush Blossom", "hex": "#F3C5C5"},
            {"name": "Ivory Jasmine", "hex": "#FDFBF7"},
            {"name": "Sky Lavender", "hex": "#C9C3E3"}
        ],
        "tags": ["bestseller", "dress", "floral", "summer", "sustainable"],
        "reviews": [
            {"author": "Elena Rostova", "rating": 5, "date": "2 days ago", "comment": "The fabric drape is pure perfection! Received endless compliments at a garden wedding."},
            {"author": "Camille Dupont", "rating": 5, "date": "1 week ago", "comment": "Breathable, lightweight, and the waist wrap cinches exactly where you want it to."},
            {"author": "Maya Patel", "rating": 4.8, "date": "2 weeks ago", "comment": "Incredible tailoring. The inner lining ensures complete opacity."}
        ]
    },
    {
        "id": 2,
        "name": "Rosewater Fine-Gauge Ribbed Twinset",
        "category": "Knitwear",
        "tagline": "Ultra-soft cashmere-infused knit cardigan & sweetheart top",
        "price": 115.00,
        "original_price": 140.00,
        "on_sale": True,
        "discount_percent": 18,
        "rating": 4.8,
        "review_count": 89,
        "image": "pexels-ron-lach-8386642.jpg",
        "badge": "Trending",
        "stock": 12,
        "short_desc": "Twin knit harmony: a ribbed sweetheart-neck camisole paired with an oversized boyfriend cardigan finished with faux-mother-of-pearl buttons.",
        "description": "Spun from ethically sourced merino wool and modal cashmere, this two-piece set epitomizes relaxed Parisian chic. The sweetheart neckline frames the collarbone delicately, while the ribbed texture stretches comfortably to flatter every silhouette. Wear together as an ensemble or styled separately with high-rise denim.",
        "fabric": "70% Fine Merino Wool, 20% Modal, 10% Cashmere",
        "care": "Hand wash in cool water with wool shampoo. Dry flat on towel.",
        "sizes": ["XS", "S", "M", "L"],
        "colors": [
            {"name": "Pastel Rose", "hex": "#ECAAB1"},
            {"name": "Oatmeal Heather", "hex": "#E6DBC9"},
            {"name": "Midnight Slate", "hex": "#30323D"}
        ],
        "tags": ["trending", "knitwear", "sweater", "cardigan", "luxury"],
        "reviews": [
            {"author": "Sophia Laurent", "rating": 5, "date": "3 days ago", "comment": "Softest knit I own! It feels like a gentle cloud against sensitive skin."},
            {"author": "Aaliyah Brooks", "rating": 4.5, "date": "2 weeks ago", "comment": "Rich tone and doesn't pill after washing. True to size."}
        ]
    },
    {
        "id": 3,
        "name": "Atelier 3D Petal Sweatshirt & Bag Set",
        "category": "Knitwear",
        "tagline": "Sculptural textured pullover styled with blush leather baguette",
        "price": 145.00,
        "original_price": 185.00,
        "on_sale": True,
        "discount_percent": 22,
        "rating": 5.0,
        "review_count": 64,
        "image": "pexels-anastasia-shuraeva-5705478.jpg",
        "badge": "Limited Edition",
        "stock": 4,
        "short_desc": "Artisan statement sweater adorned with hand-cut organza flower petals, complemented by our architectural vegan-leather crossbody shoulder bag.",
        "description": "A true couture collectible from our capsule collection. Each organza petal is cut, hand-curled, and secured onto a cozy cotton-blend knit sweater to create tactile dimension and captivating movement. Pairs seamlessly with the minimalist structured blush leather pouch bag.",
        "fabric": "85% Combed French Terry Cotton, 15% Silk Organza accents",
        "care": "Professional dry clean only. Protect embellishments when storing.",
        "sizes": ["S", "M", "L"],
        "colors": [
            {"name": "Dusty Petal & Nude", "hex": "#E3BBB1"},
            {"name": "Pearl Marshmallow", "hex": "#F7F5F0"}
        ],
        "tags": ["limited", "couture", "sweater", "bag", "luxury"],
        "reviews": [
            {"author": "Chloe Van Der Bilt", "rating": 5, "date": "Yesterday", "comment": "Unbelievable attention to detail. This belongs in a high-fashion runway showcase."},
            {"author": "Hanna Lindqvist", "rating": 5, "date": "1 week ago", "comment": "The bag and sweater pairing is stunning. Super fast shipping too."}
        ]
    },
    {
        "id": 4,
        "name": "Monochrome Artisan Linen Capsule",
        "category": "Tops & Blouses",
        "tagline": "Hand-loomed pre-washed European linen tops & shirts",
        "price": 89.00,
        "original_price": 89.00,
        "on_sale": False,
        "discount_percent": 0,
        "rating": 4.7,
        "review_count": 118,
        "image": "pexels-cristian-rojas-8030173.jpg",
        "badge": "Eco-Choice",
        "stock": 19,
        "short_desc": "Breathable, airy linen shirts with relaxed balloon sleeves, mother-of-pearl buttons, and raw rustic hems for timeless minimalist daily wear.",
        "description": "Crafted exclusively from certified Normandy flax, our Artisan Linen Capsule tops keep you cool in high summer and layer effortlessly during crisp autumn mornings. Pre-washed with natural pumice stones to achieve an exquisite vintage softness from the very first wear.",
        "fabric": "100% Pure Normandy Flax Linen",
        "care": "Machine wash delicate cycle in cold water. Iron slightly damp or embrace natural crinkles.",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": [
            {"name": "Crisp Chalk", "hex": "#FFFFFF"},
            {"name": "Raven Obsidian", "hex": "#1C1C1E"},
            {"name": "Tuscan Terracotta", "hex": "#A7493A"},
            {"name": "Sage Moss", "hex": "#879B7F"}
        ],
        "tags": ["linen", "tops", "blouse", "minimalist", "eco"],
        "reviews": [
            {"author": "Isla MacLeod", "rating": 5, "date": "5 days ago", "comment": "The fabric quality is superior to designer linen shirts twice the price."},
            {"author": "Zoe Chen", "rating": 4.5, "date": "3 weeks ago", "comment": "Perfect relaxed fit, drape is lovely and doesn't itch."}
        ]
    },
    {
        "id": 5,
        "name": "Serene Tiered Ruffle Linen Midi Dress",
        "category": "Dresses",
        "tagline": "Timeless ruffled flutter-sleeve tiered dress in heavy linen",
        "price": 139.00,
        "original_price": 175.00,
        "on_sale": True,
        "discount_percent": 21,
        "rating": 4.9,
        "review_count": 175,
        "image": "pexels-cristian-rojas-8030176.jpg",
        "badge": "Top Rated",
        "stock": 5,
        "short_desc": "Sculpted tiered midi dress featuring cascading fluted ruffles, deep on-seam pockets, and an adjustable back keyhole tie.",
        "description": "The quintessential summer classic. Cut with generous movement in medium-weight pure linen, the Serene Dress features dramatic flounce sleeves and tiered gathered panels that sway gracefully as you walk. Discreet hidden pockets make it as functional as it is breathtaking.",
        "fabric": "100% High-Density European Linen",
        "care": "Machine wash cold inside laundry pouch. Hang dry.",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": [
            {"name": "Alabaster White", "hex": "#F8F6F0"},
            {"name": "Onyx Black", "hex": "#1B1B1B"},
            {"name": "Rust Sienna", "hex": "#9E4738"}
        ],
        "tags": ["dresses", "linen", "top-rated", "midi", "pockets"],
        "reviews": [
            {"author": "Claire Beaumont", "rating": 5, "date": "4 days ago", "comment": "Best dress I bought this year! Deep pockets, gorgeous linen weight, and flattering fit."},
            {"author": "Tasha Williams", "rating": 5, "date": "10 days ago", "comment": "Looks like an Italian resort piece. High-quality construction."}
        ]
    },
    {
        "id": 6,
        "name": "Riviera Minimalist Resort Ensemble",
        "category": "Accessories & Shoes",
        "tagline": "Tailored beige blazer, silk slip skirt, strappy mules & clutch",
        "price": 165.00,
        "original_price": 210.00,
        "on_sale": True,
        "discount_percent": 21,
        "rating": 4.8,
        "review_count": 73,
        "image": "pexels-pnw-prod-9218397.jpg",
        "badge": "Curated Look",
        "stock": 8,
        "short_desc": "The complete vacation styling: structured lightweight linen blazer, floral bias skirt, and buttery Italian-crafted strappy leather kitten mules.",
        "description": "Curated by our head stylist, the Riviera Ensemble brings together capsule essentials for warm-weather getaways and urban soirées. Includes the tailored notched-lapel linen blazer, a vibrant silk poppy slip skirt, accompanied by artisan leather wrap-around kitten sandals.",
        "fabric": "Fine Silk Twill & European Linen Blend",
        "care": "Specialist dry cleaning advised.",
        "sizes": ["S", "M", "L"],
        "colors": [
            {"name": "Warm Sand & Coral", "hex": "#E3CEB3"},
            {"name": "Monochrome Chic", "hex": "#2B2B2B"}
        ],
        "tags": ["look", "resort", "blazer", "shoes", "luxury"],
        "reviews": [
            {"author": "Valerie Moreau", "rating": 5, "date": "6 days ago", "comment": "The whole outfit harmonizes so seamlessly. Incredible value for a head-to-toe look!"},
            {"author": "Giselle Gomez", "rating": 4.7, "date": "2 weeks ago", "comment": "The strappy mules are surprisingly comfortable for all-day wear."}
        ]
    },
    {
        "id": 7,
        "name": "Botanical Studio Pastel Showcase Collection",
        "category": "New Season",
        "tagline": "Curated palette of periwinkle, sky lilac, and broderie lace",
        "price": 120.00,
        "original_price": 150.00,
        "on_sale": True,
        "discount_percent": 20,
        "rating": 4.9,
        "review_count": 92,
        "image": "pexels-ron-lach-8386648.jpg",
        "badge": "New Season",
        "stock": 11,
        "short_desc": "Seasonal boutique capsule featuring lavender lounge knits, celestial blue oversized tees, and English broderie anglaise tiered sun dress.",
        "description": "Celebrate spring renewal with our fresh Botanical Studio Collection. Soft organic pigments produce gentle pastel blues and lilacs reminiscent of blooming wisteria. Made for relaxed resort lounging, café mornings, and effortless weekend travel.",
        "fabric": "Organic Combed Cotton & Sustainable Lyocell",
        "care": "Machine wash delicate cold. Tumble dry low or air dry.",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colors": [
            {"name": "Wisteria Lilac", "hex": "#C5B9DF"},
            {"name": "Sky Periwinkle", "hex": "#8FA9DF"},
            {"name": "Meadow White", "hex": "#FAFAFA"}
        ],
        "tags": ["new", "pastel", "collection", "cotton", "bestseller"],
        "reviews": [
            {"author": "Annika Soren", "rating": 5, "date": "1 day ago", "comment": "The colors in person are even more luminous than the photos. A true breath of fresh air."},
            {"author": "Lucia Fernandez", "rating": 5, "date": "1 week ago", "comment": "Beautiful tailoring and heavenly soft fabrics."}
        ]
    }
]

CATEGORIES = [
    {"slug": "all", "name": "All Collections", "icon": "bi-grid-fill"},
    {"slug": "dresses", "name": "Dresses & Gowns", "icon": "bi-handbag"},
    {"slug": "knitwear", "name": "Knitwear & Sweaters", "icon": "bi-heart"},
    {"slug": "tops", "name": "Tops & Blouses", "icon": "bi-columns"},
    {"slug": "accessories", "name": "Accessories & Shoes", "icon": "bi-gem"},
    {"slug": "new-season", "name": "New Season", "icon": "bi-stars"}
]

PROMO_CODES = {
    "AURA10": {"discount_percent": 10, "description": "10% Off Entire Order"},
    "WELCOME20": {"discount_percent": 20, "description": "20% Welcome Discount"},
    "LUXE15": {"discount_percent": 15, "description": "15% Exclusive Atelier Member Discount"},
    "FREESHIP": {"discount_percent": 0, "free_shipping": True, "description": "Complimentary Worldwide Express Shipping"}
}

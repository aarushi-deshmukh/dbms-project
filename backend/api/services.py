import uuid
import logging
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from .models import Buyer, Seller, Product, Cart, CartItem, Wishlist, ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

logger = logging.getLogger('api')


# ── Auth ──────────────────────────────────────────────────────────────────────

def authenticate_user(email, password, account_type):
    user = get_object_or_404(User, email=email)
    if not check_password(password, user.password):
        raise ValueError('invalid_password')

    if account_type == 'Buyer' and not Buyer.objects.filter(user=user).exists():
        raise ValueError('buyer_not_found')

    if account_type == 'Seller' and not Seller.objects.filter(user=user).exists():
        raise ValueError('seller_not_found')

    return user


# ── Account creation ──────────────────────────────────────────────────────────

def create_buyer_account(validated_data):
    user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
    )
    Buyer.objects.create(
        user=user,
        age=validated_data['age'],
        phone_number=validated_data['phone_number'],
        address=validated_data['address'],
        city=validated_data['city'],
        country=validated_data['country'],
        pincode=validated_data['pincode'],
    )
    return user


def create_seller_account(validated_data):
    user = User.objects.create_user(
        username=validated_data['email'],
        email=validated_data['email'],
        password=validated_data['password'],
    )
    Seller.objects.create(
        user=user,
        company_name=validated_data['company_name'],
        contact_number=validated_data['contact_number'],
        address=validated_data['address'],
        city=validated_data['city'],
        country=validated_data['country'],
        pincode=validated_data['pincode'],
    )
    return user


# ── Products ──────────────────────────────────────────────────────────────────

def list_products():
    return Product.objects.all()


def get_product_detail(product_id):
    return get_object_or_404(Product, id=product_id)


def delete_seller_product(user, product_id):
    """
    Core product deletion logic. Validates seller ownership by product ID.
    This is the primary implementation used by DELETE /api/products/<id>/.
    The legacy endpoint resolves name/brand → ID and delegates here.
    """
    seller = get_object_or_404(Seller, user=user)
    product = get_object_or_404(Product, id=product_id)

    if product.seller_id != seller.id:
        raise PermissionDenied('You do not own this product.')

    product_name = product.name
    product.delete()
    logger.info('Seller %s deleted product "%s" (id=%s)', seller.company_name, product_name, product_id)
    return True


def resolve_and_delete_product_by_name_brand(user, name, brand):
    """
    Legacy compatibility shim for DELETE /api/remove-product/<name>/<brand>/.
    Resolves the product to a unique DB ID, validates seller ownership,
    then delegates to delete_seller_product().

    Phase 5 migration path: remove this function and point the frontend
    directly to DELETE /api/products/<id>/ instead.
    """
    seller = get_object_or_404(Seller, user=user)
    try:
        product = Product.objects.get(seller=seller, name=name, brand=brand)
    except Product.DoesNotExist:
        raise NotFound('Product not found in your inventory.')
    except Product.MultipleObjectsReturned:
        # If multiple products match name+brand, pick the oldest one
        product = Product.objects.filter(seller=seller, name=name, brand=brand).order_by('created_at').first()

    return delete_seller_product(user, product.id)


# ── Cart ──────────────────────────────────────────────────────────────────────

def get_cart_items(user):
    buyer = get_object_or_404(Buyer, user=user)
    cart = Cart.objects.filter(buyer=buyer).first()
    if not cart:
        return []

    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image': item.product.image.url if item.product.image else None,
        }
        for item in CartItem.objects.filter(cart=cart).select_related('product')
    ]


def add_to_cart_item(user, product_id, quantity):
    buyer = get_object_or_404(Buyer, user=user)
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(buyer=buyer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity

    cart_item.save()
    return cart_item


def remove_cart_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    cart = get_object_or_404(Cart, buyer=buyer)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    return True


# ── Wishlist ──────────────────────────────────────────────────────────────────

def get_wishlist_items(user):
    buyer = get_object_or_404(Buyer, user=user)
    return [
        {
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'image': item.product.image.url if item.product.image else None,
        }
        for item in Wishlist.objects.filter(buyer=buyer).select_related('product')
    ]


def add_to_wishlist_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(buyer=buyer, product=product)
    return product


def remove_wishlist_item(user, product_id):
    buyer = get_object_or_404(Buyer, user=user)
    wishlist_item = get_object_or_404(Wishlist, buyer=buyer, product_id=product_id)
    wishlist_item.delete()
    return True


# ── Profile ───────────────────────────────────────────────────────────────────

def get_profile_for_user(user):
    if Buyer.objects.filter(user=user).exists():
        buyer = Buyer.objects.get(user=user)
        return {
            'account_type': 'buyer',
            'name': f'{user.first_name} {user.last_name}',
            'email': user.email,
            'phone': buyer.phone_number,
            'address': buyer.address,
            'city': buyer.city,
            'country': buyer.country,
            'pincode': buyer.pincode,
            'age': buyer.age,
        }

    if Seller.objects.filter(user=user).exists():
        seller = Seller.objects.get(user=user)
        return {
            'account_type': 'seller',
            'company_name': seller.company_name,
            'email': user.email,
            'phone': seller.contact_number,
            'address': seller.address,
            'city': seller.city,
            'country': seller.country,
            'pincode': seller.pincode,
        }

    return None


def create_product_for_seller(user, validated_data):
    seller = get_object_or_404(Seller, user=user)
    product = Product.objects.create(seller=seller, **validated_data)
    return product


# ── Shipping Addresses ────────────────────────────────────────────────────────

def get_shipping_addresses(user):
    buyer = get_object_or_404(Buyer, user=user)
    return ShippingAddress.objects.filter(buyer=buyer).order_by('-is_default', '-created_at')


def create_shipping_address(user, validated_data):
    """
    Creates a new shipping address for the buyer.
    If is_default=True, clears the default flag from all other addresses first.
    """
    buyer = get_object_or_404(Buyer, user=user)
    is_default = validated_data.get('is_default', False)

    if is_default:
        ShippingAddress.objects.filter(buyer=buyer, is_default=True).update(is_default=False)

    address = ShippingAddress.objects.create(buyer=buyer, **validated_data)
    return address


def update_shipping_address(user, address_id, validated_data):
    buyer = get_object_or_404(Buyer, user=user)
    address = get_object_or_404(ShippingAddress, id=address_id, buyer=buyer)

    is_default = validated_data.get('is_default', False)
    if is_default:
        ShippingAddress.objects.filter(buyer=buyer, is_default=True).exclude(id=address_id).update(is_default=False)

    for field, value in validated_data.items():
        setattr(address, field, value)
    address.save()
    return address


def delete_shipping_address(user, address_id):
    buyer = get_object_or_404(Buyer, user=user)
    address = get_object_or_404(ShippingAddress, id=address_id, buyer=buyer)
    address.delete()
    return True


def _get_or_create_default_address(buyer):
    """
    Internal helper: returns the buyer's default shipping address.
    If none exists, auto-creates one from the buyer's profile data
    to maintain checkout compatibility with the existing frontend.
    """
    # Try explicit default
    address = ShippingAddress.objects.filter(buyer=buyer, is_default=True).first()
    if address:
        return address

    # Try any existing address
    address = ShippingAddress.objects.filter(buyer=buyer).first()
    if address:
        return address

    # Auto-generate from buyer profile — Phase 5 migration: remove this fallback
    user = buyer.user
    address = ShippingAddress.objects.create(
        buyer=buyer,
        recipient_name=f'{user.first_name} {user.last_name}'.strip() or user.username,
        phone_number=buyer.phone_number,
        address=buyer.address,
        city=buyer.city,
        country=buyer.country,
        pincode=buyer.pincode,
        is_default=True,
    )
    logger.info('Auto-created shipping address for buyer %s from profile', user.username)
    return address


# ── Checkout & Orders ─────────────────────────────────────────────────────────

def place_order_from_cart(user, shipping_address_id=None, notes=None):
    """
    Converts the buyer's active cart into an Order.

    Guarantees:
    - Atomic: all DB writes succeed or all roll back.
    - Overselling prevention: stock is validated and decremented inside the
      same transaction, preventing race conditions from producing negative stock.

    Raises ValidationError if:
    - The cart is empty.
    - Any product has insufficient stock.
    """
    buyer = get_object_or_404(Buyer, user=user)

    with transaction.atomic():
        cart = Cart.objects.filter(buyer=buyer).first()
        if not cart:
            raise ValidationError('Your cart is empty.')

        # Use select_for_update to lock product rows for the duration of this
        # transaction, preventing concurrent checkouts from overselling.
        cart_items = list(
            CartItem.objects
            .select_for_update()
            .filter(cart=cart)
        )

        if not cart_items:
            raise ValidationError('Your cart is empty.')

        cart_item_ids = [item.id for item in cart_items]
        product_ids = [item.product_id for item in cart_items if item.product_id]
        products_by_id = Product.objects.select_for_update().in_bulk(product_ids)

        # ── 1. Validate stock for all items before touching anything ────────
        for item in cart_items:
            product = products_by_id.get(item.product_id)
            if product is None:
                raise ValidationError('A cart item references a product that no longer exists.')
            item.product = product

            if product.stock < item.quantity:
                raise ValidationError(
                    f'Insufficient stock for "{product.name}". '
                    f'Available: {product.stock}, requested: {item.quantity}.'
                )

        # ── 2. Resolve shipping address ─────────────────────────────────────
        if shipping_address_id:
            shipping_address = get_object_or_404(
                ShippingAddress, id=shipping_address_id, buyer=buyer
            )
        else:
            shipping_address = _get_or_create_default_address(buyer)

        # ── 3. Compute totals ───────────────────────────────────────────────
        total_amount = sum(
            item.product.price * item.quantity for item in cart_items
        )

        # ── 4. Generate unique order number ─────────────────────────────────
        order_number = f'ORD-{uuid.uuid4().hex[:12].upper()}'

        # ── 5. Create the Order record ──────────────────────────────────────
        order = Order.objects.create(
            buyer=buyer,
            shipping_address=shipping_address,
            order_number=order_number,
            status=Order.PENDING,
            total_amount=total_amount,
            notes=notes or '',
        )

        # ── 6. Create OrderItems & deduct stock ─────────────────────────────
        for item in cart_items:
            unit_price = item.product.price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=unit_price,
                total_price=unit_price * item.quantity,
            )
            # Deduct stock — DB CHECK constraint prevents negative values
            Product.objects.filter(pk=item.product.pk).update(
                stock=item.product.stock - item.quantity
            )

        # ── 7. Clear the cart ────────────────────────────────────────────────
        CartItem.objects.filter(id__in=cart_item_ids).delete()

    logger.info('Order %s created for buyer %s (total: %s)', order.order_number, user.username, total_amount)
    return order


def cancel_order(user, order_id):
    """
    Cancels an order and restores product stock.
    Only PENDING or CONFIRMED orders can be cancelled.
    """
    buyer = get_object_or_404(Buyer, user=user)
    order = get_object_or_404(Order, id=order_id, buyer=buyer)

    cancellable = {Order.PENDING, Order.CONFIRMED}
    if order.status not in cancellable:
        raise ValidationError(
            f'Order cannot be cancelled because its current status is "{order.status}". '
            f'Only pending or confirmed orders can be cancelled.'
        )

    with transaction.atomic():
        # Restore stock for each order item
        for item in order.items.select_related('product').all():
            Product.objects.filter(pk=item.product.pk).update(
                stock=item.product.stock + item.quantity
            )

        order.status = Order.CANCELLED
        order.save(update_fields=['status', 'updated_at'])

    logger.info('Order %s cancelled for buyer %s — stock restored', order.order_number, user.username)
    return order


def get_buyer_orders(user):
    buyer = get_object_or_404(Buyer, user=user)
    return (
        Order.objects
        .filter(buyer=buyer)
        .prefetch_related('items__product')
        .select_related('shipping_address')
        .order_by('-created_at')
    )


def get_seller_orders(user):
    """
    Returns all order items whose product belongs to this seller,
    optimized with select_related for orders, buyers, and products.
    """
    seller = get_object_or_404(Seller, user=user)
    return (
        OrderItem.objects
        .filter(product__seller=seller)
        .select_related('order__buyer__user', 'product__seller')
        .order_by('-order__created_at')
    )


def get_seller_products(user):
    """
    Returns products owned by the authenticated seller.
    Optimized with select_related for the seller entity.
    """
    seller = get_object_or_404(Seller, user=user)
    return Product.objects.filter(seller=seller).select_related('seller')


def get_seller_stats(user):
    """
    Retrieves and aggregates sales, inventory, category, and health statistics
    for the authenticated seller's dashboard.
    """
    seller = get_object_or_404(Seller, user=user)
    products = Product.objects.filter(seller=seller)

    total_products = products.count()
    total_units = sum(p.stock for p in products)
    total_value = sum(float(p.price) * p.stock for p in products)
    avg_price = float(products.aggregate(avg=models.Avg('price'))['avg'] or 0.0)

    # Category breakdown
    cat_counts = {}
    for p in products:
        cat = p.category or 'Uncategorized'
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    by_category = [
        {
            'name': cat,
            'count': count,
            'pct': round((count / total_products) * 100) if total_products > 0 else 0
        }
        for cat, count in cat_counts.items()
    ]
    by_category.sort(key=lambda x: x['count'], reverse=True)

    # Low stock items (stock <= 10)
    low_stock_qs = products.filter(stock__lte=10).order_by('stock')
    low_stock_items = [
        {
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
            'category': p.category,
            'brand': p.brand,
        }
        for p in low_stock_qs
    ]

    # Top by value
    top_by_value = []
    for p in products:
        val = float(p.price) * p.stock
        top_by_value.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
            'value': val,
            'share': round((val / total_value) * 100) if total_value > 0 else 0
        })
    top_by_value.sort(key=lambda x: x['value'], reverse=True)
    top_by_value = top_by_value[:8]

    # Price buckets
    buckets = [
        { 'label': '₹0 – 500', 'min': 0, 'max': 500 },
        { 'label': '₹500 – 2k', 'min': 500, 'max': 2000 },
        { 'label': '₹2k – 10k', 'min': 2000, 'max': 10000 },
        { 'label': '₹10k+', 'min': 10000, 'max': float('inf') },
    ]
    price_buckets = []
    for b in buckets:
        if b['max'] == float('inf'):
            count = products.filter(price__gte=b['min']).count()
        else:
            count = products.filter(price__gte=b['min'], price__lt=b['max']).count()
        price_buckets.append({
            'label': b['label'],
            'count': count,
            'pct': round((count / total_products) * 100) if total_products > 0 else 0
        })

    # Stock health
    healthy_stock = products.filter(stock__gt=10).count()
    warning_stock = products.filter(stock__gt=0, stock__lte=10).count()
    out_of_stock = products.filter(stock=0).count()

    return {
        'totalProducts': total_products,
        'totalUnits': total_units,
        'totalValue': total_value,
        'avgPrice': avg_price,
        'lowStockCount': len(low_stock_items),
        'lowStockItems': low_stock_items,
        'byCategory': by_category,
        'topByValue': top_by_value,
        'priceBuckets': price_buckets,
        'healthyStock': healthy_stock,
        'warningStock': warning_stock,
        'outOfStock': out_of_stock,
    }


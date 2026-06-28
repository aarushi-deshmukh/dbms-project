from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.user.username


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.company_name
    

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True, related_name='products')

    name = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.IntegerField()

    category = models.CharField(max_length=100, null=True, blank=True)

    image = models.ImageField(upload_to="products/", null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(stock__gte=0), name='product_stock_non_negative'),
        ]
        indexes = [
            models.Index(fields=['seller']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        if self.stock < 0:
            raise ValidationError('Stock cannot be negative.')
    
class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['buyer']),
        ]

    def __str__(self):
        return f"{self.buyer.user.username} Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name='items')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_items')

    quantity = models.IntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product'),
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name='cartitem_quantity_positive'),
        ]

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than 0.')
    
class Wishlist(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='wishlists')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['buyer']),
            models.Index(fields=['product']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['buyer', 'product'], name='unique_buyer_product_wishlist'),
        ]

    def __str__(self):
        return f"{self.buyer.user.username} - {self.product.name}"


class ShippingAddress(models.Model):
    """
    Shipping address model for future checkout implementation.
    Stores buyer's shipping addresses for order delivery.
    """
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='shipping_addresses')

    recipient_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['buyer']),
            models.Index(fields=['is_default']),
        ]

    def __str__(self):
        return f"{self.recipient_name} - {self.address}"


class Order(models.Model):
    """
    Order model representing a completed purchase by a buyer.

    Status flow: PENDING → CONFIRMED → PROCESSING → SHIPPED → DELIVERED
                         ↘ CANCELLED (from PENDING or CONFIRMED only)
    """
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    order_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['buyer']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['order_number']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    """
    OrderItem model for future checkout implementation.
    Represents individual products in an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')

    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"
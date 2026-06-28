<template>
  <div>
    <div class="cart-page">
      <div class="cart-container">
        <div class="page-header">
          <div>
            <h1>Your Cart</h1>
            <p class="item-count">{{ cart.length }} {{ cart.length === 1 ? 'item' : 'items' }}</p>
          </div>
        </div>

        <div v-if="cart.length === 0" class="empty-state">
          <div class="empty-icon">🛒</div>
          <h2>Your cart is empty</h2>
          <p>Add items to get started</p>
          <button @click="goHome" class="continue-btn">Continue Shopping</button>
        </div>

        <div v-else class="cart-content">
          <div class="cart-items">
            <div v-for="item in cart" :key="item.product_id" class="cart-item">
              <div class="item-main">
                <div class="item-image-placeholder">
                  <img v-if="item.image" :src="item.image" class="product-image" />
                  <span v-else>{{ item.name.charAt(0) }}</span>
                </div>
                <div class="item-info">
                  <h3>{{ item.name }}</h3>
                  <p class="brand">{{ item.brand }}</p>
                  <div class="item-footer">
                    <span class="quantity-badge">Qty {{ item.quantity }}</span>
                    <span class="price">${{ (item.price * item.quantity).toFixed(2) }}</span>
                  </div>
                </div>
              </div>
              <div class="item-actions">
                <button @click="addToWishlist(item)" class="action-link">
                  Save for later
                </button>
                <button @click="removeFromCart(item)" class="action-link remove">
                  Remove
                </button>
              </div>
            </div>
          </div>

          <div class="cart-summary">
            <h2>Order Summary</h2>

            <div class="summary-details">
              <div class="summary-row">
                <span>Subtotal</span>
                <span>${{ cartTotal }}</span>
              </div>
              <div class="summary-row">
                <span>Shipping</span>
                <span class="free">Free</span>
              </div>
              <div class="divider"></div>
              <div class="summary-row total">
                <span>Total</span>
                <span>${{ cartTotal }}</span>
              </div>
            </div>

            <button @click="checkout" class="checkout-btn">
              Proceed to Checkout
            </button>

            <p class="secure-note">🔒 Secure checkout</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from "@/stores/cart";
import { useWishlistStore } from "@/stores/wishlist";

export default {
  computed: {
    cart() {
      const cartStore = useCartStore();
      return cartStore.items;
    },
    cartTotal() {
      const cartStore = useCartStore();
      return cartStore.totalPrice.toFixed(2);
    }
  },

  methods: {
    async fetchCartItems() {
      try {
        const cartStore = useCartStore();
        await cartStore.fetchCart();
      } catch {
        console.error("Failed to load cart");
      }
    },

    async removeFromCart(product) {
      try {
        const cartStore = useCartStore();
        await cartStore.removeItem(product.product_id);
      } catch {
        console.error("Failed to remove item");
      }
    },

    async addToWishlist(product) {
      try {
        const wishlistStore = useWishlistStore();
        const cartStore = useCartStore();
        
        await wishlistStore.addItem(product.product_id);
        await cartStore.removeItem(product.product_id);
      } catch {
        console.error("Failed to save for later");
      }
    },

    async checkout() {
      try {
        const cartStore = useCartStore();
        await cartStore.checkout();
        alert("Order placed successfully!");
      } catch {
        alert("Failed to place order.");
      }
    },

    goHome() {
      this.$router.push('/shopping');
    }
  },

  mounted() {
    this.fetchCartItems();
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.cart-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding: 100px 20px 40px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

/* Page Header */
.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.item-count {
  font-size: 1rem;
  color: #666;
  margin: 8px 0 0 0;
  font-weight: 400;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 24px;
  opacity: 0.3;
}

.empty-state h2 {
  font-size: 1.3rem;
  font-weight: 400;
  color: #888;
  margin: 0 0 12px 0;
}

.empty-state p {
  font-size: 1.1rem;
  color: #888;
  margin: 0 0 40px 0;
}

.continue-btn {
  background-color: #000;
  color: #ffffff;
  border: none;
  padding: 16px 40px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.continue-btn:hover {
  background-color: #333;
}

/* Cart Content Layout */
.cart-content {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

/* Cart Items */
.cart-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cart-item {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s ease;
}

.cart-item:hover {
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d0d0d0;
}

.item-main {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.item-image-placeholder {
  width: 60px;
  height: 60px;
  background-color: #f8f8f8;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.item-image-placeholder span {
  font-size: 1.5rem;
  font-weight: 600;
  color: #666;
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.item-info h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.brand {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.item-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 12px;
}

.quantity-badge {
  font-size: 0.9rem;
  color: #666;
  background-color: #f8f8f8;
  padding: 4px 12px;
  border-radius: 12px;
}

.price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #000;
  margin-left: auto;
}

.item-actions {
  display: flex;
  gap: 24px;
  padding-left: 84px;
}

.action-link {
  background: none;
  border: none;
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color 0.2s;
}

.action-link:hover {
  color: #000;
}

.action-link.remove:hover {
  color: #dc2626;
}

/* Cart Summary */
.cart-summary {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  position: sticky;
  top: 100px;
}

.cart-summary h2 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #000;
  margin: 0 0 20px 0;
}

.summary-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

.summary-row span:last-child {
  color: #000;
  font-weight: 500;
}

.free {
  color: #16a34a !important;
}

.divider {
  height: 1px;
  background-color: #f0f0f0;
  margin: 8px 0;
}

.summary-row.total {
  font-size: 1.5rem;
  color: #000;
  font-weight: 700;
}

.summary-row.total span {
  font-weight: 700;
}

.checkout-btn {
  width: 100%;
  background-color: #000;
  color: #ffffff;
  border: none;
  padding: 12px;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 16px;
}

.checkout-btn:hover {
  background-color: #333;
}

.secure-note {
  text-align: center;
  font-size: 0.85rem;
  color: #888;
  margin: 0;
}

/* Responsive */
@media (max-width: 968px) {
  .cart-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .cart-summary {
    position: static;
  }
}

@media (max-width: 640px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .cart-item {
    padding: 20px;
  }

  .item-main {
    gap: 16px;
  }

  .item-image-placeholder {
    width: 60px;
    height: 60px;
  }

  .item-actions {
    padding-left: 76px;
    gap: 16px;
  }

  .cart-summary {
    padding: 20px;
  }
}
</style>
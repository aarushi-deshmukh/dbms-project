<template>
  <div>
    <div class="wishlist-page">
      <div class="wishlist-container">
        <div class="page-header">
          <div>
            <h1>Wishlist</h1>
            <p class="item-count">{{ wishlist.length }} {{ wishlist.length === 1 ? 'item' : 'items' }}</p>
          </div>
        </div>

        <div v-if="wishlist.length === 0" class="empty-state">
          <div class="empty-icon">♡</div>
          <h2>Your wishlist is empty</h2>
          <p>Save items you love for later</p>
          <button @click="goHome" class="continue-btn">Continue Shopping</button>
        </div>

        <div v-else class="wishlist-content">
          <div class="wishlist-items">
            <div v-for="item in wishlist" :key="item.id" class="wishlist-item">
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
                    <span class="price">${{ item.price }}</span>
                  </div>
                </div>
              </div>
              <div class="item-actions">
                <button @click="addToCart(item)" class="action-link primary">
                  Add to cart
                </button>
                <button @click="removeFromWishlist(item)" class="action-link remove">
                  Remove
                </button>
              </div>
            </div>
          </div>

          <div class="wishlist-summary">
            <h2>Quick Actions</h2>

            <div class="summary-stats">
              <div class="stat-item">
                <span class="stat-label">Total Items</span>
                <span class="stat-value">{{ wishlist.length }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Total Value</span>
                <span class="stat-value">${{ totalValue }}</span>
              </div>
            </div>

            <button @click="addAllToCart" class="add-all-btn">
              Add All to Cart
            </button>

            <p class="info-note">Items are saved until you remove them</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useWishlistStore } from "@/stores/wishlist";
import { useCartStore } from "@/stores/cart";

export default {
  computed: {
    wishlist() {
      const wishlistStore = useWishlistStore();
      return wishlistStore.items;
    },
    totalValue() {
      return this.wishlist
        .reduce((sum, item) => sum + parseFloat(item.price), 0)
        .toFixed(2);
    }
  },

  methods: {
    async fetchWishlistItems() {
      try {
        const wishlistStore = useWishlistStore();
        await wishlistStore.fetchWishlist();
      } catch {
        console.error("Failed to fetch wishlist");
      }
    },

    goHome() {
      this.$router.push('/shopping');
    },

    async removeFromWishlist(product) {
      try {
        const wishlistStore = useWishlistStore();
        const id = product.product_id || product.id;
        await wishlistStore.removeItem(id);
      } catch {
        console.error("Failed to remove item");
      }
    },

    async addToCart(product) {
      const id = product.product_id || product.id;

      if (!id) {
        console.error("Invalid product ID:", product);
        return;
      }

      try {
        const cartStore = useCartStore();
        const wishlistStore = useWishlistStore();
        await cartStore.addItem(id, 1);
        await wishlistStore.removeItem(id);
      } catch (err) {
        console.error("Add to cart failed:", err);
      }
    },

    async addAllToCart() {
      try {
        const cartStore = useCartStore();
        const wishlistStore = useWishlistStore();
        
        for (const item of this.wishlist) {
          const id = item.product_id || item.id;
          await cartStore.addItem(id, 1);
          await wishlistStore.removeItem(id);
        }

        alert("All items added to cart");
      } catch (err) {
        console.error("Failed to add all to cart:", err);
      }
    }
  },

  mounted() {
    this.fetchWishlistItems();
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.wishlist-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding: 100px 20px 60px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
}

.wishlist-container {
  max-width: 1200px;
  margin: 0 auto;
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
  padding: 120px 20px;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 24px;
  opacity: 0.2;
  color: #1a1a1a;
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

/* Wishlist Content Layout */
.wishlist-content {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

/* Wishlist Items */
.wishlist-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.wishlist-item {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s ease;
}

.wishlist-item:hover {
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

.action-link.primary {
  color: #000;
  font-weight: 500;
}

.action-link.remove:hover {
  color: #dc2626;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

/* Wishlist Summary */
.wishlist-summary {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  position: sticky;
  top: 100px;
}

.wishlist-summary h2 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #000;
  margin: 0 0 20px 0;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.stat-value {
  font-size: 1rem;
  font-weight: 500;
  color: #000;
}

.add-all-btn {
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

.add-all-btn:hover {
  background-color: #333;
}

.info-note {
  text-align: center;
  font-size: 0.85rem;
  color: #888;
  margin: 0;
}

/* Responsive */
@media (max-width: 968px) {
  .wishlist-content {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .wishlist-summary {
    position: static;
  }
}

@media (max-width: 640px) {
  .page-header h1 {
    font-size: 2rem;
  }

  .wishlist-item {
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

  .wishlist-summary {
    padding: 20px;
  }
}
</style>
<template>
  <div>
    <div class="history-page">
      <div class="history-container">
        <div class="page-header">
          <h1>Purchase History</h1>
          <select v-model="filterDays" class="date-filter">
            <option value="all">All Time</option>
            <option value="7">Last 7 Days</option>
            <option value="30">Last 30 Days</option>
            <option value="90">Last 3 Months</option>
          </select>
        </div>

        <div v-if="filteredOrders.length === 0" class="empty-state">
          <p>No orders found</p>
        </div>

        <div v-else class="orders-list">
          <div v-for="order in filteredOrders" :key="order.order_id" class="order-card">
            <div class="order-header">
              <div class="order-info">
                <span class="order-id">Order #{{ order.order_id }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="order-status">
                <span class="status-badge" :class="getStatusClass(order.status)">
                  {{ order.status }}
                </span>
              </div>
            </div>

            <div class="order-items">
              <div v-for="item in order.items" :key="item.product_id" class="order-item">
                <span class="item-name">{{ item.product_name }}</span>
                <span class="item-quantity">x{{ item.quantity }}</span>
              </div>
            </div>

            <div class="order-footer">
              <div class="status-details">
                <span class="label">Status:</span>
                <span class="value">{{ order.status_details }}</span>
              </div>
              <div class="order-total">
                <span class="total-label">Total:</span>
                <span class="total-amount">${{ order.total_amount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useOrdersStore } from "@/stores/orders";

export default {
  data() {
    return {
      filterDays: 'all'
    };
  },
  computed: {
    orders() {
      const ordersStore = useOrdersStore();
      return ordersStore.orders;
    },
    filteredOrders() {
      if (this.filterDays === 'all') return this.orders;

      const now = new Date();
      const cutoff = new Date(now.setDate(now.getDate() - parseInt(this.filterDays)));

      return this.orders.filter(order => {
        return new Date(order.created_at) >= cutoff;
      });
    }
  },
  methods: {
    async fetchOrderHistory() {
      try {
        const ordersStore = useOrdersStore();
        await ordersStore.fetchOrderHistory();
      } catch (error) {
        console.error("Error fetching order history:", error);
      }
    },
    formatDate(date) {
      const d = new Date(date);
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      const year = d.getFullYear();
      const hours = String(d.getHours()).padStart(2, '0');
      const minutes = String(d.getMinutes()).padStart(2, '0');
      return `${month}/${day}/${year} ${hours}:${minutes}`;
    },
    getStatusClass(status) {
      const statusLower = status.toLowerCase();
      if (statusLower.includes('delivered') || statusLower.includes('completed')) {
        return 'status-success';
      } else if (statusLower.includes('pending') || statusLower.includes('processing')) {
        return 'status-pending';
      } else if (statusLower.includes('cancelled') || statusLower.includes('failed')) {
        return 'status-error';
      }
      return 'status-default';
    }
  },
  mounted() {
    this.fetchOrderHistory();
  }
};
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background-color: #ffffff;
  padding-top: 100px;
  margin: 0px auto;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
}

.history-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e0e0e0;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 600;
  color: #000;
  margin: 0;
}

.date-filter {
  padding: 12px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #000;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
}

.date-filter:hover {
  border-color: #000;
}

.date-filter:focus {
  border-color: #000;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-state p {
  font-size: 1.3rem;
  color: #888;
}

/* Orders List */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s ease;
}

.order-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #d0d0d0;
}

/* Order Header */
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-id {
  font-size: 1.1rem;
  font-weight: 600;
  color: #000;
}

.order-date {
  font-size: 0.9rem;
  color: #666;
}

.order-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status-pending {
  background-color: #fff3e0;
  color: #e65100;
}

.status-error {
  background-color: #ffebee;
  color: #c62828;
}

.status-default {
  background-color: #f5f5f5;
  color: #666;
}

/* Order Items */
.order-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.item-name {
  font-size: 1rem;
  color: #000;
}

.item-quantity {
  font-size: 0.9rem;
  color: #666;
  background-color: #f8f8f8;
  padding: 4px 12px;
  border-radius: 12px;
}

/* Order Footer */
.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.status-details {
  display: flex;
  gap: 8px;
  font-size: 0.9rem;
}

.status-details .label {
  color: #666;
}

.status-details .value {
  color: #000;
  font-weight: 500;
}

.order-total {
  display: flex;
  align-items: center;
  gap: 8px;
}

.total-label {
  font-size: 0.95rem;
  color: #666;
}

.total-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: #000;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .date-filter {
    width: 100%;
  }

  .order-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
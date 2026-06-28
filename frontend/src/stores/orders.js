import { defineStore } from "pinia";
import api from "@/api";

export const useOrdersStore = defineStore("orders", {
  state: () => ({
    orders: [],
    sellerOrders: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchOrderHistory() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("orders/");
        this.orders = res.data.data || [];
        return this.orders;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchSellerOrders() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("seller/orders/");
        this.sellerOrders = res.data;
        return this.sellerOrders;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async cancelOrder(orderId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post(`orders/${orderId}/cancel/`);
        // Refresh local orders list
        await this.fetchOrderHistory();
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
  },
});

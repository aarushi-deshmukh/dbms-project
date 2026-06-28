import { defineStore } from "pinia";
import api from "@/api";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
    loading: false,
    error: null,
  }),
  getters: {
    cartCount: (state) => state.items.reduce((s, item) => s + item.quantity, 0),
    totalPrice: (state) =>
      state.items.reduce((s, item) => s + parseFloat(item.price) * item.quantity, 0),
  },
  actions: {
    async fetchCart() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("cart/");
        this.items = res.data.items || [];
        return this.items;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async addItem(productId, quantity = 1) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("cart/add/", {
          product_id: productId,
          quantity,
        });
        await this.fetchCart();
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async removeItem(productId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.delete(`cart/remove/${productId}/`);
        this.items = this.items.filter((item) => item.product_id !== productId);
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async checkout(shippingAddressId = null, notes = "") {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("place-order/", {
          shipping_address_id: shippingAddressId,
          notes,
        });
        this.items = []; // Clear local cart items upon success
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

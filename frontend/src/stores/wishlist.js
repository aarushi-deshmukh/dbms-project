import { defineStore } from "pinia";
import api from "@/api";

export const useWishlistStore = defineStore("wishlist", {
  state: () => ({
    items: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchWishlist() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("wishlist/");
        this.items = res.data.items || [];
        return this.items;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async addItem(productId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("wishlist/add/", {
          product_id: productId,
        });
        await this.fetchWishlist();
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
        const res = await api.delete(`wishlist/remove/${productId}/`);
        this.items = this.items.filter((item) => item.product_id !== productId);
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

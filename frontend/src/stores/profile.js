import { defineStore } from "pinia";
import api from "@/api";

export const useProfileStore = defineStore("profile", {
  state: () => ({
    profile: null,
    shippingAddresses: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchProfile() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("profile/");
        this.profile = res.data;
        return this.profile;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async fetchShippingAddresses() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("shipping-addresses/");
        this.shippingAddresses = res.data.data || [];
        return this.shippingAddresses;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async addShippingAddress(addressData) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("shipping-addresses/", addressData);
        await this.fetchShippingAddresses();
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateShippingAddress(addressId, addressData) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.put(`shipping-addresses/${addressId}/`, addressData);
        await this.fetchShippingAddresses();
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async deleteShippingAddress(addressId) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.delete(`shipping-addresses/${addressId}/`);
        this.shippingAddresses = this.shippingAddresses.filter((addr) => addr.id !== addressId);
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async updateProfile(profileData) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.put("profile/", profileData);
        // Refresh profile state from the server response
        if (res.data?.data) {
          this.profile = res.data.data;
        } else {
          await this.fetchProfile();
        }
        return res.data;
      } catch (err) {
        this.error = err.response?.data?.message || err.message;
        throw err;
      } finally {
        this.loading = false;
      }
    },
    async deleteAccount() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.delete("profile/");
        // Clear all auth state from localStorage
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("user_type");
        this.profile = null;
        this.shippingAddresses = [];
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

import { defineStore } from "pinia";
import api from "@/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: localStorage.getItem("access") || null,
    refreshToken: localStorage.getItem("refresh") || null,
    userType: localStorage.getItem("user_type") || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    isBuyer: (state) => state.userType === "buyer",
    isSeller: (state) => state.userType === "seller",
  },
  actions: {
    init() {
      const access = localStorage.getItem("access");
      const refresh = localStorage.getItem("refresh");
      const userType = localStorage.getItem("user_type");
      if (access && userType) {
        this.accessToken = access;
        this.refreshToken = refresh;
        this.userType = userType;
        this.user = {
          account_type: userType,
        };
      }
    },
    async login(email, password, accountType) {
      try {
        const response = await api.post("signin/", {
          email,
          password,
          account_type: accountType,
        });
        const data = response.data;
        if (data.success) {
          this.accessToken = data.access;
          this.refreshToken = data.refresh;
          this.userType = data.account_type.toLowerCase();
          this.user = {
            id: data.user_id,
            email: data.email,
            account_type: this.userType,
          };
          localStorage.setItem("access", this.accessToken);
          localStorage.setItem("refresh", this.refreshToken);
          localStorage.setItem("user_type", this.userType);
          return data;
        } else {
          throw new Error(data.message || "Login failed");
        }
      } catch (err) {
        console.error("Login store error:", err);
        throw err;
      }
    },
    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.userType = null;
      this.user = null;
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user_type");
    },
  },
});

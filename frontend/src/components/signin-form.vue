<template>
  <div class="form-container">
    <form @submit.prevent="submitForm" class="signin-form">
      <div class="form-header">
        <h1>Sign In</h1>
        <p class="form-subtitle">Access your account securely</p>
      </div>

      <!-- Account Type Toggle Buttons -->
      <div class="account-tabs">
        <button type="button" :class="{ active: account_type === 'Buyer' }" @click="account_type = 'Buyer'"
          class="account-tab">
          Buyer
        </button>
        <button type="button" :class="{ active: account_type === 'Seller' }" @click="account_type = 'Seller'"
          class="account-tab">
          Seller
        </button>
      </div>

      <div class="form-content">
        <div class="form-section">
          <div class="input-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" v-model="email" required placeholder="Enter your email" />
          </div>

          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required placeholder="Enter your password" />
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="submit-btn" :disabled="loading">
        <span v-if="loading" class="loading-spinner"></span>
        <span v-else>Sign In as {{ account_type }}</span>
      </button>

      <!-- Message Section -->
      <div class="message-container">
        <div v-if="message" class="message success">
          {{ message }}
        </div>
        <div v-if="error" class="message error">
          {{ error }}
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth"
import { mapActions } from "pinia"

export default {
  name: "SigninForm",

  data() {
    return {
      email: "",
      password: "",
      account_type: "Buyer",
      loading: false,
      message: "",
      error: ""
    }
  },

  methods: {
    ...mapActions(useAuthStore, ["login"]),

    setAccountType(type) {
      this.account_type = type
    },

    async submitForm() {
      this.loading = true
      this.error = ""

      try {
        const data = await this.login(
          this.email,
          this.password,
          this.account_type
        )

        const accountType = data.account_type.toLowerCase()

        // redirect based on role
        if (accountType === "buyer") {
          this.$router.push("/")
        } else if (accountType === "seller") {
          this.$router.push("/my-products")
        } else {
          console.log("Unknown account type")
          this.error = "Unknown account type"
        }

      } catch (error) {
        console.log("Login error:", error)
        if (error.response?.data?.message) {
          this.error = error.response.data.message
        } else if (error.response?.data?.error) {
          this.error = error.response.data.error
        } else {
          this.error = "Login failed. Please check your credentials."
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.form-container {
  width: 100%;
  max-width: 100%;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  overflow: visible;
}

.signin-form {
  padding: 0;
}

.form-header {
  text-align: left;
  margin-bottom: 2.5rem;
}

.form-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.form-subtitle {
  color: #666;
  font-size: 0.95rem;
}

.account-tabs {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2.5rem;
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 12px;
}

.account-tab {
  flex: 1;
  padding: 0.875rem 1.25rem;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: #666;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.account-tab.active {
  background: #1a1a1a;
  color: #ffffff;
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.form-content {
  margin-bottom: 2rem;
}

.form-section {
  animation: fadeInUp 0.5s ease-out;
}

.input-group {
  margin-bottom: 1.75rem;
}

.input-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.input-group input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: #fafafa;
  color: #1a1a1a;
}

.input-group input:focus {
  outline: none;
  border-color: #1a1a1a;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.input-group input::placeholder {
  color: #999;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #1a1a1a;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #333;
  transform: translateY(-1px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.message-container {
  margin-top: 1.25rem;
}

.message {
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  animation: slideInDown 0.3s ease-out;
}

.message.success {
  background: #f0f0f0;
  color: #1a1a1a;
  border: 1px solid #e5e5e5;
}

.message.error {
  background: #fff5f5;
  color: #1a1a1a;
  border: 1px solid #ffcccc;
}

@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInDown {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .form-header h1 {
    font-size: 1.75rem;
  }

  .account-tabs {
    gap: 0.5rem;
  }

  .account-tab {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }
}
</style>
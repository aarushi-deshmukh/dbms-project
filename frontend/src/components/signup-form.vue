<template>
  <div class="form-container">
    <form @submit.prevent="submitForm" class="signup-form">
      <div class="form-header">
        <h1>Create Account</h1>
        <p class="form-subtitle">Choose your account type to get started</p>
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
        <!-- Seller Section -->
        <div v-if="account_type === 'Seller'" class="form-section">
          <div class="input-group">
            <label for="company-name">Company Name</label>
            <input type="text" id="company-name" v-model="company_name" required
              placeholder="Enter your company name" />
          </div>
          <div class="input-group">
            <label for="contact-number">Contact Number</label>
            <input type="text" id="contact-number" v-model="contact_number" required
              placeholder="Enter contact number" />
          </div>
        </div>

        <!-- Buyer Section -->
        <div v-if="account_type === 'Buyer'" class="form-section">
          <div class="row">
            <div class="input-group half-width">
              <label for="firstname">First Name</label>
              <input type="text" id="firstname" v-model="first_name" required placeholder="First name" />
            </div>
            <div class="input-group half-width">
              <label for="lastname">Last Name</label>
              <input type="text" id="lastname" v-model="last_name" required placeholder="Last name" />
            </div>
          </div>
          <div class="row">
            <div class="input-group half-width">
              <label for="username">Username</label>
              <input type="text" id="username" v-model="username" required placeholder="Choose username" />
            </div>
            <div class="input-group half-width">
              <label for="age">Age</label>
              <input type="number" id="age" v-model="age" required placeholder="Your age" />
            </div>
          </div>
          <div class="input-group">
            <label for="phonenumber">Phone Number</label>
            <input type="text" id="phonenumber" v-model="phone_number" required placeholder="Enter phone number" />
          </div>
        </div>

        <!-- Common Fields -->
        <div class="common-fields">
          <div class="input-group">
            <label for="email">Email Address</label>
            <input type="email" id="email" v-model="email" required placeholder="Enter your email" />
          </div>
          <div class="row">
            <div class="input-group half-width">
              <label for="address">Address</label>
              <input type="text" id="address" v-model="address" required placeholder="Street address" />
            </div>
            <div class="input-group half-width">
              <label for="city">City</label>
              <input type="text" id="city" v-model="city" required placeholder="Your city" />
            </div>
          </div>
          <div class="row">
            <div class="input-group half-width">
              <label for="country">Country</label>
              <input type="text" id="country" v-model="country" required placeholder="Your country" />
            </div>
            <div class="input-group half-width">
              <label for="pincode">Pincode</label>
              <input type="number" id="pincode" v-model="pincode" required placeholder="ZIP/Postal code" />
            </div>
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" required placeholder="Create a strong password" />
          </div>
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" :disabled="loading" class="submit-btn">
        <span v-if="loading" class="loading-spinner"></span>
        <span v-else>Sign Up as {{ account_type }}</span>
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
import api from "@/api";

export default {
  data() {
    return {
      account_type: "Buyer",
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      password: "",
      age: "",
      phone_number: "",
      company_name: "",
      contact_number: "",
      address: "",
      city: "",
      pincode: "",
      country: "",
      message: "",
      error: "",
      loading: false
    };
  },
  methods: {
    async submitForm() {
      this.loading = true;
      this.message = "";
      this.error = "";

      let apiPath = "";
      let formData = {};

      if (this.account_type === "Buyer") {
        apiPath = "signup/buyer/";
        formData = {
          first_name: this.first_name,
          last_name: this.last_name,
          username: this.username,
          email: this.email,
          password: this.password,
          age: this.age,
          phone_number: this.phone_number,
          address: this.address,
          pincode: this.pincode,
          country: this.country,
          city: this.city
        };
      } else if (this.account_type === "Seller") {
        apiPath = "signup/seller/";
        formData = {
          email: this.email,
          password: this.password,
          company_name: this.company_name,
          contact_number: this.contact_number,
          address: this.address,
          pincode: this.pincode,
          country: this.country,
          city: this.city
        };
      }

      try {
        const response = await api.post(apiPath, formData);
        this.message = response.data.message || "Registration successful!";

        this.$emit("signup-success");

        setTimeout(() => {
          this.$router.push("/signin");
        }, 1200);
      } catch (error) {
        if (error.response?.data?.message) {
          this.error = error.response.data.message;
        } else if (error.response?.data?.error) {
          this.error = error.response.data.error;
        } else if (typeof error.response?.data === 'object') {
          // Join validation error messages if any
          this.error = Object.values(error.response.data).flat().join(" ");
        } else {
          this.error = "Something went wrong!";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
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

.signup-form {
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
  margin-bottom: 2.5rem;
}

.form-section {
  animation: fadeInUp 0.5s ease-out;
}

.common-fields {
  margin-top: 1.5rem;
}

.row {
  display: flex;
  gap: 3rem;
}

.input-group {
  flex: 1;
  margin-bottom: 2rem;
}

.input-group.half-width {
  flex: 0 0 calc(50% - 1.5rem);
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
  .row {
    flex-direction: column;
    gap: 0;
  }

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
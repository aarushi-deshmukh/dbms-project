<template>
  <div class="container">
    <div class="left-side">
      <div class="tabs">
        <router-link :to="'/signup'" :class="{ active: activeTab === 'signup' }" @click="activeTab = 'signup'">Sign-Up</router-link>
        <router-link :to="'/signin'" :class="{ active: activeTab === 'signin' }" @click="activeTab = 'signin'">Sign-In</router-link>
      </div>
    </div>

    <div class="right-side">
      <form @submit.prevent="submitForm">
        <h1>Sign-In</h1>

        <div class="input-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
        </div>

        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button type="submit" :disabled="loading">Sign In</button>
        <p v-if="message" class="success">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      email: '',
      password: '',
      message: '',
      error: '',
      loading: false,
      activeTab: 'signin'
    }
  },
  methods: {
    async submitForm() {
      this.message = ''
      this.error = ''
      this.loading = true

      try {
        const response = await axios.post('http://127.0.0.1:8000/api/signin/', {
          email: this.email,
          password: this.password
        })

        this.message = response.data.message
      } catch (error) {
        this.error = error.response?.data?.error || "Invalid credentials"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style>
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.left-side {
  width: 40%;
  background-color: rgb(62, 123, 39);
  color: rgb(239, 227, 194);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 20px;
  position: relative;
}

.tabs {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: flex-start;
}

.tabs a {
  color: rgb(239, 227, 194);
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  padding: 12px 20px;
  border-radius: 5px;
  transition: background 0.3s, transform 0.2s;
  width: 100%;
}

.tabs a:hover,
.tabs a.active {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(5px);
}

.right-side {
  width: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
}

form {
  background: white;
  color: rgb(93, 135, 54);
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 320px;
  display: flex;
  flex-direction: column;
  text-align: center;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 26px;
  font-weight: bold;
  font-style: italic;
}

.input-group {
  margin-bottom: 15px;
}

label {
  font-size: 14px;
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

button {
  width: 100%;
  padding: 10px;
  background: rgb(62, 123, 39);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background: #ccc;
}

.success {
  color: green;
  text-align: center;
  margin-top: 10px;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>

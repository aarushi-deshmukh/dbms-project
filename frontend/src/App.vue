<template>
  <div class="app-container">
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: "App"
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, sans-serif;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<template>
  <div id="app">
    <navbar/>
    <router-view></router-view>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
export default {
  name: 'app',
  components: {
    'navbar': Navbar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}
input:focus {
  border-color: #3498db !important;
}
.primary-btn {
  background-color: #27ae60 !important;
  border: 1px solid #16a085 !important;
}
.primary-btn:hover {
  background-color: #2ecc71 !important;
}
.secondary-btn {
  background-color: transparent !important;
  color: #27ae60 !important;
  border: 1px solid #27ae60 !important;
}
.secondary-btn:hover {
  background-color: rgba(39, 174, 96, 0.1) !important;
}
a {
  color: #3498db !important;
}
a:hover {
  color: #3380c8 !important;
  cursor: pointer;
}

</style>

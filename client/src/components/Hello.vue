<template>
  <div class="hello">
    <navbar></navbar>
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Hello'
    }
  }
}
</script>

<style scoped>
</style>

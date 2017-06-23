<template>
  <div class="navbar">
    <div class="container">
      <div class="row">
        <div class="navbar-text">
          <h2>Puzzle Hero</h2>
          <span> {{ loginMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Global from '@/global'
export default {
  name: 'navbar',
  data () {
    return {}
  },
  computed: {
    loginMessage () {
      if (Global.isLoggedIn) {
        return 'Welcome!'
      }
      return 'Login'
    }
  }
}
</script>

<style scoped>
  .navbar {
    background-color: #962538;
    border-bottom: 3px solid #CCB47D;
  }
  .navbar-text {
    width: 100%;
  }
  .navbar-text h2 {
    display: inline-block;
    float: left;
    color: white;
    font-size: 2em;
    margin: 10px 0;
  }
  .navbar-text span {
    display: inline-block;
    float: right;
    color: white;
    font-size: 1.3em;
    margin: 14px 0;
  }

</style>

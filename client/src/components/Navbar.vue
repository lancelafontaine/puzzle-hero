<template>
  <div class="navbar">
    <div class="container">
      <div class="row">
        <div class="navbar-text">
          <a href="/">
            <img class="navbar-brand" src="static/scs.ico"/>
            <h2>Puzzle Hero</h2>
          </a>
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
  computed: {
    loginMessage () {
      if (Global.isLoggedIn) {
        return 'Welcome!'
      }
      return ''
    }
  }
}
</script>

<style scoped>
  .navbar {
    background-color: #962538;
    border-bottom: 3px solid #CCB47D;
  }
  .navbar-brand {
    height: 50px;
    padding-top:10px;
    line-height: 60px;
    float: left;
    margin-right:2rem;
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

<template>
  <div class="login">
    <div class="container">
      <div class="row">
        <div id="login-header">
          <button id="login-btn" v-on:click="changeFormType($event)" v-bind:class="{'primary-btn': showingLoginForm, 'secondary-btn': showingRegisterForm}">Login</button>
          <button id="register-btn" v-on:click="changeFormType($event)" v-bind:class="{'primary-btn': showingRegisterForm, 'secondary-btn': showingLoginForm}">Register</button>
        </div>
      </div>
      <div class="row">
        <div id="login-form" class="column column-50 column-offset-25">
          <form v-on:submit.prevent="onSubmit($event)">
            <label for="username"><a>SCS Competitions Slack</a> Username</label>
            <input type="text" placeholder="1337haxxorz" name="username" id="username" required />
            <div class="row" v-if="showingRegisterForm">
              <div class="column">
                <label for="fname">First Name</label>
                <input type="text" placeholder="Alex" name="fname" id="fname" required />
              </div>
              <div class="column">
                <label for="lname">Last Name</label>
                <input type="text" placeholder="Smith" name="lname" id="lname" required />
              </div>
            </div>
            <label for="password">Password</label>
            <input type="password" placeholder="correct_horse_battery_staple" name="password" id="password" required />
            <input type="submit" class="primary-btn" name="submit" id="login-form-submit" value="Submit"/>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import restFactory from '@/js/restFactory'
import global from '@/global'

export default {
  name: 'login',
  data () {
    return {
      email: 'competitions.scs@ecaconcordia.ca',
      showingLoginForm: true,
      showingRegisterForm: false,
      slackUsers: []
    }
  },
  mounted () {
    this.populateSlackUsers()
  },
  methods: {
    populateSlackUsers () {
      restFactory.slackUsers((res) => {
        if (res.status === 200) {
          console.log(res)
        } else {
          global.defaultUserError(res)
        }
      })
    },
    onSubmit (e) {
      const formValues = {}
      const inputs = e.target.elements
      for (let i = 0; i < inputs.length; i++) {
        if (inputs[i].value !== 'Submit') {
          formValues[inputs[i].id] = inputs[i].value
        }
      }
      console.log(formValues)
      // restFactory.login((res) => {})
      // restFactory.register((res) => {})
    },
    changeFormType (e) {
      const idClicked = e.target.id
      if (idClicked === 'register-btn') {
        this.showingLoginForm = false
        this.showingRegisterForm = true
      }
      if (idClicked === 'login-btn') {
        this.showingLoginForm = true
        this.showingRegisterForm = false
      }
    }
  }
}
</script>

<style scoped>
  #login-header {
    width: 100%;
    margin-top: 50px;
    text-align: center;
  }
  #login-form {
    margin-top: 50px;
  }
</style>

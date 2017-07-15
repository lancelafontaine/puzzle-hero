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
          <div class="alert-error" v-show="showingInvalidUsernameError">
            That username doesn't exist in the SCS Competitions Slack group.
            <a href="">Click here to register.</a>
          </div>
          <form v-on:submit.prevent="onSubmit($event)">
            <label for="username"><a>SCS Competitions Slack</a> Username</label>
            <input v-on:keyup="validateEnteredSlackUser($event)" v-on:blur="validateEnteredSlackUser($event)" type="text" placeholder="1337haxxorz" name="username" id="username" list="slack-users-list" required />
            <datalist id="slack-users-list">
            </datalist>
            <label for="password">Password</label>
            <input type="password" placeholder="correct_horse_battery_staple" name="password" id="password" required />
            <input type="submit" class="primary-btn" name="submit" id="login-form-submit" value="Submit"/>
          </form>
          <div id="user-info-div" v-show="currentSlackUsername">
            <p id="user-info-header"><strong>{{currentSlackUsername}}</strong>
              <span v-show="currentSlackRealname">({{currentSlackRealname}})</span>
            </p>
            <img id="user-info-image" v-bind:src="currentSlackImage">
          </div>
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
      showingInvalidUsernameError: false,
      currentSlackUsername: '',
      currentSlackRealname: '',
      currentSlackImage: '',
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
          this.slackUsers = res.data.data
          this.autocompleteSlackUsers()
        } else {
          global.defaultUserError(res)
        }
      })
    },
    validateEnteredSlackUser (e) {
      const userInput = e.target.value
      const validSlackUsername = this.isValidSlackUsername(userInput)
      if (validSlackUsername) {
        this.showingInvalidUsernameError = false
        const slackUser = this.findSlackUserByUsername(userInput)
        this.currentSlackUsername = slackUser.username
        this.currentSlackRealname = slackUser.realname
        this.currentSlackImage = slackUser.avatar
      } else {
        this.currentSlackUsername = ''
        this.currentSlackRealname = ''
        this.currentSlackImage = ''
      }
    },
    findSlackUserByUsername (username) {
      return this.slackUsers.find(user => user.username === username)
    },
    isValidSlackUsername (username) {
      return this.slackUsers.map(user => user.username).includes(username)
    },
    autocompleteSlackUsers () {
      let optionsListString = ''
      this.slackUsers.forEach((user, index) => {
        let optionString = '<option value="' + user.username + '" />'
        optionsListString += optionString
      })
      document.getElementById('slack-users-list').innerHTML = optionsListString
    },
    onSubmit (e) {
      if (this.isValidSlackUsername(this.currentSlackUsername)) {
        this.showingInvalidUsernameError = false
        const formValues = {}
        const inputs = e.target.elements
        for (let i = 0; i < inputs.length; i++) {
          if (inputs[i].value !== 'Submit') {
            formValues[inputs[i].id] = inputs[i].value
          }
        }
      } else {
        this.showingInvalidUsernameError = true
      }
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
  #user-info-div{
    text-align: center;
  }
  #user-info-image {
    border: 2px solid #888888;
    border-radius: 50%;
  }
  .alert-error {
    padding: 10px 20px;
    margin-bottom: 15px;
    border: 1px solid #c0392b;
    border-radius: 5px;
    background-color: #ffeeee;
    color: #c0392b;
  }
</style>

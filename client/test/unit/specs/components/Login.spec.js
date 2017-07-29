import axios from 'axios'
import Vue from 'vue'
import Login from '@/components/Login'

describe('Login.vue', () => {
  let Constructor
  let vm

  beforeEach(() => {
    Constructor = Vue.extend(Login)
    vm = new Constructor().$mount()
    sinon.stub(axios, 'get').returns(Promise.resolve({
      status: 200,
      data: {
        ok: true,
        data: [{
          username: 'testy',
          realname: 'mctestface',
          avatar: 'imagey'
        }]
      }
    }))
  })

  afterEach(() => {
    axios.get.restore()
  })

  it('should render the form buttons', () => {
    expect(vm.$el.querySelector('#login-form-submit').value).to.equal('Submit')
  })

  it('should have default data', () => {
    Constructor = Vue.extend(Login)
    vm = new Constructor()

    expect(vm.email).to.equal('competitions.scs@ecaconcordia.ca')
    expect(vm.showingInvalidUsernameError).to.equal(false)
    expect(vm.currentSlackUsername).to.equal('')
    expect(vm.currentSlackRealname).to.equal('')
    expect(vm.currentSlackImage).to.equal('')
    expect(JSON.stringify(vm.slackUsers)).to.equal('[]')
  })

  it('should call initialization functions on component mount', () => {
    Constructor = Vue.extend(Login)
    vm = new Constructor()

    vm.populateSlackUsers = sinon.spy()
    vm.loadDefaultUserInfo = sinon.spy()

    expect(vm.populateSlackUsers.calledOnce).to.be.false
    expect(vm.loadDefaultUserInfo.calledOnce).to.be.false

    vm = vm.$mount()

    expect(vm.populateSlackUsers.calledOnce).to.be.true
    expect(vm.loadDefaultUserInfo.calledOnce).to.be.true
  })

  it('loadDefaultUserInfo sets defaults for Slack user information', () => {
    vm.currentSlackUsername = 'testing1'
    vm.currentSlackRealname = 'testing2'
    vm.currentSlackImage = 'testing3'

    expect(vm.currentSlackUsername).to.equal('testing1')
    expect(vm.currentSlackRealname).to.equal('testing2')
    expect(vm.currentSlackImage).to.equal('testing3')

    vm.loadDefaultUserInfo()

    expect(vm.currentSlackUsername).to.equal('')
    expect(vm.currentSlackRealname).to.equal('Authenticate with Slack username')
    expect(vm.currentSlackImage).to.equal('static/bug_default.png')
  })

  it('populateSlackUsers sets users and initiates autocompletion upon success', (done) => {
    Constructor = Vue.extend(Login)
    vm = new Constructor()

    vm.autocompleteSlackUsers = sinon.spy()
    vm.slackUsers = 'hotdogs'
    expect(vm.autocompleteSlackUsers.calledOnce).to.be.false
    expect(vm.slackUsers).to.equal('hotdogs')

    vm.populateSlackUsers()

    setTimeout(() => {
      expect(vm.autocompleteSlackUsers.calledOnce).to.be.true
      expect(JSON.stringify(vm.slackUsers)).to.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')
      done()
    }, 20)
  })

  it('populateSlackUsers logs an error upon failure', (done) => {
    Constructor = Vue.extend(Login)
    vm = new Constructor()
    axios.get.restore()
    sinon.stub(axios, 'get').returns(Promise.resolve({
      status: 404,
      data: {
        ok: true,
        data: [{
          username: 'testy',
          realname: 'mctestface',
          avatar: 'imagey'
        }]
      }
    }))

    vm.autocompleteSlackUsers = sinon.spy()
    vm.slackUsers = 'hotdogs'
    expect(vm.autocompleteSlackUsers.calledOnce).to.be.false
    expect(vm.slackUsers).to.equal('hotdogs')

    vm.populateSlackUsers()

    setTimeout(() => {
      expect(vm.autocompleteSlackUsers.calledOnce).to.be.false
      expect(vm.slackUsers).to.equal('hotdogs')
      done()
    }, 20)
  })

  it('validateEnteredSlackUser sets current slack user if valid', () => {
    vm.currentSlackUsername = 'testing1'
    vm.currentSlackRealname = 'testing2'
    vm.currentSlackImage = 'testing3'
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]

    expect(vm.currentSlackUsername).to.equal('testing1')
    expect(vm.currentSlackRealname).to.equal('testing2')
    expect(vm.currentSlackImage).to.equal('testing3')
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const data = {
      target: {
        value: 'testy'
      }
    }
    vm.validateEnteredSlackUser(data)

    expect(vm.currentSlackUsername).to.equal('testy')
    expect(vm.currentSlackRealname).to.equal('mctestface')
    expect(vm.currentSlackImage).to.equal('imagey')
  })

  it('validateEnteredSlackUser sets Slack user defaults if invalid', () => {
    vm.loadDefaultUserInfo = sinon.spy()
    expect(vm.loadDefaultUserInfo.calledOnce).to.be.false

    vm.currentSlackUsername = 'testing1'
    vm.currentSlackRealname = 'testing2'
    vm.currentSlackImage = 'testing3'
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]

    expect(vm.currentSlackUsername).to.equal('testing1')
    expect(vm.currentSlackRealname).to.equal('testing2')
    expect(vm.currentSlackImage).to.equal('testing3')
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const data = {
      target: {
        value: 'wrong name'
      }
    }
    vm.validateEnteredSlackUser(data)

    expect(vm.currentSlackUsername).to.equal('testing1')
    expect(vm.currentSlackRealname).to.equal('testing2')
    expect(vm.currentSlackImage).to.equal('testing3')
    expect(vm.loadDefaultUserInfo.calledOnce).to.be.true
  })

  it('findSlackUserByUsername returns a user if username is found in this.slackUsers', () => {
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const result = vm.findSlackUserByUsername('testy')
    expect(JSON.stringify(result)).to.equal('{"username":"testy","realname":"mctestface","avatar":"imagey"}')
  })

  it('findSlackUserByUsername does not return a user if username is not found in this.slackUsers', () => {
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const result = vm.findSlackUserByUsername('does_not_exist')
    expect(result).to.be.undefined
  })

  it('isValidSlackUsername returns true if the username is found in this.slackUsers', () => {
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const result = vm.isValidSlackUsername('testy')
    expect(result).to.be.true
  })

  it('isValidSlackUsername returns false if the username is found in this.slackUsers', () => {
    vm.slackUsers = [
      {
        username: 'testy',
        realname: 'mctestface',
        avatar: 'imagey'
      }
    ]
    expect(JSON.stringify(vm.slackUsers)).to.be.equal('[{"username":"testy","realname":"mctestface","avatar":"imagey"}]')

    const result = vm.isValidSlackUsername('you will never find me muahaha')
    expect(result).to.be.false
  })
})

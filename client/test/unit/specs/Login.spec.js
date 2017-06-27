import Vue from 'vue'
import Login from '@/components/Login'

describe('Login.vue', () => {
  let vm

  beforeEach(() => {
    const Constructor = Vue.extend(Login)
    vm = new Constructor().$mount()
  })

  it('should render the form and formType buttons', () => {
    expect(vm.$el.querySelector('#login-btn').textContent).to.equal('Login')
    expect(vm.$el.querySelector('#register-btn').textContent).to.equal('Register')
    expect(vm.$el.querySelector('#login-form-submit').value).to.equal('Submit')
  })

  it('should have default data', () => {
    expect(vm.email).to.equal('competitions.scs@ecaconcordia.ca')
    expect(vm.showingLoginForm).to.equal(true)
    expect(vm.showingRegisterForm).to.equal(false)
  })

  it('changeFormType should show the login form and change data with a login id attributes', () => {
    const eventData = {
      target: {
        id: 'login-btn'
      }
    }
    vm.showingLoginForm = false
    vm.showingRegisterForm = true
    expect(vm.showingLoginForm).to.equal(false)
    expect(vm.showingRegisterForm).to.equal(true)
    vm.changeFormType(eventData)
    expect(vm.showingLoginForm).to.equal(true)
    expect(vm.showingRegisterForm).to.equal(false)
  })

  it('changeFormType should show the register form and change data with a register id attributes', () => {
    const eventData = {
      target: {
        id: 'register-btn'
      }
    }
    vm.showingLoginForm = true
    vm.showingRegisterForm = false
    expect(vm.showingLoginForm).to.equal(true)
    expect(vm.showingRegisterForm).to.equal(false)
    vm.changeFormType(eventData)
    expect(vm.showingLoginForm).to.equal(false)
    expect(vm.showingRegisterForm).to.equal(true)
  })

  it('changeFormType should not change data if an invalid id is passed', () => {
    const eventData = {
      target: {
        id: 'this-id-does-not-exist'
      }
    }
    vm.showingLoginForm = true
    vm.showingRegisterForm = false
    expect(vm.showingLoginForm).to.equal(true)
    expect(vm.showingRegisterForm).to.equal(false)
    vm.changeFormType(eventData)
    expect(vm.showingLoginForm).to.equal(true)
    expect(vm.showingRegisterForm).to.equal(false)
  })
})

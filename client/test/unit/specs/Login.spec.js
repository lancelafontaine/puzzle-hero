import Vue from 'vue'
import Login from '@/components/Login'

describe('Login.vue', () => {
  let vm

  beforeEach(() => {
    const Constructor = Vue.extend(Login)
    vm = new Constructor().$mount()
  })

  it('should render the form buttons', () => {
    expect(vm.$el.querySelector('#login-form-submit').value).to.equal('Submit')
  })

  it('should have default data', () => {
    expect(vm.email).to.equal('competitions.scs@ecaconcordia.ca')
  })
})

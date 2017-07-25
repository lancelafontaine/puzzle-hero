import Vue from 'vue'
import Navbar from '@/components/Navbar'
import Global from '@/global'

describe('Navbar.vue', () => {
  it('should render the title in the navbar', () => {
    const Constructor = Vue.extend(Navbar)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.navbar-text h2').textContent)
      .to.equal('Puzzle Hero')
  })

  it('should prompt to login if not logged in', () => {
    Global.isLoggedIn = false
    const Constructor = Vue.extend(Navbar)
    const vm = new Constructor().$mount()
    expect(vm.loginMessage).to.equal('')
  })

  it('should welcome user if logged in', () => {
    Global.isLoggedIn = true
    const Constructor = Vue.extend(Navbar)
    const vm = new Constructor().$mount()
    expect(vm.loginMessage).to.equal('Welcome!')
  })
})


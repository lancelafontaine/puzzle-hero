import Vue from 'vue'
import Navbar from '@/components/Navbar'

describe('Navbar.vue', () => {
  it('should render the title in the navbar', () => {
    const Constructor = Vue.extend(Navbar)
    const vm = new Constructor().$mount()
    expect(vm.$el.querySelector('.navbar-text h2').textContent)
      .to.equal('Puzzle Hero')
  })
})


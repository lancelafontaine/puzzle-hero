import Vue from 'vue'
import Challenges from '@/components/Challenges'
import global from '@/global'

describe('Challenges.vue', () => {
  let Constructor
  let vm

  beforeEach(() => {
    Constructor = Vue.extend(Challenges)
    vm = new Constructor().$mount()
  })

  it('should have default data', () => {
    Constructor = Vue.extend(Challenges)
    vm = new Constructor()

    expect(vm.challenges).to.be.a('array')
    expect(vm.NUMBER_OF_COLUMNS).to.be.a('number')
    expect(vm.global).to.be.a('object')
    expect(vm.categoryFilter).to.equal('')
    expect(vm.solvedFilter).to.equal('')

    expect(vm.categories).to.be.a('array')
  })

  it('should call initialization functions on component mount', () => {
    Constructor = Vue.extend(Challenges)
    vm = new Constructor()

    global.ensureLoggedIn = sinon.spy()

    expect(global.ensureLoggedIn.calledOnce).to.be.false
    vm = vm.$mount()
    expect(global.ensureLoggedIn.calledOnce).to.be.true
  })

  it('should initialize categories based on the obtained challenges', () => {
    Constructor = Vue.extend(Challenges)
    vm = new Constructor()

    vm.challenges = [
      {category: 'a'},
      {category: 'b'},
      {category: 'c'}
    ]
    expect(JSON.stringify(vm.categories)).to.equal(JSON.stringify(['a', 'b', 'c']))
  })

  it('numberOfRows determines how many rows of challenges are required based on the number of columns', () => {
    vm.NUMBER_OF_COLUMNS = 3

    let challenges = Array(3).fill({})
    expect(vm.numberOfRows(challenges)).to.equal(1)

    challenges = Array(4).fill({})
    expect(vm.numberOfRows(challenges)).to.equal(2)

    challenges = Array(6).fill({})
    expect(vm.numberOfRows(challenges)).to.equal(2)

    challenges = Array(7).fill({})
    expect(vm.numberOfRows(challenges)).to.equal(3)
  })

  it('challengeIndexByCell determines the challenge index by row number and offset if the challenge exists', () => {
    vm.NUMBER_OF_COLUMNS = 3

    let rowNumber = 1
    let offset = 0
    let challenges = Array(3).fill({})
    expect(vm.challengeIndexByCell(rowNumber, offset, challenges)).to.equal(0)

    rowNumber = 1
    offset = 2
    challenges = Array(3).fill({})
    expect(vm.challengeIndexByCell(rowNumber, offset, challenges)).to.equal(2)

    rowNumber = 2
    offset = 0
    challenges = Array(6).fill({})
    expect(vm.challengeIndexByCell(rowNumber, offset, challenges)).to.equal(3)

    rowNumber = 2
    offset = 2
    challenges = Array(6).fill({})
    expect(vm.challengeIndexByCell(rowNumber, offset, challenges)).to.equal(5)

    rowNumber = 3
    offset = 2
    challenges = Array(6).fill({})
    expect(vm.challengeIndexByCell(rowNumber, offset, challenges)).to.be.undefined
  })

  it('challengesByCategory filters challenges by category', () => {
    vm.challenges = []
    let category = 'a'
    expect(JSON.stringify(vm.challengesByCategory(category))).to.equal('[]')

    vm.challenges = [
      {category: 'a'},
      {category: 'a'},
      {category: 'b'},
      {category: 'b'},
      {category: 'c'},
      {category: 'c'}
    ]
    category = 'doesntexist'
    expect(JSON.stringify(vm.challengesByCategory(category))).to.equal('[]')

    category = 'a'
    expect(JSON.stringify(vm.challengesByCategory(category))).to.equal(
      JSON.stringify([
        { category: 'a' },
        { category: 'a' }
      ])
    )
  })

  it('filterChallenges returns a boolean if a challenge property matches against an arbitrary filter', () => {
    const challenge = {category: 'a'}
    let categoryFilter = 'a'
    expect(vm.filterChallenges(challenge.category, categoryFilter)).to.be.true

    categoryFilter = ''
    expect(vm.filterChallenges(challenge.category, categoryFilter)).to.be.true

    categoryFilter = 'all'
    expect(vm.filterChallenges(challenge.category, categoryFilter)).to.be.true

    categoryFilter = 'does_not_exist'
    expect(vm.filterChallenges(challenge.category, categoryFilter)).to.be.false
  })
})

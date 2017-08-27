import global from '@/global'

describe('global.js', () => {
  it('should be able to call defaultUserError', () => {
    expect(global.defaultUserError).to.be.a('function')
    expect(global.defaultUserError({'something': 'went wrong'})).to.be.undefined
  })

  it('range returns an array of all integers between 0 and the upperBound', () => {
    expect(JSON.stringify(global.range(5))).to.equal(JSON.stringify([0, 1, 2, 3, 4]))
    expect(JSON.stringify(global.range(0))).to.equal(JSON.stringify([]))
    expect(JSON.stringify(global.range(-1))).to.be.undefined
  })
})

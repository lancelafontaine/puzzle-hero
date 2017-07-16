import global from '@/global'

describe('global.js', () => {
  it('should be able to call defaultUserError', () => {
    expect(global.defaultUserError).to.be.a('function')
    expect(global.defaultUserError({'something': 'went wrong'})).to.be.undefined
  })
})

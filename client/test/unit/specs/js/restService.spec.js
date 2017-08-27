import axios from 'axios'
import restService from '@/js/restService'

describe('restService.js', () => {
  it('slackUsers responds with an array of user objects upon success', () => {
    sinon.stub(axios, 'get').returns(Promise.resolve({
      status: 200,
      data: {
        ok: true,
        data: []
      }
    }))

    return restService.getSlackUsers().then((res) => {
      expect(res.status).to.equal(200)
      expect(JSON.stringify(res.data.data)).to.equal('[]')
    })
  })
})

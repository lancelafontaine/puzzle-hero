import axios from 'axios'
import config from '@/config'

export default {
  getSlackUsers () {
    return axios.get(config.serverBaseUrl + '/slack-users')
  },
  postVerifySlackEmail (userData) {
    return axios.post(config.serverBaseUrl + '/verify-slack-email', userData)
  }
}

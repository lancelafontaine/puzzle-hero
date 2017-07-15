import axios from 'axios'
import config from '@/config'

export default {
  slackUsers (cb) {
    axios.get(config.serverBaseUrl + '/slack-users')
      .then((res) => {
        if (cb) cb(res)
      })
      .catch((res) => {
        console.err(res)
      })
  }
}

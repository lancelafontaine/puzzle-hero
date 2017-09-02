import axios from 'axios'
import config from '@/config'

export default {
  getSlackUsers () {
    return axios.get(config.serverBaseUrl + '/slack-users')
  },
  postVerifySlackEmail (userData) {
    return axios.post(config.serverBaseUrl + '/verify-slack-email', userData)
  },
  getChallenges () {
    // TO DO: replace this mock
    return {
      challenges: [
        {
          name: 'Algo-Destruction',
          category: 'Algorithms',
          points: 200,
          number_of_solves: 10,
          question: {
            type: 'async', // possible values are "regex" or "async"
            description: 'binary search this thingy',
            hint: 'it needs to be sorted', // unsure if this is needed, can we jsut put in description?
            files: []
          },
          submissions: {
            state: 'unsolved', // possible values: 'unsolved', 'inreview' (only applicable if type: 'async'), or 'solved'
            attempts: [
              'FLAG_first_attempt',
              'FLAG_second_attempt',
              'FLAG_got_it_this_is_the_answer'
            ]
          }
        },
        {
          name: 'Hack me!',
          category: 'Security',
          points: 300,
          number_of_solves: 5,
          question: {
            type: 'regex', // possible values are "regex" or "async"
            description: 'a hard question',
            hint: 'sql injection', // unsure if this is needed, can we jsut put in description?
            files: [
              '/static/questions/1/bin.zip'
            ]
          },
          submissions: {
            state: 'solved', // possible values: 'unsolved', 'inreview' (only applicable if type: 'async'), or 'solved'
            attempts: [
              'FLAG_first_attempt',
              'FLAG_second_attempt',
              'FLAG_got_it_this_is_the_answer'
            ]
          }
        }
      ]
    }
  }
}

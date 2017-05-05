import globalState from './global';

export default new Vue({
  el: '#navbar',
  data: {
    local: {
      message: 'testing'
    },
    global: globalState
  }
});


<template>
  <div class="challenge">
    {{ challenge }}
  </div>
</template>

<script>
export default {
  name: 'challenge',
  data () {
    return {}
  },
  props: {
    challenge: {
      type: Object,
      required: true
    }
  },
  methods: {}
}
</script>

<style scoped>
</style>

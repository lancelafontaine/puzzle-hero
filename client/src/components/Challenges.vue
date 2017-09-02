<template>
  <div class="challenges">
    <div class="container">
      <div class="row">
        <div class="column challenges-header">
          <h1>Challenges</h1>
        </div>
      </div>
      <div class="row">
        <div class="column challenges-filters">
          <span>Filters</span>
          <div class="row">
            <div class="column">
              <select v-model="categoryFilter" class="challenges-category-filter">
                <option value="" disabled="disabled" selected="selected">Categories:</option>
                <option value="all">All categories</option>
                <template v-for="category in categories">
                  <option v-bind:value="category">{{ category }}</option>
                </template>
              </select>
            </div>
            <div class="column">
              <select v-model="solvedFilter" class="challenges-solved-filter">
                <option value="" disabled="disabled" selected="selected">Answer type:</option>
                <option value="all">All questions</option>
                <option value="unsolved">Unsolved</option>
                <option value="inreview">In Review</option>
                <option value="solved">Solved</option>
              </select>
            </div>
          </div>
        </div>
        <div class="column challenges-score">
          <div class="challenges-score-div">
            <span>Player Score:</span>
            <span>Team Score:</span>
          </div>
        </div>
      </div>
      <template v-for="category in categories">
        <div v-show="filterChallenges(category, categoryFilter)" class="challenges-category">
          <h2>{{category}}</h2>
          <template v-for="rowNumber in numberOfRows(challengesByCategory(category))">
            <div class="row">
              <template v-for="offset in global.range(NUMBER_OF_COLUMNS)">
                <div class="column">
                  <template v-if="challengeIndexByCell(rowNumber, offset, challengesByCategory(category)) < challengesByCategory(category).length">
                    <challenge v-show="filterChallenges(challengesByCategory(category)[challengeIndexByCell(rowNumber, offset, challengesByCategory(category))].submissions.state, solvedFilter)" :challenge="challengesByCategory(category)[challengeIndexByCell(rowNumber, offset, challengesByCategory(category))]"></challenge>
                    </template>
                </div>
              </template>
            </div>
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import restService from '@/js/restService'
import global from '@/global'
import Challenge from '@/components/Challenge'

export default {
  name: 'challenges',
  components: {
    'challenge': Challenge
  },
  data () {
    return {
      challenges: restService.getChallenges().challenges,
      NUMBER_OF_COLUMNS: 3,
      categoryFilter: '',
      solvedFilter: '',
      global
    }
  },
  mounted () {
    global.ensureLoggedIn()
  },
  computed: {
    categories () {
      return this.challenges.map(challenge => challenge.category)
    }
  },
  methods: {
    numberOfRows (challenges) {
      const numberOfChallenges = challenges.length
      if (numberOfChallenges % this.NUMBER_OF_COLUMNS === 0) {
        return numberOfChallenges / this.NUMBER_OF_COLUMNS
      }
      return Math.floor(numberOfChallenges / this.NUMBER_OF_COLUMNS) + 1
    },
    challengeIndexByCell (rowNumber, offset, challenges) {
      const index = ((rowNumber - 1) * this.NUMBER_OF_COLUMNS) + offset
      if (index < challenges.length) {
        return index
      }
    },
    challengesByCategory (category) {
      return this.challenges.filter(challenge => challenge.category === category)
    },
    filterChallenges (element, filter) {
      return element === filter || filter === '' || filter === 'all'
    }
  }
}
</script>

<style scoped>
  .challenges {
    margin-top: 60px;
  }
  .challenges-header {
    text-align: center;
  }
  .challenges-score-div {
    float: right;
  }
  .challenges-category {
    margin: 30px 0;
  }
</style>

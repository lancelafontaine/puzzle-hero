export default {
  range (upperBound) {
    if (upperBound >= 0) {
      return Array(upperBound).fill().map((x, i) => i)
    }
  },
  defaultUserError (obj) {
    console.log(obj)
    alert('Oops! Something wen\'t wrong. Please try again later')
  },
  ensureLoggedIn () {
    // TO DO, implement this based on authentication mechanism, and redirect to login page if not authenticated
  },
  isLoggedIn: false
}

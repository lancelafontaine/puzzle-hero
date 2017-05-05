import babel from 'rollup-plugin-babel';
import uglify from 'rollup-plugin-uglify';

export default {
  entry: 'src/js/main.js',
  plugins: [
    babel(),
    uglify()
  ],
  format: 'iife',
  moduleName: 'puzzle-hero'
};

const gulp = require('gulp');
const htmlmin = require('gulp-htmlmin');
const runSequence = require('run-sequence');
const sass = require('gulp-sass');
const concat = require('gulp-concat');
const cleanCSS = require('gulp-clean-css');
const rollup = require('rollup-stream');
const source = require('vinyl-source-stream');
const connect = require('gulp-connect');

gulp.task('default', () => {
  runSequence(['html', 'sass', 'js'], ['serve', 'watch']);
});

gulp.task('html', () => {
  return gulp.src('src/index.html')
    .pipe(htmlmin({collapseWhitespace: true}))
    .pipe(gulp.dest('dist'))
    .pipe(connect.reload());
});

gulp.task('sass', () => {
  return gulp.src([
    'node_modules/milligram/dist/milligram.min.css',
    'node_modules/normalize.css/normalize.css',
    'src/css/main.scss'
  ])
    .pipe(sass().on('error', sass.logError))
    .pipe(concat('style.min.css'))
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(gulp.dest('dist'))
    .pipe(connect.reload());
});

gulp.task('js', () => {
  return rollup('rollup.config.js')
    .pipe(source('app.min.js'))
    .pipe(gulp.dest('dist'))
    .pipe(connect.reload());
});

gulp.task('serve', () => {
  connect.server({
    root: 'dist',
    livereload: true
  });
});

gulp.task('watch', () => {
  gulp.watch(['src/index.html'], ['html']);
  gulp.watch(['src/css/*.scss'], ['sass']);
  gulp.watch(['src/js/*.js'], ['js']);
});



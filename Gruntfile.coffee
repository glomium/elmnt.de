module.exports = (grunt) ->

  @initConfig


    pkg: grunt.file.readJSON "./package.json"


    # https://www.npmjs.com/package/grunt-contrib-clean
    clean: 
      all: [
        './layout/build',
      ]


    # https://www.npmjs.com/package/grunt-contrib-coffee
    coffee:
      options:
        bare: true
      compile:
        files:
          './layout/build/project.coffee.js': './layout/coffee.js'


    # https://www.npmjs.com/package/grunt-contrib-copy
    copy:
      js:
        files: [
          {
              expand: true
              cwd: 'bower_components'
              src: grunt.file.readJSON "./layout/bower_components.json"
              dest: 'media/js/'
              flatten: true
              filter: 'isFile'
          },
        ]


    # https://www.npmjs.com/package/grunt-contrib-uglify
    uglify:
      options:
        compress:
          warnings: false
        mangle: true
        preserveComments: /^!|@preserve|@license|@cc_on/i
      compile:
        src: grunt.file.readJSON "./layout/javascript.json"
        dest: './media/js/bootstrap.min.js'


    # https://www.npmjs.com/package/grunt-sass
    sass:
      compile:
        files:
          './layout/build/project.css': './layout/project.scss'


    autoprefixer:
      options:
        browsers: [
          'Android 2.3',
          'Android >= 4',
          'Chrome >= 35',
          'Firefox >= 31',
          'Explorer >= 9',
          'iOS >= 7',
          'Opera >= 12',
          'Safari >= 7.1'
        ]
      compile:
        src: [
          './layout/build/project.css',
        ]
        dest: './layout/build/prefixed.css'


    # https://www.npmjs.com/package/grunt-contrib-cssmin
    cssmin:
      compile:
        files:
          './media/css/bootstrap.min.css': './layout/build/prefixed.css'


    # https://www.npmjs.com/package/grunt-contrib-watch
    watch:
      js:
        files: ["./layout/project.coffee", "./layout/*.js", "./layout/javascript.json"]
        tasks: ["buildjs"]
      css:
        files: ["./layout/project.scss"]
        tasks: ["buildcss"]


  @loadNpmTasks "grunt-autoprefixer"
  @loadNpmTasks "grunt-contrib-clean"
  @loadNpmTasks "grunt-contrib-coffee"
  @loadNpmTasks "grunt-contrib-copy"
  @loadNpmTasks "grunt-contrib-cssmin"
  @loadNpmTasks "grunt-contrib-uglify"
  @loadNpmTasks "grunt-contrib-watch"
  @loadNpmTasks "grunt-sass"

  @registerTask "buildjs", ["coffee", "uglify"]

  @registerTask "buildcss", ["sass", "autoprefixer", "cssmin"]

  @registerTask "default", ["clean", "buildjs", "buildcss", "copy"]

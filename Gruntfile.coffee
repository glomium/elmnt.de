module.exports = ->

  @initConfig

    # https://www.npmjs.com/package/grunt-contrib-clean
    clean: 
      all: [
        'src/build',
      ]

    # https://www.npmjs.com/package/grunt-contrib-coffee
    coffee:
      options:
        bare: true
      compile:
        files:
          'src/build/project.coffee.js': 'src/coffee.js'


    # https://www.npmjs.com/package/grunt-contrib-uglify
    uglify:
      options:
        banner: ''
        compress:
          warnings: false
        mangle: true
        preserveComments: 'some'
      compile:
        src: [
          '../bootstrap/dist/js/bootstrap.min.js',
          'src/build/coffee.js',
          'src/project.js',
        ]
        dest: 'media/js/project.min.js'

    # https://www.npmjs.com/package/grunt-sass
    sass:
      compile:
        files:
          'src/build/project.css': 'src/project.scss'

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
          'src/build/project.css',
        ]
        dest: 'src/build/prefixed.css'

    # https://www.npmjs.com/package/grunt-contrib-cssmin
    cssmin:
      compile:
        files:
          'media/css/project.min.css': 'src/build/prefixed.css'

    # https://www.npmjs.com/package/grunt-contrib-watch
    # watch:

  @loadNpmTasks "grunt-autoprefixer"
  @loadNpmTasks "grunt-contrib-clean"
  @loadNpmTasks "grunt-contrib-coffee"
  @loadNpmTasks "grunt-contrib-cssmin"
  @loadNpmTasks "grunt-contrib-uglify"
# @loadNpmTasks "grunt-contrib-watch"
  @loadNpmTasks "grunt-sass"

  @registerTask "buildjs", ["coffee", "uglify"]

  @registerTask "buildcss", ["sass", "autoprefixer", "cssmin"]

  @registerTask "default", ["clean", "buildjs", "buildcss"]

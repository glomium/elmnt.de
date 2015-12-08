module.exports = ->

  @initConfig

    # https://www.npmjs.com/package/grunt-contrib-clean
    clean: 
      all: [
        'src/project.coffee.js',
      ]

    # https://www.npmjs.com/package/grunt-contrib-sass
    # sass:

    # https://www.npmjs.com/package/grunt-contrib-watch
    # watch:

    # https://www.npmjs.com/package/grunt-contrib-uglify
    uglify:
      options:
        banner: 'banner'
        compress:
          warnings: false
        mangle: true
        preserveComments: 'some'
      base:
        src: [
          'src/js/project.js',
          'src/js/project.coffee.js',
        ]
        dest: 'media/js/base.min.js'

    # https://www.npmjs.com/package/grunt-contrib-coffee
    coffee:
      options:
        bare: true
      compile:
        files:
          'src/project.coffee.js': 'src/project.coffee'

    autoprefixer:
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

# @loadNpmTasks "grunt-autoprefixer"
  @loadNpmTasks "grunt-contrib-clean"
  @loadNpmTasks "grunt-contrib-coffee"
# @loadNpmTasks "grunt-contrib-cssmin"
# @loadNpmTasks "grunt-contrib-sass"
  @loadNpmTasks "grunt-contrib-uglify"
# @loadNpmTasks "grunt-contrib-watch"

  @registerTask "default", ["clean:all", "coffee:compile", "uglify:base"]

module.exports = function(grunt) {

grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
        libs: {
            src: [
                'static/bower/angular/angular.min.js',
                'static/bower/angular-cookies/angular-cookies.min.js',
                'static/bower/angular-route/angular-route.min.js',
                'static/bower/angular-foundation/mm-foundation-tpls.min.js',
                'static/bower/jsTimezoneDetect/jstz.min.js',
                'static/bower/proso-apps-js/proso-apps-services.js',
                'static/foundation/js/vendor/jquery.js',
                'static/foundation/js/vendor/modernizr.min.js',
                'static/foundation/js/vendor/fastclick.js',
                'static/foundation/js/foundation.min.js'
            ],
            dest: 'static/dist/libs.min.js'
        },
        dist: {
            src: ['static/js/*.js', 'static/ng-parts/templates.js'],
            dest: 'static/dist/plant-challenge.js'
        }
    },
    uglify: {
        options: {
            banner: '/*! <%= pkg.name %>-libs <%= grunt.template.today("yyyy-mm-dd") %> */\n'
        },
        build: {
            src: 'static/dist/plant-challenge.js',
            dest: 'static/dist/plant-challenge.min.js'
        },
        foundation: {
            src: 'static/foundation/js/foundation.js',
            dest: 'static/foundation/js/foundation.min.js'
        }
    },
    jshint: {
        files: ['static/js/*.js']
    },
    watch: {
        files: ['static/js/*.js', "static/*.css"],
        tasks: ['jshint']
    },
    cssmin: {
        target: {
            files: {
                'static/dist/plant-challenge.min.css': [
                    'static/*.css',
                    "static/foundation/css/normalize.css",
                    "static/foundation/css/myfoundation.css"
                ]
            }
        }
    },
    ngtemplates:  {
        plantChallenge: {
            src: 'static/ng-parts/*.html',
            dest: 'static/ng-parts/templates.js'
        }
    }
});

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-angular-templates');

    grunt.registerTask('default', ['jshint', 'ngtemplates', 'concat', 'uglify:build', "cssmin"]);
    grunt.registerTask('foundation', ['uglify:foundation']);

};
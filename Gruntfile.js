module.exports = function(grunt) {

grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    concat: {
        libs: {
            src: [
                'static/foundation/js/vendor/jquery.js',
                'static/bower/angular/angular.min.js',
                'static/bower/angular-cookies/angular-cookies.min.js',
                'static/bower/angular-route/angular-route.min.js',
                'static/bower/angular-foundation/mm-foundation-tpls.min.js',
                'static/bower/angular-sanitize/angular-sanitize.min.js',
                'static/bower/jsTimezoneDetect/jstz.min.js',
                'static/bower/proso-apps-js/proso-apps-services.js',
                'static/bower/slick-carousel/slick/slick.js',
                'static/bower/angular-slick-carousel/dist/angular-slick.min.js',
                'static/foundation/js/vendor/modernizr.js',
                'static/foundation/js/vendor/fastclick.js',
                'static/foundation/js/foundation.min.js',
                'static/foundation/js/foundation/foundation.clearing.js'
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
        files: ['static/js/*.js', "static/*.css", "static/ng-parts/*.html"],
        tasks: ['jshint', 'ngtemplates', 'concat', 'uglify:build', "cssmin", "copy"]
    },
    cssmin: {
        target: {
            files: {
                'static/dist/plant-challenge.min.css': [
                    "static/foundation/css/normalize.css",
                    "static/foundation/css/myfoundation.css",
                    "static/bower/slick-carousel/slick/slick.css",
                    "static/bower/slick-carousel/slick/slick-theme.css",
                    'static/*.css'
                ]
            }
        }
    },
    ngtemplates:  {
        plantChallenge: {
            src: 'static/ng-parts/*.html',
            dest: 'static/ng-parts/templates.js'
        }
    },
    copy: {
        images: {
            cwd: 'static/imgs',  // set working folder / root to copy
            src: '**/*',           // copy all files and subfolders
            dest: 'static/dist/imgs',    // destination folder
            expand: true           // required when using cwd
        },
        fonts: {
            cwd: 'static/bower/slick-carousel/slick/fonts',  // set working folder / root to copy
            src: '**/*',           // copy all files and subfolders
            dest: 'static/dist/fonts',    // destination folder
            expand: true           // required when using cwd
        },
        loader: {
            cwd: 'static/bower/slick-carousel/slick',  // set working folder / root to copy
            src: 'ajax-loader.gif',           // copy all files and subfolders
            dest: 'static/dist',    // destination folder
            expand: true           // required when using cwd
        }
    }
});

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-angular-templates');
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['jshint', 'ngtemplates', 'concat', 'uglify:build', "cssmin", "copy"]);
    grunt.registerTask('foundation', ['uglify:foundation']);

};
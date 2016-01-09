angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.flashcards-practice","proso.apps.flashcards-userStats","proso.apps.user-user", "proso.apps.common-toolbar", "proso.apps.tpls"]);
var app = angular.module('plantChallenge', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps", "ngSanitize", "slickCarousel", "timer"]);

var MAX_GUESSES = 2;

app.config(["$httpProvider", function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.factory("global", function(){
    return {};
});

app.run(["$rootScope", "$location", "userService", "global", function ($rootScope, $location, userService, global) {
    $rootScope.$on('$routeChangeSuccess', function(){
        if (global.progress) {
            global.progress.active = false;
        }
        ga('send', 'pageview', $location.path());
    });

    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        var path = next.originalPath;
        var intro = ["/", "/intro", "/intro-final", "/login", "/practice"];
        var training = ["/training"];
        var contest = ["/contest", "/contest-closed"];

        if (userService.status.logged && intro.indexOf(path) !== -1 ){
            $location.path("/training");
            return;
        }
        if (!userService.status.logged && intro.indexOf(path) === -1 && path !== "/post-practice"){
            $location.path("/login");
            return;
        }
        if ((!userService.user.contest_open) && path !== "/contest-closed" && stringStartsWith(path, "/contest")){
            $location.path("/contest-closed");
            return;
        }
        if (training.indexOf(path) !== -1){
            global.section = "training";
        }else if (stringStartsWith(path, "/contest")){
            global.section = "contest";
        }else if (intro.indexOf(path) !== -1){
             delete global.section;
        }
    });
}]);

app.run(["configService", "userService", function(configService, userService){
    configService.processConfig(config);
    userService.processUser(user);
}]);

app.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');
    $routeProvider.
        when('/', {
            templateUrl: 'static/ng-parts/intro-1.html'
        }).
        when('/intro', {
            templateUrl: 'static/ng-parts/intro-2.html'
        }).
        when('/intro-final', {
            templateUrl: 'static/ng-parts/intro-final.html'
        }).
        when('/post-practice', {
            templateUrl: 'static/ng-parts/post-practice.html'
        }).
        when('/about', {
            templateUrl: 'static/ng-parts/about.html'
        }).
        when('/login', {
            templateUrl: 'static/ng-parts/auth.html',
            controller: "auth"
        }).
        when('/practice', {
            templateUrl: 'static/ng-parts/practice.html',
            controller: "practice"
        }).
        when('/practice/:id/:areaName', {
            templateUrl: 'static/ng-parts/practice.html',
            controller: "practice"
        }).
        when('/area-overview/:id/:areaName', {
            templateUrl: 'static/ng-parts/set-overview.html',
            controller: "setOverview"
        }).
        when('/training', {
            templateUrl: 'static/ng-parts/training.html',
            controller: "training"
        }).
         when('/contest-closed', {
            templateUrl: 'static/ng-parts/contest-closed.html'
        }).
        when('/contest', {
            templateUrl: 'static/ng-parts/contest-pending.html',
            controller: "contestPending"
        }).
        when('/contest/guesses', {
            templateUrl: 'static/ng-parts/contest-guesses.html',
            controller: "contestGuesses"
        }).
        when('/contest/leaderboard', {
            templateUrl: 'static/ng-parts/contest-leaderboard.html',
            controller: "contestLeaderboard"
        }).
        when('/contest/detail/:id', {
            templateUrl: 'static/ng-parts/contest-detail.html',
            controller: "contestDetail"
        }).
        when('/contest/about', {
            templateUrl: 'static/ng-parts/contest-about.html'
        }).
        otherwise({
            redirectTo: '/'
        });

        $locationProvider.html5Mode(true);
    }]);

app.controller("panelMenu", ["$scope", "global", "userService", "areas", function ($scope, global, userService, areas) {
    $scope.global = global;
    $scope.user = userService;
    $scope.areas = areas;
}]);

app.controller("panelAuth", ["$scope", "userService", "$location", "global", function ($scope, userService, $location, global) {
    $scope.user = userService;
    global.user = userService;
    $scope.$watch("user.status.logged", function(logged, o){
        if (logged && !o){
            $location.path("/training");
        }
        if(!logged && o){
            $location.path("/login");
        }
    });
}]);

app.controller("auth", ["$scope", "userService", function ($scope, userService) {
    $scope.user = userService;

    $scope.signUp = function(){
        userService.signupParams($scope.login.email, $scope.login.email, $scope.login.password, $scope.login.password2);
    };

    $scope.logIn = function(){
        userService.login($scope.login.email, $scope.login.password);
    };
}]);


app.directive('focusMe', ['$timeout', function($timeout) {
    return {
        scope: {
            trigger: '=focusMe'
        },
        priority: -1,
        link: function($scope, element) {
            $scope.$watch('trigger', function(value) {
                if (value) {
                    $timeout(function () { element[0].focus(); });
                }
            });
        }
    };
}]);

app.directive('plantSelect', ["$http", function($http){
    return {
        restrict: "E",
        scope: {
            model: '=',
            focus: '=',
            short: '=',
            all: '=',
            submit: '='
        },
        templateUrl: "static/ng-parts/plant-select.html",
        link: function($scope) {
            $scope.getPlantNames = function(val) {
                return $http.get($scope.short ? 'typehead-short' : $scope.all ? 'typehead-all' : 'typehead', {
                    params: {
                        search: val
                    }
                }).then(function(response){
                    $scope.typeheadHiddenCount = response.data.count;
                    return response.data.plants;
                });
            };

            $scope.searchGoogle = searchGoogle;
            $scope.openWeb = openWeb;
            $scope.webIcon = webIcon;
        }
    };
}]);

app.directive('keypressEvents', ["$document", "$rootScope", function ($document, $rootScope) {
    return {
        restrict: 'A',
        link: function () {
            $document.bind('keypress', function (e) {
                $rootScope.$broadcast('keypress', e, String.fromCharCode(e.which));
            });
        }
    };
}]);

app.directive('nextAction', [function() {
    return {
        scope: {
            condition: '=nextAction'
        },
        link: function ($scope, element) {
            $scope.$on('keypress', function (e, a, key) {
                if (a.keyCode === 13 && $scope.condition) {
                    angular.element(element).triggerHandler('click');
                }
            });
        }
    };
}]);


app.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
    var original = $location.path;
    $location.path = function (path, reload) {
        if (reload === false) {
            var lastRoute = $route.current;
            var un = $rootScope.$on('$locationChangeSuccess', function () {
                $route.current = lastRoute;
                un();
            });
        }
        return original.apply($location, [path]);
    };
}]);

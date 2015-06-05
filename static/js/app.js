angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.flashcards-practice","proso.apps.flashcards-userStats","proso.apps.user-user"]);
var app = angular.module('plantChallenge', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps"]);

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
        var contest = ["/contest"];

        if (userService.status.logged && intro.indexOf(path) !== -1 ){
            $location.path("/training");
            return;
        }
        if (!userService.status.logged && intro.indexOf(path) === -1 && path !== "/post-practice"){
            $location.path("/login");
            return;
        }
        if (training.indexOf(path) !== -1){
            global.section = "training";
        }else if (contest.indexOf(path) !== -1){
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
            when('/training', {
                templateUrl: 'static/ng-parts/training.html',
                controller: "training"
            }).
            when('/contest', {
                templateUrl: 'static/ng-parts/contest.html'
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


app.controller("postPractice", ["$scope", "global", "$location", function ($scope, global, $location) {
    if (!global.summary){
        $location.path("/training");
    }
    $scope.global = global;
    $scope.summary = global.summary;
}]);

app.controller("training", ["$scope", "$location", "global", "areas", function ($scope, $location, global, areas) {
    $scope.areas = areas;
    if (global.introFinished){
        $scope.showInfo = true;
        global.introFinished = false;
    }

    $scope.openArea = function (area) {
        $location.path("/practice/" + area.id + "/" + area.name);
    };

    areas.loadAreas();
    $scope.max = 10;
    $scope.dynamic = 7;

}]);


var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};

app.directive('focus', function(){
    return function(scope, element){
            element[0].focus();
    };
});
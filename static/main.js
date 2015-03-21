var app = angular.module('plantChallenge', ["ngCookies", "ngRoute"]);

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


app.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'static/ng-parts/welcome.html',
                controller: 'something'
            }).
            when('/home', {
                templateUrl: 'static/ng-parts/home.html',
                controller: 'something'
            }).
            when('/practice', {
                templateUrl: 'static/ng-parts/practice.html',
                controller: 'something'
            }).
            otherwise({
                redirectTo: '/'
            });

        $locationProvider.html5Mode(true);
    }]);

app.factory("Data", function ($cookies) {
    return {}
});

app.controller("something", function ($scope, $cookies, Data) {

});
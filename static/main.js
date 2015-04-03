var app = angular.module('plantChallenge', ["ngCookies", "ngRoute", "mm.foundation"]);

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


app.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider.
            when('/', {
                templateUrl: 'static/ng-parts/intro-1.html'
            }).
            when('/intro', {
                templateUrl: 'static/ng-parts/intro-2.html'
            }).
            when('/home', {
                templateUrl: 'static/ng-parts/home.html'
            }).
            when('/practice', {
                templateUrl: 'static/ng-parts/practice.html'
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
            otherwise({
                redirectTo: '/'
            });

        $locationProvider.html5Mode(true);
    }]);


app.controller("auth", function ($scope, $cookies) {

});

app.controller("practice", function ($scope, $http) {
    $scope.flashcard = {
        id: 1,
        term: {
            "lang":"en",
            "name":"Passiflora caerulea",
            "url":"http://en.wikipedia.org/wiki/Passiflora_caerulea",
            "object_type":"fc_term",
            "item_id":2134,
            "type":null,
            "id":2134
        },
        images: ["static/plants/plant1.jpg", "static/plants/plant2.jpg"],
        selected_image: "static/plants/plant1.jpg"
    };
    $scope.answer = {guesses: 0};

    $scope.submit = function(){
        if (!$scope.answer.term)
            return;
        $scope.answer.answered = true;
        $scope.answer.guesses++;
        $scope.answer.correct = $scope.answer.term.id == $scope.flashcard.term.id;
        if ($scope.answer.correct){
            $scope.answer.closed = true;
        }
    };

    $scope.getPlantNames = function(val) {
    return $http.get('typehead', {
        params: {
            input: val
        }
        }).then(function(response){
            return response.data.plants;
        });
    };
    $scope.search_google = function(plant){
        window.open('https://www.google.cz/search?&tbm=isch&q=' + plant.name);
    };
    $scope.open_web = function(plant){
        window.open(plant.url);
    };
});

app.directive('stopEvent', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attr) {
            element.bind('click', function (e) {
                e.stopPropagation();
            });
        }
    };
 });
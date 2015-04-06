var app = angular.module('plantChallenge', ["ngCookies", "ngRoute", "mm.foundation"]);

var MAX_GUESSES = 2;

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.service("authService", AuthService);


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
            when('/intro-final', {
                templateUrl: 'static/ng-parts/intro-final.html'
            }).
            when('/post-practice', {
                templateUrl: 'static/ng-parts/post-practice.html'
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

app.factory("PlantSet", function () {
    return {}
});


app.controller("auth", function ($scope, authService, $location) {
    $scope.auth = authService;

    $scope.sign_up = function(){
        authService.signup($scope.login.email, $scope.login.email, $scope.login.password, $scope.login.password);
    };

    $scope.$watch("auth.user.logged", function(n, o){
        if (n){
            $location.path("/intro-final")
        }
    });

    var update_profile = function() {
        $scope.$apply(authService.update_profile)
    };
});

app.controller("practice", function ($scope, $http, PlantSet, $location) {
    $scope.load_flashcards = function(){
        PlantSet.length = 5;
        PlantSet.corrects = 0;
        PlantSet.current = -1;
        PlantSet.progress = [null, null, null, null, null];
        PlantSet.name = "Plants";
        PlantSet.active = false;

        $http.get('flashcards/flashcards', {params: {db_orderby: "id"}})
            .success(function(response){
                $scope.flashcards = response.data.reverse();
                $scope.next_plant();
                PlantSet.active = true;
            });
    };

    $scope.save_answer = function(answer){
        PlantSet.progress[PlantSet.current] = {
            correct: answer.correct,
            name: $scope.flashcard.term.name
        };
        if (answer.correct)
            PlantSet.corrects.current++;
        console.log(answer);
    };

    $scope.next_plant = function(){
        PlantSet.current++;
        if (PlantSet.current >= PlantSet.length){
            $location.path("/post-practice");
            PlantSet.active = false;
            return;
        }
        $scope.answer = {guesses: 0};
        $scope.flashcard = $scope.flashcards.pop();
        $scope.flashcard.context.content = JSON.parse($scope.flashcard.context.content.split("'").join('"'));
        $scope.flashcard.selected_image = $scope.flashcard.context.content[0];
    };

    $scope.try_again = function(){
        $scope.answer.term = null;
        $scope.answer.answered = false;
    };

    $scope.skip = function(){
        $scope.answer.closed = true;
        $scope.answer.answered = true;
        $scope.answer.correct = false;
        $scope.save_answer($scope.answer);
    };

    $scope.submit = function(){
        if (!$scope.answer.term)
            return;
        $scope.answer.answered = true;
        $scope.answer.guesses++;
        $scope.answer.correct = $scope.answer.term.id == $scope.flashcard.term.id;
        if ($scope.answer.correct || $scope.answer.guesses >= MAX_GUESSES){
            $scope.answer.closed = true;
            $scope.save_answer($scope.answer);
        }
    };

    $scope.getPlantNames = function(val) {
    return $http.get('typehead', {
        params: {
            search: val
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

    $scope.load_flashcards();
});


app.controller("post-practice", function ($scope, PlantSet) {
    $scope.set = PlantSet;
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

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("authService").update_profile(element.scope());
};
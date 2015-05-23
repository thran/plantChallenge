angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.flashcards-practice","proso.apps.user-user"]);
var app = angular.module('plantChallenge', ["ngCookies", "ngRoute", "mm.foundation", "proso.apps"]);

var MAX_GUESSES = 2;

app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.factory("global", function(){
    return {};
});

app.run(function ($rootScope, $location, userService, global) {
    $rootScope.$on('$routeChangeSuccess', function(){
        ga('send', 'pageview', $location.path());
    });

    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        var path = next.originalPath;
        var intro = ["/", "/intro", "/intro-final", "/login"];
        var training = ["/training"];
        var contest = ["/contest"];

        if (userService.status.logged && intro.indexOf(path) !== -1 ){
            $location.path("/training");
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
});

app.run(function(configService, userService){
    configService.processConfig(config);
    userService.processUser(user);
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

app.factory("PlantSet", function () {
    return {}
});

app.controller("panelMenu", function ($scope, global, userService) {
    $scope.global = global;
    $scope.user = userService;
});

app.controller("panelAuth", function ($scope, userService) {
    $scope.user = userService;
});

app.controller("auth", function ($scope, userService, $location) {
    $scope.service = userService;

    $scope.sign_up = function(){
        userService.signupParams($scope.login.email, $scope.login.email, $scope.login.password, $scope.login.password);
    };

    $scope.$watch("service.status.logged", function(logged, o){
        if (logged){
            $location.path("/training")
        }else if(o){
            $location.path("/")
        }
    });
});

app.controller("practice", function ($scope, $http, PlantSet, $location, practiceService, global) {
    $scope.set = PlantSet;
    $scope.load_flashcards = function(){
        practiceService.initSet("intro");
        practiceService.setFilter({categories: ["intro_set"]});
        PlantSet.length = 5;
        PlantSet.corrects = 0;
        PlantSet.current = -1;
        PlantSet.progress = [null, null, null, null, null];
        PlantSet.name = "Plants";
        PlantSet.active = false;

        $scope.next_plant();
        PlantSet.active = true;
    };

    $scope.save_answer = function(answer){
        PlantSet.progress[PlantSet.current] = {
            correct: answer.correct,
            name: $scope.flashcard.term.name
        };
        if (answer.correct)
            PlantSet.corrects++;

        practiceService.saveAnswerToCurrentFC(
            answer.correct ? $scope.flashcard.id : null,
            (new Date).getTime() - answer.start_time,
            "guesses: " + answer.guesses
        );
    };

    $scope.next_plant = function(){
        practiceService.getFlashcard()
            .then(
            function(flashcard){
                PlantSet.current++;
                $scope.answer = {guesses: 0, start_time: (new Date).getTime()};
                $scope.flashcard = flashcard;
                $scope.flashcard.context.content = JSON.parse($scope.flashcard.context.content.split("'").join('"'));
                $scope.flashcard.selected_image = $scope.flashcard.context.content[0];
            }, function(msg){
                $location.path("/post-practice");
                global.introFinished = True;
                PlantSet.active = false;
            });
    };

    $scope.image_url = function(image, size){
        if (typeof image === "undefined"){
            return null;
        }
        return "http://images.flowerchecker.com/images/" + image + "-" + size;
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

app.controller("training", function ($scope, global) {
    if (global.introFinished){
        $scope.showInfo = true;
        global.introFinished = false;
    }

});

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};
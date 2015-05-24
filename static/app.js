angular.module("proso.apps", ["proso.apps.common-config","proso.apps.common-logging","proso.apps.flashcards-practice","proso.apps.flashcards-userStats","proso.apps.user-user"]);
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
        global.progress.active = false;
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

app.controller("panelMenu", function ($scope, global, userService) {
    $scope.global = global;
    $scope.user = userService;
});

app.controller("panelAuth", function ($scope, userService, $location, global) {
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
});

app.controller("auth", function ($scope, userService) {
    $scope.user = userService;

    $scope.sign_up = function(){
        userService.signupParams($scope.login.email, $scope.login.email, $scope.login.password, $scope.login.password);
    };
});

app.controller("practice", function ($scope, $http, $location, practiceService, global, $routeParams) {
    var area = parseInt($routeParams.id);
    var areaName = $routeParams.areaName;
    var progress = {};
    global.progress = progress;
    $scope.load_flashcards = function(){
        if (area){
            practiceService.initSet("common");
            practiceService.setFilter({categories: [area]});
        }else {
            practiceService.initSet("intro");
            practiceService.setFilter({categories: ["intro_set"]});
        }
        progress.active = true;
        progress.length = practiceService.getConfig().set_length;
        progress.current = -1;
        progress.tries = Array.apply(null, new Array(progress.length)).map(function(){return null})

        $scope.next_plant();
    };

    $scope.save_answer = function(answer){
        progress.tries[progress.current] = {correct: answer.correct};

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
                progress.current++;
                $scope.answer = {guesses: 0, start_time: (new Date).getTime()};
                $scope.flashcard = flashcard;
                $scope.flashcard.context.content = JSON.parse($scope.flashcard.context.content.split("'").join('"'));
                $scope.flashcard.selected_image = $scope.flashcard.context.content[0];
            }, function(msg){
                if (!area) {
                    global.introFinished = true;
                }
                global.summary = practiceService.getSummary();
                global.summary.area = area;
                global.summary.areaName = areaName;
                progress.active = false;
                $location.path("/post-practice");
            });
    };

    $scope.image_url = function(image, size){
        if (typeof image === "undefined"){
            return null;
        }
        return "http://images.flowerchecker.com/images/" + image + "-" + size;
    };

    $scope.try_again = function(){
        $scope.typeheadHiddenCount = null;
        $scope.answer.term = null;
        $scope.answer.answered = false;
    };

    $scope.skip = function(){
        $scope.typeheadHiddenCount = null;
        $scope.answer.closed = true;
        $scope.answer.answered = true;
        $scope.answer.correct = false;
        $scope.save_answer($scope.answer);
    };

    $scope.submit = function(){
        if (!$scope.answer.term)
            return;
        $scope.typeheadHiddenCount = null;
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
            $scope.typeheadHiddenCount = response.data.count;
            return response.data.plants;
        });
    };
    $scope.searchGoogle = function(plant){
        window.open('https://www.google.cz/search?&tbm=isch&q=' + plant.name);
    };
    $scope.openWeb = function(plant){
        window.open(plant.url);
    };

    $scope.webIcon = function(plant){
        if (!plant){ return }
        if (plant.url.match(/wikipedia/)) {
            return "wikipedia";
        }
        return "fi-web";
    };

    $scope.load_flashcards();
});

app.controller("postPractice", function ($scope, global, $location) {
    if (!global.summary){
        $location.path("/training");
    }
    $scope.global = global;
    $scope.summary = global.summary;
});

app.controller("training", function ($scope, $location, global, areas) {
    $scope.areas = areas;
    if (global.introFinished){
        $scope.showInfo = true;
        global.introFinished = false;
    }

    $scope.openArea = function (area) {
        $location.path("/practice/" + area.id + "/" + area.name);
    };

    areas.loadAreas();

});


app.factory("areas", function($http, userStatsService){
    var self = this;
    self.stats = {};

    self.loadAreas = function(){
        $http.get('/flashcards/categorys', {params:{ filter_column: "type", filter_value: "set"}})
            .success(function(response){
                self.areas = response.data;
                self.loadStats()
            }
        );
    };

    self.loadStats = function(){
        console.log("sa");
        self.areas.forEach(function(area){
            userStatsService.addGroup(area.id, {categories: [area.id]})
        });
        userStatsService.getStats().success(function(result){
            self.areas.forEach(function(area){
                area.stats = result.data[area.id];
            });
        })
    };

    return self;
});

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};

app.directive('focus', function(){
    return function(scope, element){
            element[0].focus();
    };
});
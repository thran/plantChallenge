app.service("contestService", ["$http", "$q", function ($http, $q) {
    var self = this;
    var deferred = null;

    var getData = function (){
        $http.get("/contest/data")
            .success(function(response){
                self.requests = response.requests;
                self.leaderboard = response.leaderboard;
                self.totalPoints = response.total_points;

                angular.forEach(self.requests, function(request){
                    request.time = response.request_lifetime - moment().diff(request.created, "seconds");
                });

                self.guesses = response.guesses;
                angular.forEach(self.guesses, function(guess) {
                    guess.request.time = response.request_lifetime - moment().diff(guess.request.created, "seconds");
                    guess.delay = moment.utc(guess.delay * 1000).format("HH:mm:ss");
                    guess.request.closed = guess.request.time < 0;
                    guess.status = guess.correct === "c" ? "Correct!" : guess.correct === "pc" ? "Almost!" : guess.correct === "i" ? "Disagreement" : "We are not sure";
                    guess.request.guess = guess;
                });
                deferred.resolve(self);
            });
    };

    self.getData = function () {
        if (!deferred){
            deferred = $q.defer();
        }
        if (!self.requests){
            getData();
        }
        return deferred.promise;
    };

    self.makeGuess = function (request) {
         return $http.post("contest/make_guess", request.guess)
            .success(function(response){
                request.guess.new = false;
                request.guess.request = request;
                self.guesses.unshift(request.guess);
            });
    };
}]);

app.controller("contestPanel", ["$scope", "$location", "contestService", function ($scope, $location, contestService){
    contestService.getData().then(function (data) {
        $scope.totalPoints = data.totalPoints;
    });
    if ($location.path() === "/contest"){
        $scope.page = "contest";
    }
    if ($location.path() === "/contest/guesses"){
        $scope.page = "guesses";
    }
    if ($location.path() === "/contest/leaderboard"){
        $scope.page = "leaderboard";
    }
}]);

app.controller("contestGuesses", ["$scope", "contestService", "$interval", function ($scope, contestService, $interval){
    var SLICK_SPEED = 3000;
    $scope.requestsPerPage = 15;
    $scope.currentPage = 1;
    $scope.image_url = image_url;

    contestService.getData().then(function (data) {
        $scope.guesses = data.guesses;
        $interval(function () {
            $("slick").eq(Math.floor(Math.random() * $scope.requestsPerPage)).slick('slickNext');
        }, SLICK_SPEED);
    });

    $scope.slickConfig = {
        dots: true,
        autoplay: false,
        arrows: false
    };
}]);

app.controller("contestDetail", ["$scope", "contestService", "$routeParams", function ($scope, contestService,  $routeParams){
    var id = parseInt($routeParams.id);
    $scope.image_url = image_url;
    $scope.searchGoogle = searchGoogle;
    $scope.openWeb = openWeb;
    $scope.webIcon = webIcon;

    contestService.getData().then(function (data) {
        angular.forEach(data.requests, function (request, i) {
            if (request.id === id){
                $scope.request = request;
                request.selectedImage = request.images[0];
                if (!request.guess){
                    request.guess = {
                        request: request.id,
                        new: true
                    };
                }
                if (i > 0) {
                    $scope.previous = data.requests[i - 1].id;
                }
                if (i < data.requests.length - 1) {
                    $scope.next = data.requests[i + 1].id;
                }
            }
        });
        if ($scope.request){
            return;
        }
        angular.forEach(data.guesses, function (guess, i) {
            if (guess.request.id === id){
                $scope.request = guess.request;
                guess.request.selectedImage = guess.request.images[0];
            }
        });
    });

    $scope.submit = function(){
        contestService.makeGuess($scope.request);
    };
}]);

app.controller("contestLeaderboard", ["$scope", "contestService", "$routeParams", function ($scope, contestService,  $routeParams){
    contestService.getData().then(function (data) {
        $scope.leaderboard = data.leaderboard;
    });
}]);


app.controller("contestPending", ["$scope", "contestService", "$interval", function ($scope, contestService, $interval){
    var SLICK_SPEED = 3000;
    $scope.requestsPerPage = 15;
    $scope.currentPage = 1;

    $scope.image_url = image_url;
    $scope.searchGoogle = searchGoogle;
    $scope.openWeb = openWeb;
    $scope.webIcon = webIcon;

    $scope.slickConfig = {
        dots: true,
        autoplay: false,
        arrows: false
    };

    contestService.getData().then(function (data) {
        $scope.requests = data.requests;
        $interval(function () {
            $("slick").eq(Math.floor(Math.random() * $scope.requestsPerPage)).slick('slickNext');
        }, SLICK_SPEED);
    });

}]);
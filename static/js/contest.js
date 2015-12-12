
app.controller("contest", ["$scope", "$http", "$location", "$interval", "$routeParams", function ($scope, $http, $location, $interval, $routeParams){
    var id = parseInt($routeParams.id);
    var SLICK_SPEED = 3000;
    $scope.requestsPerPage = 15;
    $scope.currentPage = 1;

    var getRequests = function (){
        $http.get("/contest/requests")
            .success(function(response){
                $scope.requests = response.requests;

                angular.forEach($scope.requests, function(request){
                    request.time = response.request_lifetime - moment().diff(request.created, "seconds");
                    if (request.id === id){
                        $scope.goToDetail(request);
                    }
                });

                $interval(function () {
                    $("slick").eq(Math.floor(Math.random() * $scope.requestsPerPage)).slick('slickNext');
                }, SLICK_SPEED);

                $scope.guesses = response.guesses;
                angular.forEach($scope.guesses, function(guess) {
                    guess.request.time = response.request_lifetime - moment().diff(guess.request.created, "seconds");
                    guess.delay = moment.utc(guess.delay * 1000).format("HH:mm:ss");
                    guess.request.closed = guess.request.time < 0;
                    guess.status = guess.correct === "c" ? "Correct!" : guess.correct === "pc" ? "Almost!" : guess.correct === "i" ? "Wrong" : "We are not sure";
                    guess.request.guess = guess;
                });
            });
    };

    $scope.image_url = image_url;

    $scope.slickConfig = {
        dots: true,
        autoplay: false,
        arrows: false
    };

    $scope.goToDetail = function(request){
        $scope.selectedRequest = request;
        request.selectedImage = request.images[0];
        id = request.id;
        if (!request.guess){
            request.guess = {
                request: request.id,
                new: true
            };
        }
        $location.path("/contest/"+request.id, false);
    };

    $scope.goToOverview = function(request){
        $scope.selectedRequest = null;
        id = null;
        $location.path("/contest", false);
    };

    $scope.submit = function(){
        var request = $scope.selectedRequest;
        $http.post("contest/make_guess", request.guess)
            .success(function(response){
                request.guess.new = false;
            });
    };

    $scope.searchGoogle = searchGoogle;
    $scope.openWeb = openWeb;
    $scope.webIcon = webIcon;

    getRequests();

}]);
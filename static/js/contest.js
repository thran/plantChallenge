
app.controller("contest", ["$scope", "$http", "$location", "$interval", "$routeParams", function ($scope, $http, $location, $interval, $routeParams){
    var id = parseInt($routeParams.id);
    var SLICK_SPEED = 1000;
    $scope.requestsPerPage = 15;
    $scope.currentPage = 1;

    if (false){
        $location.path("/contest-closed");
    }

    var get_requests = function (){
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

    get_requests();

}]);
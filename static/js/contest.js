
app.controller("contest", ["$scope", "$http", "$location", "$interval", function ($scope, $http, $location, $interval){
    var SLICK_SPEED = 1000;
    $scope.requestsPerPage = 15;
    $scope.currentPage = 1;

    var get_requests = function (){
        $http.get("/contest/requests")
            .success(function(response){
                $scope.requests = response.requests;

                angular.forEach($scope.requests, function(request){
                    request.time = response.request_lifetime - moment().diff(request.created, "seconds");
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

    $scope.select = function(request){
        $scope.selectedRequest = request;
    };


    get_requests();

}]);
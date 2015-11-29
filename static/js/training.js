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

app.controller("practice", ["$scope", "$http", "$location", "practiceService", "global", "$routeParams", "areas",
    function ($scope, $http, $location, practiceService, global, $routeParams, areas) {
    var area = parseInt($routeParams.id);
    var areaName = area ? $routeParams.areaName : "Intro set";
    var progress = {};
    areas.setActive(area);
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
        progress.tries = Array.apply(null, new Array(progress.length)).map(function(){return null;});

        $scope.next_plant();
    };

    $scope.save_answer = function(answer){
        progress.tries[progress.current] = {correct: answer.correct};
        if (answer.correct){
            areas.correctAnswer();
        }

        practiceService.saveAnswerToCurrentFC(
            answer.correct ? $scope.flashcard.id : null,
            (new Date()).getTime() - answer.start_time,
            "guesses: " + answer.guesses
        );
    };

    $scope.next_plant = function(){
        practiceService.getFlashcard()
            .then(
            function(flashcard){
                progress.current++;
                $scope.answer = {guesses: 0, start_time: (new Date()).getTime()};
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

    $scope.image_url = image_url;

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
        if (!$scope.answer.term) {
            return;
        }
        $scope.typeheadHiddenCount = null;
        $scope.answer.answered = true;
        $scope.answer.guesses++;
        $scope.answer.correct = $scope.answer.term.id === $scope.flashcard.term.id;
        if ($scope.answer.correct || $scope.answer.guesses >= MAX_GUESSES){
            $scope.answer.closed = true;
            $scope.save_answer($scope.answer);
        }
    };

    $scope.searchGoogle = searchGoogle;
    $scope.openWeb = openWeb;
    $scope.webIcon = webIcon;

    $scope.load_flashcards();
}]);

app.controller("postPractice", ["$scope", "global", "$location", "$timeout", function ($scope, global, $location, $timeout) {
    if (!global.summary){
        $location.path("/training");
        return;
    }
    $scope.global = global;
    $scope.summary = global.summary;
    $scope.image_url = image_url;

    $scope.selectFlashcard = function(flashcard){
        $scope.slickReady = false;
        $scope.selectedFlashcard = flashcard;
        $timeout(function(){$scope.slickReady = true;});
    };
    $scope.selectFlashcard($scope.summary.flashcards[0]);

    $scope.slickConfig = {
        dots: true,
        autoplay: true,
        autoplaySpeed: 3000,
        method: {}
    };

}]);

app.controller("setOverview", ["$scope", "$routeParams", "areas", "$timeout", function ($scope, $routeParams, areas, $timeout) {
    $scope.id = parseInt($routeParams.id);
    $scope.areaName = $routeParams.areaName;
    areas.getOverview($scope.id);
    $scope.overviews = areas.areaOverview;

    $scope.image_url = image_url;
    $scope.$watch("overviews", function(n, o) {
        if (n) {
            $timeout(function () {
                $(document).foundation('clearing');
            });
        }
    }, true);
}]);

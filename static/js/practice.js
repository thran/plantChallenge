
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

    $scope.getPlantNames = function(val) {
    return $http.get( $scope.flashcard.term.name.indexOf(" ") > -1 ? 'typehead' : 'typehead-short', {
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
        window.open(plant.external_url);
    };

    $scope.webIcon = function(plant){
        if (!plant){ return; }
        if (plant.external_url.match(/wikipedia/)) {
            return "wikipedia";
        }
        return "fi-web";
    };

    $scope.load_flashcards();
}]);
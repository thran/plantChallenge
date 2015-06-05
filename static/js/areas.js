
app.factory("areas", ["$http", "userStatsService", function($http, userStatsService){
    var self = this;

    self.loadAreas = function(){
        if (self.areas){
            self.loadStats();
            return;
        }
        return $http.get('/flashcards/categorys', {params:{ filter_column: "type", filter_value: "set"}})
            .success(function(response){
                self.areas = response.data;
                self.loadStats();
            }
        );
    };

    self.loadStats = function(){
        self.areas.forEach(function(area){
            userStatsService.addGroup(area.id, {categories: [area.id]});
        });
        userStatsService.getStats().success(function(result){
            self.areas.forEach(function(area){
                area.stats = result.data[area.id];
            });
            self.updateLevels();
        });
    };

    self.updateLevels = function(){
        var levelLimits = [0, 3, 10, 20, 50, 100, 200, 500, 1000, 10000];
        self.areas.forEach(function(area){
            for (var i=0; i < levelLimits.length; i++) {
                if (levelLimits[i] <= area.stats.number_of_correct_answers){
                    area.level = i;
                    area.nextLevelIn = levelLimits[i + 1] - area.stats.number_of_correct_answers;
                    area.inThisLevel = area.stats.number_of_correct_answers - levelLimits[i];
                    area.levelLength = levelLimits[i + 1] -levelLimits[i];
                }
            }
        });
    };

    self.setActive = function(areaId){
        if (!self.areas){
            self.loadAreas().success(function(){
               self.setActive(areaId);
            });
            return;
        }
        self.areas.forEach(function(area){
           if (area.id === areaId){
               self.active = area;
           }
        });
    };

    self.correctAnswer = function(){
        if (self.active){
            self.active.stats.number_of_correct_answers++;
            self.active.stats.number_of_answers++;
            self.updateLevels();
        }
    };

    return self;
}]);
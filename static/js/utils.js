function openPopup(url, next) {
    /* Open popup to Google or Facebook auth */

    var w = 700;
    var h = 500;
    var left = 100;
    var top = 100;

    var settings = 'height=' + h + ',width=' + w + ',left=' + left + ',top=' + top + ',resizable=yes,scrollbars=yes,toolbar=no,menubar=no,location=yes,directories=no,status=yes';
    url += "?next=" + next;

    window.open(url, "popup", settings);
}

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

app.directive('back', function(){
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('click', goBack);
            function goBack() {
                history.back();
                scope.$apply();
            }
        }
    };
});

var image_url = function(image, size){
    if (typeof image === "undefined"){
        return null;
    }
    return "http://images.flowerchecker.com/images/" + image + "-" + size;
};

var social_auth_callback = function(){
    var element = angular.element($("body"));
    element.injector().get("userService").loadUserFromJS(element.scope());
};


var searchGoogle = function(plant){
    window.open('https://www.google.cz/search?&tbm=isch&q=' + plant.name);
};

var openWeb = function(plant){
    window.open(plant.external_url);
};

var webIcon = function(plant){
    if (!plant){ return; }
    if (plant.external_url.match(/wikipedia/)) {
        return "wikipedia";
    }
    return "fi-web";
};
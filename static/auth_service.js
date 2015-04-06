AuthService = function($http){
    var user = this.user = {
        "logged": false
    };

    var _update_profile = function(){
        $http.get("user/profile/").success(function(data){
            user.logged = true;
            user.profile = data.data;
            user.name = data.data.user.username;
        });
    };

    var _reset_error = function(){
        user.error_msg = null;
        user.error_type = null;
    };

    this.signup = function(name, email, pass, pass2){
        _reset_error();
        $http.post("user/signup/", {
            "username": name,
            "email": email,
            "password": pass,
            "password_check": pass2
        }).success(function(){
            _update_profile()
        }).error(function(data){
            user.error_msg = data.error;
            user.error_type = data.error_type;
        });
    };

    this.login = function(){
        _reset_error();
    };


    this.logout = function(){
        $http.get("user/logout/").success(function(){
            user.logged = false;
            user.profile = null;
            user.name = null;
        });
    };

    _update_profile();
};
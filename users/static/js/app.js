/* Jquery definitions */
(function() {
    $('.piloting_request').click(function(e) {
        console.log('CLICKING!');
        e.preventDefault();
        $('.overlay').css('visibility','visible');
        $('.overlay').css('opacity','1');
    });
})();


/* Angular definitions */
(function(){
    var app = angular.module('fireStop', []);

    app.config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    
    }]);

    app.controller('SignupController', ['$scope', '$http', function($scope, $http) {
        $scope.data = {};

        $scope.submit_signup = function() {
            $http.post(SIGNUP_URL, $scope.data)
                 .success(function(data) {
                     $scope.signup.$setPristine(true);
                     $scope.data = {};
                 })
                 .error(function(data) {
                     console.log('NOT Success');
                 });
        }
    }])
})();

/* Jquery definitions */
var modal = (function($) {
    var close_modal = function() {
        $('.overlay').css('visibility','hidden');
        $('.overlay').css('opacity','0');
    }
    // Modal actions
    $('.close-modal').click(close_modal);

    $('.piloting_request').click(function(e) {
        e.preventDefault();

        $('.overlay').css('visibility','visible');
        $('.overlay').css('opacity','1');
    });

    $('.modal').click(function(e) {
        e.stopPropagation();
    });

    $('.overlay').click(close_modal);

    return {
        close: close_modal
    }
})(jQuery);


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
    }]);

    app.controller('PilotController', ['$scope', '$http', function($scope, $http) {
        $scope.data = {};
        $scope.submit_data = function() {
            console.log('submit data: %o', $scope.data);
            $http.post(PROFILE_URL, $scope.data)
                 .success(function(data) {
                     $scope.pilot.$setPristine(true);
                     $scope.data = {};
                     modal.close();
                 })
                 .error(function(data) {
                     //console.log('error: %o', data)
                 })
        }
    }]);
})();

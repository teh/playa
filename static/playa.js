app = angular.module('playa', [])


var PlaylistController = function($scope, $http) {
    $scope.src = null
    $scope.currentTitle = "No title"
    $http.get('/music').success(function(data) {
        $scope.playlist = data.songs
    })

    $scope.onPlay = function(path, title) {
        $scope.src = path
        $scope.currentTitle = title
        console.log(document.getElementById("audio"))
        setTimeout(function() {
            document.getElementById("audio").play()
        }, 5)
    }
}

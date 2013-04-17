app = angular.module('playa', [])

app.directive('audioControls', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            angular.element(element).bind('progress', function() {
            })
            angular.element(element).bind('ended', function() {
                scope.onNext()
                scope.$digest()
            })
        }
    }
})

var PlaylistController = function($scope, $http) {
    $scope.src = null
    $scope.currentTitle = "No title"
    $scope.playlist = []
    $http.get('/music').success(function(data) {
        $scope.playlist = data.songs
    })

    $scope.onPlay = function(path, title) {
        $scope.src = path
        $scope.currentTitle = title
        setTimeout(function() {
            document.getElementById("audio").play()
        }, 5)
    }

    $scope.onNext = function() {
        for (var i = 0; i < $scope.playlist.length; i++) {
            var e = $scope.playlist[i]
            if (e.title == $scope.currentTitle) {
                e = $scope.playlist[i + 1]
                $scope.onPlay(e.path, e.title)
                return
            }
        }
    }
}

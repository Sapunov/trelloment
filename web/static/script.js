let api_uri = `${location.protocol}//${location.hostname}:${location.port}/api`;

function BaseCtrl($scope) {

}

function BoardsCtrl($scope, $http) {
    $scope.boards = [];
    $scope.charts = {};

    function loadBoards() {
        $http.get(api_uri + '/boards').then(function(response) {
            $scope.boards = response.data;
            loadCharts();
        });
    }

    function extractAxis(data, chart_type) {
        var out = { labels: [], data: [], series: [chart_type] };

        for ( var i in data ) {
            out.labels.push(data[i][0]);
            out.data.push(data[i][1]);
        }

        return out;
    }

    function loadCharts(chart_type) {
        chart_type = chart_type || 'progress';

        for ( var i in $scope.boards ) {
            $http.get(api_uri + '/boards/' + $scope.boards[i].id + '/' + chart_type)
            .then(function(response) {
                $scope.charts[$scope.boards[i].id] = extractAxis(response.data, chart_type);
            });
        }
    }

    loadBoards();
}

function BoardCtrl($scope, $http, $routeParams) {

}

function CardCtrl($scope, $http, $routeParams) {

}

(function(){
    angular.module('trelloment', ['ngRoute', 'chart.js'])

    .controller('baseCtrl', BaseCtrl)
    .controller('boardsCtrl', BoardsCtrl)
    .controller('boardCtrl', BoardCtrl)
    .controller('cardCtrl', CardCtrl)

    .config(['$locationProvider', '$routeProvider',
        function config($locationProvider, $routeProvider) {
            $locationProvider.html5Mode(true);

            $routeProvider
            .when('/', {
                templateUrl: '/static/partials/boards.html',
                controller: 'boardsCtrl'
            })

            .when('/boards/:boardId', {
                templateUrl: '/static/partials/board.html',
                controller: 'boardCtrl'
            })

            .when('/cards/:cardId', {
                templateUrl: '/static/partials/card.html',
                controller: 'cardCtrl'
            })
        }
    ]);
})();

let api_uri = `${location.protocol}//${location.hostname}:${location.port}/api`;

function BaseCtrl($scope) {
    $scope.extractAxis = function(data, chart_type) {
        var out = { labels: [], data: [], series: [chart_type] };

        for ( var i in data ) {
            out.labels.push(data[i][0]);
            out.data.push(data[i][1]);
        }

        return out;
    }
}

function BoardsCtrl($scope, $http) {
    $scope.boards = [];
    $scope.charts = {};

    function loadBoards() {
        $http.get(api_uri + '/boards').then(function(response) {
            $scope.boards = response.data;
        });
    }

    loadBoards();
}

function BoardCtrl($scope, $http, $routeParams) {
    let boardId = $routeParams.boardId;

    $scope.board = {};

    $scope.cards_todo = [];
    $scope.cards_done = [];

    $scope.chart = {};
    $scope.chart_type = 'progress';

    function loadBoardCards() {
        $http.get(api_uri + '/boards/' + boardId + '/cards').then(function(response) {
            for ( var i in response.data ) {
                if ( response.data[i].is_completed ) {
                    $scope.cards_done.push(response.data[i]);
                } else {
                    $scope.cards_todo.push(response.data[i]);
                }
            }
        });
    }

    function loadBoard() {
        $http.get(api_uri + '/boards/' + boardId).then(function(response) {
            $scope.board = response.data;
            loadChart();
        });
    }

    function loadChart() {
        $http.get(api_uri + '/boards/' + boardId + '/' + $scope.chart_type)
        .then(function(response) {
            $scope.chart = $scope.extractAxis(response.data, $scope.chart_type);
        });
    }

    loadBoard();
    loadBoardCards();
}

function CardCtrl($scope, $http, $routeParams) {
    let cardId = $routeParams.cardId;

    $scope.card = {};

    $scope.chart = {};
    $scope.chart_type = 'progress';

    function loadCard() {
        $http.get(api_uri + '/cards/' + cardId).then(function(response) {
            $scope.card = response.data;
            loadChart();
        });
    }

    function loadChart() {
        $http.get(api_uri + '/cards/' + cardId + '/' + $scope.chart_type)
        .then(function(response) {
            $scope.chart = $scope.extractAxis(response.data, $scope.chart_type);
        });
    }

    loadCard();
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

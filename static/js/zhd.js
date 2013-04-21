// Generated by CoffeeScript 1.6.2
(function() {
  var AddTrackCtrl, HomeCtrl, PlaylistCtrl, initTypeahead, youtubeSuggest;

  angular.module("zhd", []).config(function($routeProvider) {
    return $routeProvider.when("/", {
      controller: HomeCtrl,
      templateUrl: "/static/views/home.html"
    }).when("/:id", {
      controller: PlaylistCtrl,
      templateUrl: "/static/views/playlist.html"
    }).when("/:id/:query", {
      controller: AddTrackCtrl,
      templateUrl: "/static/views/add_track.html"
    }).otherwise({
      redirectTo: "/"
    });
  });

  HomeCtrl = function($scope, $http, $location) {
    console.log("homeCtrl");
    $scope.letsRock = function() {
      return alert("OPPA GANGNAM STYLE!!!");
    };
    return $scope.changeView = function(view) {
      console.log(view);
      $http.put('api/' + view + '/').then(function(response) {
        return console.log(response);
      });
      return $location.path(view);
    };
  };

  PlaylistCtrl = function($scope, $routeParams, $http, $location) {
    var playlistId;

    playlistId = $routeParams.id;
    $scope.playlistName = playlistId;
    $http.get("/static/daft-punk.json").success(function(data) {
      return $scope.tracks = data;
    }).error(function() {
      return alert('Error fetching the playlist :( Try to reload the page.');
    });
    $scope.playTrack = function(id) {
      return $scope.dz.player.playTracks([id]);
    };
    $scope.buildPlayer = function() {
      DZ.init({
        appId: '116267',
        channelUrl: 'http://developers.deezer.com/examples/channel.php',
        player: {
          container: 'player',
          onload: function() {}
        }
      });
      return $scope.dz = DZ;
    };
    $scope.initRdio = initRdio;
    $scope.initTypeahead = initTypeahead;
    return $scope.changeView = function(view) {
      console.log(view);
      return $location.path(view);
    };
  };

  youtubeSuggest = function(parsedResponse) {
    var datum, _i, _len, _ref, _results;

    _ref = parsedResponse[1];
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      datum = _ref[_i];
      _results.push(datum);
    }
    return _results;
  };

  initTypeahead = function() {
    return $('#playlist .typeahead').typeahead({
      name: 'suggestions',
      remote: {
        url: 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&json=t&q=%QUERY',
        dataType: 'jsonp',
        jsonpCallback: 'youtubeSuggest',
        cache: true,
        filter: youtubeSuggest
      },
      template: '<p><strong>{{value}}</strong></p>',
      engine: Hogan
    });
  };

  AddTrackCtrl = function($scope, $routeParams, $http) {
    var playlistId;

    playlistId = $routeParams.id;
    $scope.playlistName = playlistId;
    $scope.trackQuery = $routeParams.query;
    console.log("/api/" + playlistId + "/");
    $http.get("/api/" + playlistId + "/").success(function(data) {
      $scope.playlist = data;
      return console.log(data);
    }).error(function() {
      return alert('Error fetching the playlist :( Try to reload the page.');
    });
    $scope.fetchSongByName = function(name) {
      var self, url;

      url = "http://" + host + "/api/v4/song/search" + std_sim_params;
      self = this;
      return $.ajax({
        type: "GET",
        url: url,
        dataType: "jsonp",
        cache: true,
        data: {
          title: name,
          results: 20,
          format: "jsonp",
          sort: "song_hotttnesss-desc"
        },
        success: function(data) {
          console.log(data);
          $scope.$apply(function() {
            return $scope.tracks = data.response.songs;
          });
          console.log("done", $scope.tracks);
          return console.log($scope);
        }
      });
    };
    $scope.fetchSongByName($scope.trackQuery);
    return console.log($scope);
  };

}).call(this);

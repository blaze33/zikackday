# Configuration
angular.module("zhd", []).config ($routeProvider) ->

  # Routes
  $routeProvider.
    when("/",
      controller: HomeCtrl
      templateUrl: "/static/views/home.html"

    ).when("/:id",
      controller: PlaylistCtrl
      templateUrl: "/static/views/playlist.html"

    ).otherwise redirectTo: "/"


# Home controller
HomeCtrl = ($scope) ->
  $scope.letsRock = ->
    alert "OPPA GANGNAM STYLE!!!"


# Playlist controller
PlaylistCtrl = ($scope, $routeParams, $http) ->

  playlistId = $routeParams.id

  # Getting the playlist
  $scope.playlistName = playlistId

  # Fetching the tracks
  $http.get("/static/tracks.json").success( (data) ->
    $scope.tracks = data
  ).error( () ->
    alert('Error fetching the playlist :( Try to reload the page.')
  )

  # Playing a track
  $scope.playTrack = (id) ->
    $scope.dz.player.playTracks [id]


  # Initializing the player
  $scope.buildPlayer = () ->
    DZ.init
      appId  : '116267',
      channelUrl : 'http://developers.deezer.com/examples/channel.php',  
      player : {
        container : 'player',
        onload : () ->
      }
    $scope.dz = DZ



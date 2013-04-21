# Configuration
angular.module("zhd", []).config ($routeProvider) ->

  # Routes
  $routeProvider
    .when("/",
      controller: HomeCtrl
      templateUrl: "/static/views/home.html"

    ).when("/:id",
      controller: PlaylistCtrl
      templateUrl: "/static/views/playlist.html"

    ).when("/:id/:query",
      controller: AddTrackCtrl
      templateUrl: "/static/views/add_track.html"

    ).otherwise redirectTo: "/"


# Home controller
HomeCtrl = ($scope, $http, $location) ->
  console.log("homeCtrl")
  $scope.letsRock = ->
    alert "OPPA GANGNAM STYLE!!!"

  $scope.changeView = (view) ->
    console.log( view )
    $http.put( 'api/'+view+'/' )
      .then (response) -> console.log response
    $location.path(view) # path not hash


# Playlist controller
PlaylistCtrl = ($scope, $routeParams, $http, $location) ->

  playlistId = $routeParams.id

  # Getting the playlist
  $scope.playlistName = playlistId


  # Fetching the tracks
  $http.get("/static/daft-punk.json").success( (data) ->
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

  # Initializing the player
  $scope.initRdio = initRdio
  $scope.initTypeahead = initTypeahead

  # searching a new track to add
  $scope.changeView = (view) ->
    console.log( view )
    $location.path(view) # path not hash

youtubeSuggest = (parsedResponse) ->
  (datum for datum in parsedResponse[1])

initTypeahead = () ->
  $('#playlist .typeahead').typeahead(
    name: 'suggestions'
    remote:
      url: 'http://suggestqueries.google.com/complete/search?client=youtube&ds=yt&json=t&q=%QUERY'
      dataType: 'jsonp'
      jsonpCallback: 'youtubeSuggest',
      cache: true
      filter: youtubeSuggest
    template: '<p><strong>{{value}}</strong></p>'
    engine: Hogan
  )

# Add-a-track controller
AddTrackCtrl = ($scope, $routeParams, $http) ->

  playlistId = $routeParams.id
  $scope.playlistName = playlistId
  $scope.trackQuery = $routeParams.query

  # Fetching the playlist data
  console.log("/api/#{playlistId}/")
  $http.get("/api/#{playlistId}/").success( (data) ->
    $scope.playlist = data
    console.log(data)
  ).error( () ->
    alert('Error fetching the playlist :( Try to reload the page.')
  )

  # Fetching echonest data
  $scope.fetchSongByName = (name) ->
    url = "http://" + host + "/api/v4/song/search" + std_sim_params
    self = this
    $.ajax
      type: "GET"
      url: url
      dataType: "jsonp"
      cache: true # dont append timestamp
      data:
        title: name
        results: 20
        format: "jsonp"
        sort: "song_hotttnesss-desc"

      success: (data) ->
        console.log data
        $scope.$apply ->
          $scope.tracks = data.response.songs
        console.log "done", $scope.tracks
        console.log $scope



  $scope.fetchSongByName $scope.trackQuery
  console.log $scope

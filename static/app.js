(function(){

    var app = angular.module('scloud', [ ]);

    app.controller('StreamController', [ '$http' , function( $http ){  
        var stream = this;
        stream.tracks = [];
        $http.get('/get_tracks').success(function(data){
            stream.tracks = data.tracks;
        });

        this.play = function(stream_url){
            $http.post('/play_stream', { url : stream_url});
        }
    } ] );

})();

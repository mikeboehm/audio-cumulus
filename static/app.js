(function(){

    var app = angular.module('scloud', [ ]);

    app.controller('StreamController', [ '$http' , function( $http ){  
        var stream = this;
        stream.tracks = [];
        this.pagination = 'title';
        $http.get('/get_tracks').success(function(data){
            stream.tracks = data.tracks;
        });

        this.updatePagination = function(new_order){
            this.pagination = '-' + new_order;
        }
        this.play = function(stream_url){
            $http.post('/play_stream', { url : stream_url});
        }
    } ] );

})();

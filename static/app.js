(function(){

    var app = angular.module('scloud', [  ]).filter('duration', function() {
        return function(input) {
            var ms = input % 1000;
            s = (input - ms) / 1000;
            var secs = s % 60;
            s = (s - secs) / 60;
            var mins = s % 60;
            var hrs = (s - mins) / 60;

            return hrs + ':' + ("0" + mins).slice(-2) + ':' + ("0" + secs).slice(-2);
        }
    });

    app.controller('StreamController', [ '$http', '$sce', function( $http, $sce ){  

        this.pagination = '-date';
        var stream = this;
        stream.tracks = [];
        stream.embed_code = '';

        $http.get('/get_tracks').success(function(data){
            stream.tracks = data.tracks;
        });

        this.updatePagination = function(new_order){
            this.pagination = new_order;
        }
        this.play = function(stream_url){
            $http.post('/play_stream', { url : stream_url});
        }
        this.embed = function(stream_url){
            $http.post('/embedcode', { url : stream_url}).success(function(data){
                stream.embed_code = $sce.trustAsHtml('<div class="well well-lg">' + data + '</div>');
            });
        }
    } ] );

    app.controller('FavouritesController', [ '$http', '$sce', function( $http, $sce ){  

        this.pagination = '-date';
        var stream = this;
        stream.tracks = [];
        stream.embed_code = '';

        $http.get('/get_favourites').success(function(data){
            stream.tracks = data.tracks;
        });

        this.updatePagination = function(new_order){
            this.pagination = new_order;
        }
        this.play = function(stream_url){
            $http.post('/play_stream', { url : stream_url});
        }
        this.embed = function(stream_url){
            $http.post('/embedcode', { url : stream_url}).success(function(data){
                stream.embed_code = $sce.trustAsHtml('<div class="well well-lg">' + data + '</div>');
            });
        }
    } ] );

    app.controller('OthersController', [ '$http', '$sce', function( $http, $sce ){  

        this.pagination = '-date';
        var stream = this;
        stream.tracks = [];
        stream.embed_code = '';

        $http.get('/get_others_favourites').success(function(data){
            stream.tracks = data.tracks;
        });

        this.updatePagination = function(new_order){
            this.pagination = new_order;
        }
        this.play = function(stream_url){
            $http.post('/play_stream', { url : stream_url});
        }
        this.embed = function(stream_url){
            $http.post('/embedcode', { url : stream_url}).success(function(data){
                stream.embed_code = $sce.trustAsHtml('<div class="well well-lg">' + data + '</div>');
            });
        }
    } ] );

    app.controller('StopController', [ '$http', function( $http ){  
        this.stopPlaying = function(){
            $http.get('/stop')
        }
    } ] )

})();

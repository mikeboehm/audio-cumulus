(function(){

    var app = angular.module('scloud', [ ]).filter('duration', function() {
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

    app.controller('StreamController', [ '$http' , function( $http ){  
        var stream = this;
        stream.tracks = [];
        this.pagination = '-date';
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

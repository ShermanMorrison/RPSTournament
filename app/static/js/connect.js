var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/game');
//    socket.on('connect', function() {
//        console.log('Server says I connected!');
//    });
});

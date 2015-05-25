var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/game');
    socket.on('session', function(data) {
        console.log('My session id =' + data.sessionID);
    });
});

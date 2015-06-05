var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/game');
    socket.on('session', function(data) {
        alert('My session id =' + data.sessionID);
    });
    socket.on('joined', function(data) {
        alert('Server says + ' + data.sender + ' connected!');
    });
});

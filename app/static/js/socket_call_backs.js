var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/game');
    socket.on('session', function(data) {
//        alert('My session id =' + data.sessionID);
    });
    socket.on('joined', function(data) {
//        alert('Server says + ' + data.sender + ' connected!');
    });
    socket.on('challengeRequest', function(data){
        $("#challenger").text(data['sender']);
        $("#challengeModal").modal("show");
    });
    socket.on('challengeAccept', function(data) {
        $.post('/lobby', {type: 'joinGame', game_id: data['game_id'], id: data['id']});
    });
    socket.on('challengeDecline', function(data){
        $("#pendingModal").modal("hide");
    });
    socket.on('challengeCancel', function(data){
        $("#challengeModal").modal("hide");
    });
    socket.on('joinGame', function(data) {
        window.location.assign('/game/' + data['game_id']);
    });
});


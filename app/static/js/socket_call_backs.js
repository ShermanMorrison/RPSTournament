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
        $.post('/lobby', {type: 'joinGame', challenger: data['challenger'], challengee: data['challengee']});
    });
    socket.on('challengeDecline', function(data){
        $("#pendingModal").modal("hide");
    });
    socket.on('challengeCancel', function(data){
        $("#challengeModal").modal("hide");
    });
    socket.on('joinGame', function(data) {
        if (data['sender'] == name){

        }
        window.location.assign('/game');
    });
});


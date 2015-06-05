$(document).ready(function(){
    window.onunload = exitLobby;

    function exitLobby(){

//        $.post('/lobby', {type: 'leaveLobby'});
          $.ajax({
            type: 'POST',
            url: '/lobby',
            data: {'type': 'leaveLobby'},
            async: false
          })
        return false;
    }
});


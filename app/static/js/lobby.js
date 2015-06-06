var accept;
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

    var bindUI = function(){
        //menu hover
        $('#userNav li').hover(
            function() {
                $('ul', this).slideDown("fast");
            },
            function() {
                $('ul', this).slideUp("fast");
            }
        );
        $('.listEntryChallenge').on("click", function(event){

            $("#challengee").text($(".user").text());
            $("#pendingModal").modal("show");

            var send_to = $(event.target).parents('#userEntry').find('.user').text();
            $.post('/lobby', {type: 'challenge', target: send_to, sender: name});

        })
    };

    var ready = function(){
        bindUI();
        accept = function(){
            $.post('/lobby', {type: 'challengeResponse', challenger: $('#challenger').text(), response: 'accept'});
        }
    }

    ready();
});


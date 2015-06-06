var accept, decline, cancel;
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

            $("#challengee").text($(event.target).parents('#userEntry').find('.user').text());
            $("#pendingModal").modal("show");

            var send_to = $(event.target).parents('#userEntry').find('.user').text();
            $.post('/lobby', {type: 'challenge', target: send_to, sender: name});

        })
    };

    var ready = function(){
        bindUI();
        accept = function(){
            $.post('/lobby', {type: 'challengeAccept', challenger: $('#challenger').text()});
        }
        decline = function(){
            $.post('/lobby', {type: 'challengeDecline', challenger: $('#challenger').text()});
        }
        cancel = function(){
            $.post('/lobby', {type: 'challengeCancel', challengee: $('#challengee').text()});
        }
    }

    ready();
});


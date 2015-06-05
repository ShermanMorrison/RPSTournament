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
        $('.listEntryChallenge').on("click", function(){
            $.post("/lobby", {type: 'challenge', target: $("#name").text(), sender: name});
        })
    };

    bindUI();
});


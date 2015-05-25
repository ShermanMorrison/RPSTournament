var accept;
$(document).ready(function(){
    (function(){


            socket.on('joined', function(data) {
                console.log('Server says + ' + data.sender + ' connected!');
            });
            socket.on('left', function(data) {
                console.log('Server says + ' + data.sender + ' left the game!');
            });
            socket.on('challengeRequest', function(data) {
                console.log('Server says + ' + data.sender + ' sent me a modal challenge!!');
                $('#challenger').html(data.sender);
                $('#challengeModal').modal('show');
            });
            socket.on('submittedMove', function(data) {
                console.log('Got a submittedMove message: ' + data.msg );
                if (data.msg && data.sender != name){
                    hideOthersOpp(images[data.msg]);
                    $(images[data.msg] + "Opp").toggle();
                }
            });
            socket.on('challengeResponse', function(data) {
                console.log('Got an acceptedChallenge message: ' + data.challenger);
                window.location.assign('/game');
            });

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

            var ready = function(){
                bindUI();
                accept = function(){
                    console.log("clicked accept");
                    $.post('/lobby', {type: 'challengeResponse', challenger: $('#challenger').text(), response: 'accept'});
                    window.location.assign('/game');
                }
            }

            ready();
    })();
});

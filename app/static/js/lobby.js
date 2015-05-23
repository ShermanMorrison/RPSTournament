$(document).ready(function(){
    (function(){


            socket.on('joined', function(data) {
                console.log('Server says + ' + data.sender + ' connected!');
            });
            socket.on('left', function(data) {
                console.log('Server says + ' + data.sender + ' left the game!');
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
            };

            var ready = function(){
                bindUI();
            }

            ready();
    })();
});

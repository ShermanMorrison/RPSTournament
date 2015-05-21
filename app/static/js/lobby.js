$(document).ready(function(){
    (function(){
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

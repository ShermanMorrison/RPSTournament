(function(){

    var bindUI = function(){
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
        console.log("Ready to run JS!");
        bindUI();
    }

//    $(function(){ready();});
    ready();
})();
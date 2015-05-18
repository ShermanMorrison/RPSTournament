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

var images = ["#rockImg","#paperImg","#scissorsImg"];

var hideOthers= function(index){
    for (i in images) {
        if (i != index){
            $(images[i]).hide();
        }
    }

}

var rock = function(){
    hideOthers(0);
    $("#rockImg").toggle();
};

var paper = function(){
    hideOthers(1);
    $("#paperImg").toggle();
};

var scissors = function(){
    hideOthers(2);
    $("#scissorsImg").toggle();
};
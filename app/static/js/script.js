console.log("in login script.js!");
var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log('Server says I connected!');
//        socket.emit('joined', {});
    });
    debugger;
});

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
            console.log("Ready to run JS!");
            bindUI();
        }

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

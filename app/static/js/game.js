var images, hideOthers, rock, paper, scissors, submit;
var move = -1;

$(document).ready(function(){
    images = ["#rockImg","#paperImg","#scissorsImg"];

    hideOthers= function(index){
        if (move == index)
            move = -1;
        else
            move = index;
        for (i in images) {
            if (i != index){
                $(images[i]).hide();
            }
        }
    }

    hideOthersOpp = function(index){
        if (move == index)
            move = -1;
        else
            move = index;
        for (i in images) {
            if (i != index){
                $(images[i] + "Opp").hide();
            }
        }
    }

    rock = function(){
        hideOthers(0);
        $("#rockImg").toggle();
    };

    paper = function(){
        hideOthers(1);
        $("#paperImg").toggle();
    };

    scissors = function(){
        hideOthers(2);
        $("#scissorsImg").toggle();

    };

    submit = function(){
        if (move >= 0 && move < 3){
            $.post("/game", {data: move});
            console.log("Sent post to submit move");
        }
        else{

            $('#display_submit').fadeIn(10);
            $('#display_submit').fadeOut(1000);
        }

    };


    // socket handlers
    socket.on('submittedMove', function(data) {
        console.log('Got a submittedMove message: ' + data.msg );
        if (data.msg){
            hideOthersOpp(images[data.msg]);
        }
         $(images[data.msg] + "Opp").toggle();
    });
});
var images, hideOthers, changeMove, rock, paper, scissors, submit;
var move = -1;

$(document).ready(function(){
    images = ["#rockImg","#paperImg","#scissorsImg"];

    hideOthers= function(index){
        for (i in images) {
            if (i != index){
                $(images[i]).hide();
            }
        }
    }

    hideOthersOpp = function(index){
        for (i in images) {
            if (i != index){
                $(images[i] + "Opp").hide();
            }
        }
    }


    rock = function(){
        move = 0;
    };

    paper = function(){
        move = 1;
    };

    scissors = function(){
        move = 2;
    };

    submit = function(){
        if (move >= 0 && move < 3){
            hideOthers(move);
            $(images[move]).toggle();
            $.post("/game", {data: move, sender: name});
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
        if (data.msg && data.sender != name){
            hideOthersOpp(images[data.msg]);
            $(images[data.msg] + "Opp").toggle();
        }

    });
});
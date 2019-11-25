(function() {
  var clearResizeScroll, conf, getRandomInt, insertI, lol;

  conf = {
    cursorcolor: "#696c75",
    cursorwidth: "4px",
    cursorborder: "none"
  };

  lol = {
    cursorcolor: "#cdd2d6",
    cursorwidth: "4px",
    cursorborder: "none"
  };


  clearResizeScroll = function() {
    $("#texxt").val("");
    $(".messages").getNiceScroll(0).resize();
    return $(".messages").getNiceScroll(0).doScrollTop(999999, 999);
  };


  insertI = function() {
    var innerText;
    innerText = $.trim($("#texxt").val());
    if (innerText !== "") {
      //$(".messages").append("<li class=\"i\"><div class=\"head\"><span class=\"time\">" + (new Date().getHours()) + ":" + (new Date().getMinutes()) + " AM, Today</span><span class=\"name\"> User </span></div><div class=\"message\">" + innerText +"hhhhh"+ "</div></li>");
      $(".messages").append(`
                    <li class="i">
                        <div class="head">
                        <span class="time"> ${(new Date().getHours())} : ${ (new Date().getMinutes())} Today</span>
                        <span class="name"> User </span></div><div class="message"> ${innerText}
                        </div>
                    </li>
                    `)

      clearResizeScroll();

      $.post( "/chatbot", {question:innerText},handle_response);
//      $.post( "/chatbot", {question:innerText}, handle_response);
      function handle_response(data) {
          // append the bot repsonse to the div
          $(".messages").append(`
                        <li class="friend-with-a-SVAGina">
                            <div class="head">
                            <span class="name"> BetaGo  </span>
                            <span class="time">  ${(new Date().getHours())} : ${(new Date().getMinutes())} Today</span>
                            </div><div class="message"> ${data['message']}
                            </div>
                        </li>
                        `)
          clearResizeScroll();
        }

//      $.ajax({
//			url: "/chatbot",
//			type: "POST",
//			data: {
//				'question':innerText,
//			},
//			dataType: "json",
//			success: function (data) {
//				console.log(data);
//				$(".messages").append("<li class=\"friend-with-a-SVAGina\"><div class=\"head\"><span class=\"name\">BetaGo  </span><span class=\"time\">" + (new Date().getHours()) + ":" + (new Date().getMinutes()) + " AM, Today</span></div><div class=\"message\">" + message['message'] + "</div></li>");
//              clearResizeScroll();
//			}
//
//		});

     }

    }

  $(document).ready(function() {
    $(".messages").niceScroll(lol);
    $("#texxt").keypress(function(e) {
      if (e.keyCode === 13) {
        insertI();
      }
    });
    return $(".send").click(function() {
      insertI();
    });
  });

}).call(this);
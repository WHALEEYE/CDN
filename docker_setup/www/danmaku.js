const timers = [];
const jqueryDom = createDanmaku('hihihi'); // test danmaku, delete it as you like
addInterval(jqueryDom);// test danmaku, delete it as you like

// Generate a WebSocket connection with the server
const ws = new WebSocket("ws://127.0.0.1:8765/");

// Called when WS is connected
ws.onopen = function() {
  console.log("on open");
  ws.send("open");
};

// Called when a WS message is received
ws.onmessage = function (event) {
    const received_msg = JSON.parse(event.data);
    console.log(received_msg);
    const jqueryDom = createDanmaku(received_msg.value);
    console.log(JSON.stringify(received_msg.value))
    addInterval(jqueryDom);
};

// Called when WS is closed
ws.onclose = function() {
  console.log("on close");
  ws.send("close")
};

// get the text in input area and send it to the server. Then clean up the input area.
$(".send").on("click", function () {
    const text = document.getElementById('danmakutext').value;
    ws.send(text)
    document.getElementById('danmakutext').value = "";
});

// create a Dom object corresponding to a danmaku
function createDanmaku(text) {
    const jqueryDom = $("<div class='bullet'>" + text + "</div>");
    const fontColor = "rgb(255,255,255)";
    const fontSize = "20px";
    let top = Math.floor(Math.random() * 400) + "px";
    const left = $(".screen_container").width() + "px";
    jqueryDom.css({
        "position": 'absolute',
        "color": fontColor,
        "font-size": fontSize,
        "left": left,
        "top": top,
    });
    $(".screen_container").append(jqueryDom);
    return jqueryDom;
}
// add timer task to let the danmaku fly from right to left
function addInterval(jqueryDom) {
    let left = jqueryDom.offset().left - $(".screen_container").offset().left;
    const timer = setInterval(function () {
        left--;
        jqueryDom.css("left", left + "px");
        if (jqueryDom.offset().left + jqueryDom.width() < $(".screen_container").offset().left) {
            jqueryDom.remove();
            clearInterval(timer);
        }
    }, 5); // set delay as 5ms,which means the danmaku changes its position every 5ms
    timers.push(timer);
}

window.onbeforeunload=function(e){
    ws.send("close")
    ws.close(1000)
    console.log("reload")
}
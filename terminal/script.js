var command = document.getElementById("cmd_line");
var commandArry = [];

var iframe = document.createElement("iframe");
iframe.className = "screen";
iframe.setAttribute("width", "100%");
iframe.setAttribute("height", 300);
iframe.setAttribute("frameborder", 0);
iframe.style.maxWidth = "450px";

var textarea = document.querySelector('textarea');
textarea.addEventListener('keydown', autosize);


// KEYBOARD EVENTS
var elem = document.getElementById("cmd_line");
elem.onkeyup = function(e) {
    if (e.keyCode == 13) { // ENTER
        let command_value = command.value.replace(/(\r\n|\n|\r)/gm, "");
        command_value = command_value.replace(/ +/g, ' ');
        if (command_value == "") {
            document.getElementById("cmd_line").value = "";
            document.getElementById("cmd_line").focus();
        } else {
            commandArry.push(command_value);
            i = commandArry.length;
            parse(command_value);
            document.getElementById("cmd_line").scrollIntoView();
        }
    } else if (e.keyCode == 38) { // UP
        if (i > 0) {
            i--;
            document.getElementById("cmd_line").value = commandArry[i];
        } else {
            document.getElementById("cmd_line").value = "";
        }
    } else if (e.keyCode == 40) { // DOWN
        if (i < commandArry.length) {
            document.getElementById("cmd_line").value = commandArry[i];
            i++;
        } else {
            document.getElementById("cmd_line").value = "";
        }
    }
}


// PARSE COMMAND
function parse(command_value) {
    let code = document.createElement("p");

    if (command_value == "exit") {
        exit();
    } else if (command_value == "clear") {
        clear();
    } else {
        code.className = "cmd";
        code.innerHTML = command_value + '<span class="comment"> ↵</span>';
        document.getElementById("terminal_screen").appendChild(code);

        if (command_value == "help") {
            help();
        } else if (command_value == "whoami") {
            whoami();
        } else if (command_value == "video -l" || command_value == "video list") {
            video_list();
        } else if (command_value.split(' ').slice(0, 2).join(' ') == "video -p" || command_value.split(' ').slice(0, 2).join(' ') == "video play") {
            video_play(command_value.split(' ').slice(2).join(' '));
        } else if (command_value == "ipconfig"){
            ipconfig();
        } else {
            code = document.createElement("p");
            code.className = "error";
            code.innerHTML = '"' + command_value + '" is not defined! <pre class="warning">';
            document.getElementById("terminal_screen").appendChild(code);
        }
    }
    cmd_clear();
}

function print(output){
    let p = document.createElement("p");
    p.innerHTML = output;
    document.getElementById("terminal_screen").appendChild(p);
}

// cmd function

function ipconfig(){
    $.ajax({
        url: "http://ip-api.com/json",
        async: false,
        dataType: "jsonp",
        jsonp: "callback",
        data: {
            "fields": "status,country,regionName,city,isp,query",
            "lang": "en"
        },
        success: function(data){
            let output = "Failed!";
            if (data.status == "success"){
                output = `IP: ${data.query} <br>ISP: ${data.isp} <br>Loc: ${data.city}, ${data.regionName}, ${data.country}`;
            }
            print(output);
        }
    })
}

function exit() {
    window.close();
    // alert("Exit!");
}

function clear() {
    var ps = document.getElementById("terminal_screen").querySelectorAll("*");
    var ps_length = ps.length;
    var i;
    for (i = ps_length - 1; i >= 0; i--) {
        ps[i].remove();
    }
}

function help() {
    code = document.createElement("div");
    code.innerHTML = `
    <p class="warning"><i class="fa fa-question-circle" aria-hidden="true"></i>
    These are common commands used in various situations:</p>
    <ul class="list">
        <li>whoami <span class="comment"> ............................ [Shows who am i]</span></li>
        <li>video list <span class="comment">or -l .................. [Lists all videos]</span></li>
        <li>video play &lsaquo;video_name&rsaquo; <span class="comment">or -p ..... [Plays selected video]</span></li>
        <li>clear <span class="comment"> ............................. [Clear screen]</span></li>
        <li>exit <span class="comment"> .............................. [Close current browser window]</span></li>
    </ul>
    <br>`;
    document.getElementById("terminal_screen").appendChild(code);
}

function whoami() {
    print(`<span class="error">♥</span> I am the [<span class="info">Terminal</span>] of ${window.location.host}.`);
}

function video_play(x) {

    $.getJSON("../video/data/playlist.json", function(data){
        let src = null;
        let title = null;
        for (let i=0; i<data.length; i++){
            if (data[i].number == x){
                src = data[i].src;
                title = data[i].title;
                iframe.setAttribute("src", src);
                break
            }
        }
        if (src){
            document.getElementById("terminal_screen").appendChild(iframe);
            print(`<span class="info">${title}</span> is playing...`);
        } else{
            print(`Invalid video number: <span class="error">${x}</span>!`);
        }
        
    })
}

function video_list() {
    $.getJSON("../video/data/playlist.json", function(data){
        let content = "";
        data.forEach(element => {
            content += `<li>${element.number} <span class="comment">${element.title}</span></li>`;
        });
        let output = `
        <p class="warning"><i class="fa fa-music" aria-hidden="true"></i>
        Here is the list</p>
        <ul class="list">${content}</ul>
        <p class="info">Use 'video -p &lsaquo;number&rsaquo;' command for playing the video...</p>
        <br>`
        print(output);
    })
}

function cmd_clear() {
    command.value = "";
}

/////////////////////////////////////////////////////

function autosize() {
    let el = this;
    setTimeout(function() {
        el.style.cssText = 'height:auto; padding:0';
        el.style.cssText = 'height:' + el.scrollHeight + 'px';
    }, 0);
}

function setFocus() {
    document.getElementById("cmd_line").focus();
}
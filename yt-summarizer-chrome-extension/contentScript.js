var url_yt;
function generateSummary(url_yt) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("summarized-text").innerHTML = this.responseText;
       }
    };
    req.open("GET", `http://localhost:5000/api/summarize?youtube_url=${url_yt}`, true);
    req.send();
    console.log("Running..");
}

var port = chrome.runtime.connect({name: 'summarizer'});      
port.onDisconnect.addListener(function(obj) {
  console.log('disconnected port');
});

chrome.runtime.onConnect.addListener(function(port) {
    port.onMessage.addListener(function(msg) {
        url_yt = msg.url;
        generateSummary(url_yt);
    });
});

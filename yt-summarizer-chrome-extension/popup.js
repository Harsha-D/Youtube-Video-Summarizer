var url_yt,button1 = document.getElementById("summarybutton"),button2 = document.getElementById("summarybutton1"),button3 = document.getElementById("summarybutton2");

function generateSummary(url_yt,x) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("summarized-text").innerHTML =
            this.responseText;
            document.getElementById("plswait").innerHTML = "";
       }
    };
    if(x==1){
        req.open("GET", `http://localhost:5000/api1/summarize1?youtube_url=${url_yt}`, true);
        req.send();
    }
    if(x==2){
        req.open("GET", `http://localhost:5000/api2/summarize2?youtube_url=${url_yt}`, true);
        req.send();
    }
    if(x==3){
        req.open("GET", `http://localhost:5000/api3/summarize3?youtube_url=${url_yt}`, true);
        req.send();
    }
    console.log("Running..");
}

button1.addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        url_yt = tabs[0].url;
        document.getElementById("plswait").innerHTML = "Fetching summary, please wait...";
        button1.style.display = 'none';
        button2.style.display = 'none';
        button3.style.display = 'none';
        var x=1;
        generateSummary(url_yt,x);
    });
}, false);
button2.addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        url_yt = tabs[0].url;
        document.getElementById("plswait").innerHTML = "Fetching summary, please wait...";
        button1.style.display = 'none';
        button2.style.display = 'none';
        button3.style.display = 'none';
        var x=2;
        generateSummary(url_yt,x);
    });
}, false);
button3.addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        url_yt = tabs[0].url;
        document.getElementById("plswait").innerHTML = "Fetching summary, please wait...";
        button1.style.display = 'none';
        button2.style.display = 'none';
        button3.style.display = 'none';
        var x=3;
        generateSummary(url_yt,x);
    });
}, false);

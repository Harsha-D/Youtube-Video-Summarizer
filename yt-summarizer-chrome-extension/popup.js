var url_yt,button = document.getElementById("summarybutton");
function generateSummary(url_yt) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("summarized-text").innerHTML =
            this.responseText;
            document.getElementById("plswait").innerHTML = "";
       }
    };
    req.open("GET", `http://localhost:5000/api/summarize?youtube_url=${url_yt}`, true);
    req.send();
    console.log("Running..");
}

button.addEventListener("click", function() {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
        url_yt = tabs[0].url;
        document.getElementById("plswait").innerHTML = "Fetching summary, please wait...";
        generateSummary(url_yt);
    });
}, false);
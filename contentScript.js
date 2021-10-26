// function pageRedirect(URL){
//     window.location.href = URL;
// }
function summarizeVideo(){
    YouTube_URL = window.location.href
    var res = YouTube_URL.split("=")[1]
    if(res.includes("&list")){
        res = res.split("&list")[0]
    }
    const URL = "http://127.0.0.1:5000/api/summarize/"+res
    console.log(URL)
    // pageRedirect(URL)
    fetch(URL).then((summary)=>{
        console.log(summary);
        return summary.json();
    }).then((data)=>{
        alert(data.Summary);
    }).catch((error)=>{
        console.log(error);
    })
}

chrome.runtime.onMessage.addListener(function(message){
    if(message.action === 'SUMMARY'){
        summarizeVideo();
    }
});
const summaryForm = document.getElementById("summary-form");
summaryForm.onsubmit = function(e){
    e.preventDefault();
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "SUMMARY"});
				window.close();
    });
}

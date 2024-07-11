chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action == "extract_text") {
    var text = document.body.innerText;
    sendResponse(text);
  }
});

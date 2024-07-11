chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg.action === "extract_data") {
    const position = document.querySelector('.app-title');
    const position_text: string = position ? (position as any).innerText : "";

    console.log(position)
    const company = document.querySelector<HTMLSpanElement>('.company-name');
    const company_text = company ? (company as any)?.innerText?.substring(3) : "";

    console.log(company)
    sendResponse({ position: position_text.trim(), company: company_text.trim() });
  } else {
    sendResponse("Unknown action.");
  }
});

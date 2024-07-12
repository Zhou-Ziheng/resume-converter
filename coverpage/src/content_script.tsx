chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
  if (msg.action === "extract_data") {
    if (window.location.href.includes("greenhouse.io")) {
      handleGreenhouse(sendResponse);
    } else if (window.location.href.includes("waterlooworks.uwaterloo.ca")) {
      handleWaterlooWorks(sendResponse);
    }

  } else {
    sendResponse("Unknown action.");
  }
});

const handleGreenhouse = (sendResponse: (response: any) => void) => {
  const position = document.querySelector('.app-title');
  const position_text: string = position ? (position as any).innerText : "";

  console.log(position)
  const company = document.querySelector<HTMLSpanElement>('.company-name');
  const company_text = company ? (company as any)?.innerText?.substring(3) : "";

  console.log(company)
  sendResponse({ position: position_text.trim(), company: company_text.trim() });

}

const handleWaterlooWorks = (sendResponse: (response: any) => void) => {
  const positionTableRow = findTableRowWithText("Job Title:");
  console.log(positionTableRow)
  const position = positionTableRow ? positionTableRow.querySelectorAll('td')?.[1] : null;
  const position_text = position ? (position as any).innerText : "";

  const companyTableRow = findTableRowWithText("Organization:");
  const company = companyTableRow ? companyTableRow.querySelectorAll('td')?.[1] : null;
  const company_text = company ? (company as any).innerText : "";

  sendResponse({ position: position_text.trim(), company: company_text.trim() });
}

const findTableRowWithText = (text: string) => {
  const rows = document.querySelectorAll('tr');
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    console.log(row.innerText)
    if (row.innerText.includes(text)) {
      return row;
    }
  }
  return null;
}
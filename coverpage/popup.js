// // // // // Inject the payload.js script into the current tab after the popout has loaded
// // // // window.addEventListener('load', function (evt) {
// // // // 	chrome.extension.getBackgroundPage().chrome.tabs.executeScript(null, {
// // // // 		file: 'payload.js'
// // // // 	});;
// // // // });

// // // // // Listen to messages from the payload.js script and write to popout.html
// // // // chrome.runtime.onMessage.addListener(function (message) {
// // // // 	document.getElementById('pagetitle').innerHTML = message;
// // // // });
// // // // popup.js (service worker)

// // // console.log('Service worker script loaded.');

// // // self.addEventListener('install', event => {
// // //   console.log('Service worker installed.');
// // // });

// // // self.addEventListener('activate', event => {
// // //   console.log('Service worker activated.');
// // // });

// // // self.addEventListener('fetch', event => {
// // //   console.log('Fetch intercepted for:', event.request.url);
// // //   // Handle fetch requests here if needed.
// // // });
// // // popup.js (service worker)

// // // Function to inject payload.js into the current tab
// // function injectPayloadScript() {
// //     chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
// //         // Query the active tab in the current window
// //         chrome.tabs.executeScript(tabs[0].id, { file: 'payload.js' }, function() {
// //         console.log('payload.js injected into the current tab');
// //         });
// //     });
// // }

// // // Inject payload.js when the popup.html has fully loaded
// // window.addEventListener('load', function() {
// //     injectPayloadScript();
// // });

// // // Listen to messages from payload.js
// // chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
// //     // Update popup.html with the message received from payload.js
// //     document.getElementById('pagetitle').innerHTML = message;
// // });
// // popup.js (service worker)

// // Function to inject payload.js into the current tab
// function injectPayloadScript() {
//   chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//     chrome.tabs.executeScript(tabs[0].id, { file: 'payload.js' }, function() {
//       console.log('payload.js injected into the current tab');
//     });
//   });
// }

// // Inject payload.js into the current tab when the extension is first loaded
// injectPayloadScript();

// // Listen to messages from payload.js
// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//   console.log('Message received from payload.js:', message);
//   // Update popup.html with the message received from payload.js
//   document.getElementById('pagetitle').textContent = message;
// });
// // popup.js (service worker)

// // Function to inject payload.js into the current tab
// function injectPayloadScript() {
//   chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//     chrome.tabs.executeScript(tabs[0].id, { file: 'payload.js' }, function() {
//       console.log('payload.js injected into the current tab');
//     });
//   });
// }

// // Inject payload.js into the current tab when the extension is first loaded
// injectPayloadScript();

// // Listen to messages from payload.js
// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//   console.log('Message received from payload.js:', message);
//   // Update popup.html with the message received from payload.js
//   document.getElementById('pagetitle').textContent = message;
// });
// popup.js

// Function to handle clicking the extension icon
chrome.action.onClicked.addListener((activeTab) => {
  chrome.extension.getBackgroundPage().console.log("smol vrooom");
  // Get active tab details
  // Ensure we have a valid tab and URL
  if (activeTab && activeTab.url) {
    // Check if the URL is http or https
    if (
      activeTab.url.startsWith("http://") ||
      activeTab.url.startsWith("https://")
    ) {
      // Inject content script to scrape job description
      chrome.scripting.executeScript(
        {
          target: { tabId: activeTab.id },
          function: scrapeJobDescription,
        },
        (results) => {
          // Handle results from scraping
          if (results && results.length > 0 && results[0].result) {
            let jobDescription = results[0].result;
            // Use the job description to generate the cover letter
            generateCoverLetter(jobDescription);
          } else {
            console.error("Failed to scrape job description");
          }
        }
      );
    } else {
      console.error("Invalid URL");
    }
  } else {
    console.error("No active tab found");
  }
});

// Function to scrape job description from the webpage
function scrapeJobDescription() {
  let jobDescription = "";

  // Customize this scraping logic based on the structure of the target job description page
  // Example: This tries to find the main content of the page
  let mainContent = document.querySelector("body"); // Modify this selector based on your needs
  if (mainContent) {
    jobDescription = mainContent.innerText;
  }
  console.log("Scraped job description:", jobDescription);
  return jobDescription;
}

// Function to generate cover letter based on the scraped job description
function generateCoverLetter(jobDescription) {
  console.log("Generating cover letter with job description:", jobDescription);
}

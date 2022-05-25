function logTabs(tabs) {
    console.log(tabs)
  }
  
  browser.tabs.query({currentWindow: true}, logTabs)
  

function notify(message){
  console.log(message)
  if (message.isPhishing == true){
    alert("Phishing Detected. \nStopped loading page.")
  }
}

browser.runtime.onMessage.addListener(notify);

console.log("loaded")
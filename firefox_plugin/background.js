async function listener(requestDetails) {
  console.log(requestDetails);
  var isPhishing = false;

  if (typeof requestDetails.documentUrl != "undefined") {
    console.log()
    return {}
  }

  await browser.runtime.sendNativeMessage(
    "fedphish",
    requestDetails.url
  ).then((response) => {
    console.log(response);
    isPhishing = response;
  });

  console.log("Native comms complete");

  if (isPhishing === true) {
    console.log("Phishing detected");
    // browser.tabs.executeScript({
    //   code: `alert("Phishing Detected");`
    // });
    await browser.tabs.create({url: "phishing_detected.html"});

    return {
      cancel: true
    }
  } else {
    return {}
  }

}

/*
On a click on the browser action, send the app a message.
*/
browser.webRequest.onBeforeRequest.addListener(
  listener,
  { urls: ["<all_urls>"] },
  ["blocking"],
)
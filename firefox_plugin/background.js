async function listener(requestDetails) {
  console.log(requestDetails.url);
  var isPhishing = false;

  await browser.runtime.sendNativeMessage(
    "fedphish",
    requestDetails.url
  ).then((response) => {
    console.log(response);
    isPhishing = response;
  });

  if (isPhishing === true) {
    console.log("Phishing detected");
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
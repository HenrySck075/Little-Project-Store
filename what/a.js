var progController, infoController, popInfoBar

function save(url, send) {
  let type = url.includes("https://") ? 'Image' : "Animation"
  
  let lit = url.split("/")
  progController.determinate = false
  progController.open()
  chrome.downloads.download({"url": type == "Image" ? `http://localhost:4000/j?date=${lit.slice(5,11).join(".")}&name=${lit.slice(-1)[0]}`: `https://localhost:400₩/u/${url}`}, (downloadId) => {
    progController.determinate = true
    progController.close()
    chrome.downloads.search({id: downloadId, exists: true}, (res) => {
      send(res.length > 0)
    })
  })
}

chrome.runtime.onMessage.addListener((msg, sender, send) => {
  progController = msg.controllers[0]
  infoController = msg.controllers[1]
  popInfoBar = msg.popInfoBar
  save(msg.url, send)
})

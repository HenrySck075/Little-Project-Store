let a = document.createElement("link")
a.href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css"
a.rel="stylesheet"
document.head.appendChild(a)

let b=document.createElement("script")
b.src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"
document.head.appendChild(b)

let c=document.createElement("script")
c.src="https://cdn.jsdelivr.net/npm/jimp@0.22.10/browser/lib/jimp.min.js"
document.head.appendChild(c)

function createElement(selector) {
  let tagName = selector.match(/^([^\.|#|\[]*)/g)
  if (tagName === null) {return {}}
  else {tagName = tagName[0]}
  let classes = selector.match(/\.([^\.|#|\[]*)/g)
  let id = selector.match(/#([^\.|#|\[]*)/g)
  if (id === null) {}
  else {id = id[0].replace("#", "")}
  let attrs = selector.match(/\[(.*)\]/g)
  if (attrs === null) {}

  let elem = document.createElement(tagName)
  if (classes !== null) {
    for (let cls of classes) {
        elem.classList.add(cls.replace(".",""))
        }
    }
  if (id !== null) elem.id = id
  if (attrs !== null) {
      attrs = attrs[0].replace("[", "").replace("]", "")
    for (let i of attrs.split(",")) {
        pair = i.split("=")
        k=pair[0].trim()
        v=pair[1].trim()
        if (["'",'"'].includes(v.at(0))) {v=v.slice(1,v.length-1)}
        if (["true","false"].includes(v)) {v=(v==="true")}
        if (!isNaN(v)) {v= +v}

        if (["innerText","outerText","innerHTML"].includes(k)) {
              elem[k]=v
            } else {
                  elem.setAttribute(k,v)
                }
        }
    }
  return elem
}

let btn = createElement("button.mdc-button.mdc-button--raised.downBtn")
btn.appendChild(createElement("div.mdc-button__ripple"))
btn.appendChild(createElement("span.mdc-button__label[innerText='Convert & Save']"))

let prog = createElement('div.mdc-linear-progress[aria-valuemin="0",aria-valuemax="1",aria-valuenow="0",role="progressbar"]')
let progBuffer = createElement('div.mdc-linear-progress__buffer')
progBuffer.appendChild(createElement("div.mdc-linear-progress__buffer-bar"))
let progBar = createElement('div.mdc-linear-progress__bar.mdc-linear-progress__primary-bar')
progBar.appendChild(createElement("span.mdc-linear-progress__bar-inner"))
let progBar2 = createElement('div.mdc-linear-progress__bar.mdc-linear-progress__secondary-bar')
progBar2.appendChild(createElement("span.mdc-linear-progress__bar-inner"))
prog.appendChild(progBuffer)
prog.appendChild(progBar)
prog.appendChild(progBar2)

let infoBar = createElement("aside.mdc-snackbar")
infoBar.appendChild(createElement("div.mdc-snackbar__surface[role='status',aria-relevant='additions']"))
infoBar.querySelector(".mdc-snackbar__surface").appendChild(createElement("div.mdc-snackbar__label[aria-atomic=false]"))

const observer = new MutationObserver(mutations => {
  try {
    for (let i of mutations) {
      if (i.addedNodes.length == 1) {
        console.log(i.addedNodes)
        let div = i.addedNodes[0].lastChild.parentElement
        if (div.classList.value.includes("illust-details-big")) {
          let controls = div.querySelector(".zoom-controls")
          controls.innerHTML = ""
          controls.appendChild(btn)
          div.insertBefore(prog,controls)
          controls.appendChild(infoBar)
        }
      }
    }
  } catch (e) {console.log(e.stack)}
})

var progController;
var infoController;

observer.observe(document.body, {
  childList: true,
  subtree: true
})

setTimeout(() => {
  mdc.ripple.MDCRipple.attachTo(btn)
  infoController = new mdc.snackbar.MDCSnackbar(infoBar)
  progController = new mdc.linearProgress.MDCLinearProgress(prog)
  progController.close()
}, 3000)

function popInfoBar(msg, time = -1) {
  infoController.close()
  infoController.timeoutMs = (time < 0 ? -1 : time*1000)
  infoController.labelText = msg
  infoController.open()
}

function saveOld(url) {
  let lit = url.split("/")
  let x = new XMLHttpRequest()
  x.open("GET", `http://localhost:4000/j?date=${lit.slice(5,11).join(".")}&name=${lit.slice(-1)[0]}`)
  progController.open()
  x.onprogress = e => {
    progController.foundation.setProgress(e.loaded/e.total)
  }
  x.onload = e => {
    let ponse = x.response
    let url = URL.createObjectURL(ponse)
    let anchor = createElement(`a[href="${url}"]`)
    anchor.download=url.split("/").slice(-1)[0]
    anchor.click()
    progController.close()
    progController.foundation.setProgress(0)
    popInfoBar("Image saved to disk",4)
    URL.revokeObjectURL(url)
  }
  x.responseType = "blob"
  x.send()
}

function save(url) {
  let lit = url.split("/")
  location.href = `http://localhost:4000/j?date=${lit.slice(5,11).join(".")}&name=${lit.slice(-1)[0]}`
}

btn.addEventListener("click", () => {
  save(document.querySelector("img.scaled-image").src)
})


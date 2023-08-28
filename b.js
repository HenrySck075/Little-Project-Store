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

let style = document.createElement("style")
style.sheet.insertRule(":root {--mdc-theme-primary: rgb(0,150,250)}")
document.head.appendChild(style)
function createButton(label, params = {}) {
  let btn = createElement("button.mdc-button.mdc-button--raised.downBtn")
  btn.appendChild(createElement("div.mdc-button__ripple"))
  btn.appendChild(createElement(`span.mdc-button__label[innerText=${label}]`))
  for (let e of Object.keys(params)) {
    btn[e] = params[e]
  }

  return btn
}
let btn = createButton('Convert & Save')

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

let observee = {}

const observer = new MutationObserver(mutations => {
  try {
    for (let i of Object.keys(observee)) {
      let h = document.querySelector(i)
      if (h !== null) {observee[i](h)}
    }
  } catch (e) {console.log(e.stack)}
})

var progController;
var infoController;

observer.observe(document.body, {
  childList: true,
  subtree: true
})

function onElementExist(sel, cb, multiple=false) {
  if (multiple) {
    for (let h of document.querySelectorAll(sel)) {
      cb(h)
    }
  }
  else {
    h = document.querySelector(sel)
    if (h !== null) cb(h)
  }
  observee[sel] = cb
}

onElementExist(".illust-details-big", (div) => {
  let controls = div.querySelector(".zoom-controls")
  controls.innerHTML = ""
  controls.appendChild(btn)
  div.insertBefore(prog,controls)
  controls.appendChild(infoBar)
})

function fullPath(el){ 
  var names = []; 
  while (el.parentNode){ 
    if (el.id){ 
      names.unshift('#'+el.id); break; 
    } else { 
      if (el==el.ownerDocument.documentElement) {
        names.unshift(el.tagName.toLowerCase());
      }
    else{ 
      for (var c=1,e=el;e.previousElementSibling;e=e.previousElementSibling,c++) {
        names.unshift(el.tagName+":nth-child("+c+")"); 
      } el=el.parentNode; 
    } 
  } 
  return names.join(" "); }
} // TODO: indent later

onElementExist(".user-details-card.top-card .user-details-follow .ui-button", (btn) => {
  btn.parentElement.replaceChild(createButton("Next", {click: null}))
})

onElementExist(".user-details-card:nth-child(2) .user-details-follow .ui-button", (btn) => {
  btn.parentElement.replaceChild(createButton("Queue", {onclick: (e) => {
    let elen = e.target
    if (elem.dataset.queueToggled ?? false) {
      elem.dataset.queueToggled = true
  }
  }}))
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


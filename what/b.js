function extractSelector(selector) {
  let tagName = selector.match(/^([^\.|#|\[]*)/g)
  if (tagName === null) {return {}}
  else {tagName = tagName[0]}
  let classes = selector.match(/\.([^\.|#|\[]*)/g)
  let id = selector.match(/#([^\.|#|\[]*)/g)
  if (id === null) {}
  else {id = id[0].replace("#", "")}
  let attraw = selector.match(/\[(.*)\]/g)
  let attrs = {}
  if (attraw !== null) {
    attraw = attraw[0].replace("[", "").replace("]", "")
    for (let i of attraw.split(",")) {
      pair = i.split("=")
      k=pair[0].trim()
      v=pair[1].trim()
      if (["'",'"'].includes(v.at(0))) {v=v.slice(1,v.length-1)}
      if (["true","false"].includes(v)) {v=(v==="true")}
      if (!isNaN(v)) {v= +v}
      attrs[k] = v
    }
  }

  return [tagName, classes, id, attrs]
}

function createElement(selector) {
  let [tagName, classes, id, attrs] = extractSelector(selector)

  let elem = document.createElement(tagName)
  if (classes !== null) {
    for (let cls of classes) {
        elem.classList.add(cls.replace(".",""))
        }
    }
  if (id !== null) elem.id = id
  if (attrs !== {}) {
    for (let k of Object.keys(attrs)) {
      let v = attrs[k]

      if (["innerText","outerText","innerHTML"].includes(k)) {
        elem[k]=v
      } else {
        elem.setAttribute(k,v)
      }
    }
  }
  return elem
}


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

function allProvidedAttrsExist(elem, attrs) {
  for (let k of Object.keys(attrs)) {
    let v = attrs[k]
    
    // if `k` is attributes that is not visible in html file     "access using brace"      "access using getAttribute"
    if (!(["innerText","outerText","innerHTML"].includes(k)    ?   (elem[k] == v)    :    (elem.getAttribute(k) == v))) return false
  }
  return true
}

var progController;
var infoController;


function onElementExist(sel, cb, boundary = document.body) {
  for (let h of boundary.querySelectorAll(sel)) {
    cb(h)
  }
  const observer = new MutationObserver(mutations => {
    // time complexity 🔥🔥🔥🔥🔥🔥🔥🔥🗣️🗣️🗣️🗣️🗣️
    for (let mut of mutations) {
      for (let i of mut.addedNodes) {
        boundary.querySelectorAll(sel).forEach(el => {
          console.log(i.isEqualNode(el))
          if (i.isEqualNode(el)) cb(i)
        })
      }
    }
  })
  
  observer.observe(boundary, {
    childList: true,
    subtree: true
  })
}


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

function popInfoBar(msg, time = -1) {
  infoController.close()
  infoController.timeoutMs = (time < 0 ? -1 : time*1000)
  infoController.labelText = msg
  infoController.open()
}

// literally just to wait for main illust element
function waitForElm(selector) {
  return new Promise(resolve => {
      if (document.querySelector(selector)) {
          return resolve(document.querySelector(selector));
      }

      const observer = new MutationObserver(mutations => {
          if (document.querySelector(selector)) {
              observer.disconnect();
              resolve(document.querySelector(selector));
          }
      });

      observer.observe(document.body, {
          childList: true,
          subtree: true
      });
  });
}

function main(gang, nam) {

  btn.addEventListener("click", () => {
    chrome.runtime.sendMessage({
      "url": document.querySelector(".illust-details-ugoira") ? location.href.split("/").slice(-1)[0] : document.querySelector("img.scaled-image").src,
      "popInfoBar": popInfoBar,
      "controllers": [progController, infoController]
    }, res => {
       res ? popInfoBar(type+" saved to device",4) : popInfoBar(type+" downloading failed",4)
    })
  })

  mdc.ripple.MDCRipple.attachTo(btn)
  infoController = new mdc.snackbar.MDCSnackbar(infoBar)
  progController = new mdc.linearProgress.MDCLinearProgress(prog)
  progController.close()

  console.log('ahwsufivbehwisuv')
  if (document.querySelector("title").innerText.includes("ugoira")) {
    console.log("what the heck")
    onElementExist(".segment-top.user-badge", div => {
      let controls = div.querySelector(".user-details-card")
      controls.innerHTML = ""
      controls.appendChild(btn)
      div.insertBefore(prog, controls)
      controls.appendChild(infoBar)
    })
  } else {
    onElementExist(".illust-details-big", (div) => {
      console.log("que pro")
      let controls = div.querySelector(".zoom-controls")
      controls.innerHTML = ""
      controls.appendChild(btn)
      div.insertBefore(prog,controls)
      controls.appendChild(infoBar)
    })
  }
}

document.addEventListener("DOMContentLoaded", main)

function $(s) {
    return document.querySelector(s)
};
function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }
        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}
let Resources;
let s = document.createElement("script")
s.src = "//cdn.jsdelivr.com/HenrySck075/Little-Project-Store/neal.rsc.js"
document.body.appendChild(s)
while (Resources === undefined) {}
function ThePasswordGame() {
    let pswdRsc = Resources.ThePasswordGame
    let password = '';
    let countries = pswdRsc.countries
    let chessSolutions = pswdRsc.chessSolutions
    let vowels = pswdRsc.vowels
    let atomics = pswdRsc.atomics
    let ytDurations = pswdRsc.ytDurations
    let states = {
        boldVowels: false,
	wingdings: false
    }
    //https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
    function update(v) {
	//let untagged = v.slice()
	if (states.boldVowels) {
	    for (let i of vowels) { 
		v = v.replaceAll(i, `<strong>${i}</strong>`) 
		v = v.replaceAll(i.toUpperCase(), `<strong>${i.toUpperCase()}</strong>`) 
	    }
        }
        pswbox.innerHTML = v
    };
    function wait(ms) {
        var start = Date.now(),
            now = start;
        while (now - start < ms) {
            now = Date.now();
        }
    }
    // rule 16 can causes rule 18 to break so we'll fix that here
    function fixAtomic(str) {
	    setTimeout(()=>{
		if ($(".atomic-number .rule-top img").src.includes("error")) {
		    let atomic = atomics[str.match(/H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Sc|Ti|V|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Y|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|I|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|W|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|U|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr|Rf|Db|Sg|Bh|Hs|Mt|Ds|Rg|Cn|Nh|Fl|Mc|Lv|Ts|Og|Uue/g)[0]]
		    update(password.replace("H".repeat(atomic),""))
		}
	    }, 100)
    }
    function captcha() {
        let str = $(".captcha-img").src.split("/").slice(-1)[0].split(".png")[0]
        let dcapt = str.matchAll(/\d+/g)
        console.log(dcapt)
        let dint = 0
        for (let i of dcapt) { dint = dint + parseInt(i) }
        // reroll if sum is higher than 25
        if (dint > 21) {
            $(".captcha-refresh").click();
            setTimeout(captcha, 1000)
        }
        else if (dint != 0) update(password.replace("1".repeat(dint), "") + str)
        else update(password + str)
    }
    let saved = password.slice()
    function geoguess(idx) {
        let i = countries[idx]
        update(password + " " + i.toLowerCase())
        setTimeout(() => {
            if ($(".geo .rule-icon").src.includes("error")) {update(saved);geoguess(idx + 1)}
        }, 50)
    }
    var pswbox = $("[contenteditable=true] p");
    let stat = document.createElement("p")
    stat.style.textAlign = "center"
    $(".password-wrapper").insertBefore(stat, $(".password-box"))
    //password box
    // in case paul and the fire change the password
    pswbox.addEventListener("DOMSubtreeModified", () => {
        password = pswbox.innerText
    })
    update('I am loved maypepsi111111111111111111111 4AXXXVHe🌑🌘🌗🌖🌕🌔🌓🌒🌑 🏋️‍♂️🏋️‍♂️🏋️‍♂️'+"H".repeat(122));
    //captcha
    waitForElm('.captcha-img').then(() => { captcha() })
    //wordle
    waitForElm('.wordle').then(() => {
        stat.innerText = "Adding wordle string..."
        let r = new XMLHttpRequest()
        r.open("GET", `https://neal.fun/api/password-game/wordle?date=${new Date().toISOString().split("T")[0]}`)
        r.send()
        r.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                update(password + JSON.parse(r.responseText).answer)
                if (!$(".wordle .rule-icon").src.includes("checkmark")) update(password + JSON.parse(r.responseText).tomorrowAnswer)
                stat.innerText = "Waiting..."
            }
        };
    })
    //geoguess
    waitForElm('.geo').then(() => {
        setTimeout(() => {
            saved = password.slice()
            stat.innerText = "Cycling through list of supported guesses..."
            geoguess(0)
        }, 100)
    })
    //chess
    //TODO: debug on pc this thing have 50% chance to crash
    waitForElm(".chess-wrapper").then(() => {
        setTimeout(() => {
            let idx = + $(".chess-img").src.split("puzzle")[1].split(".svg")[0]
            let str = chessSolutions[idx]
            let dcapt = str.matchAll(/\d+/g)
            let dint = 0
            for (let i of dcapt) { dint = dint + parseInt(i) }
            update(password.replace("1".repeat(dint), "") + str)
	    fixAtomic(str)
        }, 100)
    })
    //paul
    waitForElm(".egg").then(() => { update(password + "🥚🐛🐛🐛") })
    //vowels
    waitForElm(".bold-vowels").then(() => {
	states.boldVowels = true
	update(password)
    })
    //fire
    waitForElm(".fire").then(()=>{
	update(password.replaceAll("🔥",""))
    })
};
ThePasswordGame()

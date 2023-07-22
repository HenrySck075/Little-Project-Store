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

function ThePasswordGame() {
    let password = '';
    let countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "St Lucia", "Samoa", "San Marino", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "England", "United States", "Britain"]
    let chessSolutions = ["Nf6+", "Qd5+", "Qb8+", "Qd8+", "Qxg6+", "Qxd7+", "Qxf8+", "Qd7+", "Qg6+", "Qxh6+", "Qg4+", "Qxh6+", "Qg6+", "Rg1+", "Qxh5+", "Ne7", "Qc3+", "Qf5+", "Bf6+", "Qc8+", "Re8+", "Rc1+", "Bf4+", "Ne6+", "Qf8+", "Bf5+", "Qxc6+", "Qxb8+", "Qxd6+", "Rd8+", "Nd3+", "Rxb6+", "Qxf7+", "Nf6+", "Qe7+", "Rg8+", "Qxf7+", "Be3+", "Nh4+", "Qxe6+", "Qf8+", "Qf6+", "Nb5+", "Qxh7+", "Qxb7+", "Qg1+", "Bh6+", "Rxf6+", "Qxh6+", "h5+", "Nxd7+", "Rxh2+", "Bb5+", "Rg8+", "Qh8+", "Bh5+", "Qh7+", "Qxh7+", "Ne5+", "Qxg7+", "Rh8+", "Rxh6+", "Qxe8+", "Rxe8+", "Qxh6+", "Qxh7+", "Kh6", "Be1+", "Rxg7+", "Qxg7+", "Rg7", "Bd6+", "Ng6+", "Qh3+", "Rg1+", "Qg1+", "Rh8+", "Rf6", "Re7+", "Qh6+", "Qxh7+", "Rf6+", "Qf7+", "Bb6+", "Rxg6+", "Qh8+", "Rxh3+", "Rxh7+", "Nf5+", "Rxf7+", "Rf7+", "f5+", "Rh8+", "Qxf2+", "Qxf8+", "Re8+", "Rxf6+", "Qh3+", "Nf3", "Qxe6+", "Rg8+", "Qe8+", "Rxf5+", "Qxh2+", "Rxf8+", "Rxg6+", "Bf2+", "Qxc3+", "Nd4+", "Qxh3+", "Nf4+", "Qg2+", "Qxh7+", "Qh2+", "Qh1+", "Qxh3+", "Rxg7+", "Qd8+", "Rd8+", "Rd8+", "Nd5+", "Rc8+", "g5+", "Rh4+", "Ng6+", "Qxe6+", "Bf7+", "Ne7+", "Nh8+", "Rxf1+", "Bxg6+", "Nxf7+", "Re5+", "Rf8+", "Rxe6+", "Rxh7+", "Nxb7+", "Qg8+", "Qxh6+", "Ra1+", "Rh8+", "Bg6+", "Qd8+", "Qh5+", "Qxg6+", "Qxa3+", "Bg6+", "Nf4+", "Qxc3+", "Ne6+", "Nxf7+", "Rxd8+", "Ng3+", "Re8+", "Bxf3+", "Rh2+", "Re8+", "Bh6", "Qb5+", "Qh6+", "Rxh7+", "Rxf7+", "Rxf8+", "Rh6", "Bf5+", "Rxh6+", "Qe6+", "Rxa7+", "Rg2+", "Qg4+", "Qh1+", "g4+", "Qc6+", "Rg8+", "Bf6+", "Qc6", "f2+", "Ne2+", "Rh6+", "Rc1+", "Ne4+", "Ng4", "Rf7+", "Qd8+", "Rxh6+", "Qg7+", "Be5+", "Rxh6+", "Re4+", "Nf7+", "Rxh6+", "Rf1+", "Rg8+"]
    let vowels = ["o", "u", "e", "a", "i", "y"]
    let atomics = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10, "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20, "Sc": 21, "Ti": 22, "V": 23, "Cr": 24, "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30, "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39, "Zr": 40, "Nb": 41, "Mo": 42, "Tc": 43, "Ru": 44, "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49, "Sn": 50, "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "La": 57, "Ce": 58, "Pr": 59, "Nd": 60, "Pm": 61, "Sm": 62, "Eu": 63, "Gd": 64, "Tb": 65, "Dy": 66, "Ho": 67, "Er": 68, "Tm": 69, "Yb": 70, "Lu": 71, "Hf": 72, "Ta": 73, "W": 74, "Re": 75, "Os": 76, "Ir": 77, "Pt": 78, "Au": 79, "Hg": 80, "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89, "Th": 90, "Pa": 91, "U": 92, "Np": 93, "Pu": 94, "Am": 95, "Cm": 96, "Bk": 97, "Cf": 98, "Es": 99, "Fm": 100, "Md": 101, "No": 102, "Lr": 103, "Rf": 104, "Db": 105, "Sg": 106, "Bh": 107, "Hs": 108, "Mt": 109, "Ds": 110, "Rg": 111, "Cn": 112, "Nh": 113, "Fl": 114, "Mc": 115, "Lv": 116, "Ts": 117, "Og": 118, "Uue": 119}

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


function $(s) {
    return document.querySelector(s)
};
function ThePasswordGame() {
    let password = '';
    let countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "St Lucia", "Samoa", "San Marino", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "England", "United States", "Britain"]
    let chessSolutions = ["Nf6+", "Qd5+", "Qb8+", "Qd8+", "Qxg6+", "Qxd7+", "Qxf8+", "Qd7+", "Qg6+", "Qxh6+", "Qg4+", "Qxh6+", "Qg6+", "Rg1+", "Qxh5+", "Ne7", "Qc3+", "Qf5+", "Bf6+", "Qc8+", "Re8+", "Rc1+", "Bf4+", "Ne6+", "Qf8+", "Bf5+", "Qxc6+", "Qxb8+", "Qxd6+", "Rd8+", "Nd3+", "Rxb6+", "Qxf7+", "Nf6+", "Qe7+", "Rg8+", "Qxf7+", "Be3+", "Nh4+", "Qxe6+", "Qf8+", "Qf6+", "Nb5+", "Qxh7+", "Qxb7+", "Qg1+", "Bh6+", "Rxf6+", "Qxh6+", "h5+", "Nxd7+", "Rxh2+", "Bb5+", "Rg8+", "Qh8+", "Bh5+", "Qh7+", "Qxh7+", "Ne5+", "Qxg7+", "Rh8+", "Rxh6+", "Qxe8+", "Rxe8+", "Qxh6+", "Qxh7+", "Kh6", "Be1+", "Rxg7+", "Qxg7+", "Rg7", "Bd6+", "Ng6+", "Qh3+", "Rg1+", "Qg1+", "Rh8+", "Rf6", "Re7+", "Qh6+", "Qxh7+", "Rf6+", "Qf7+", "Bb6+", "Rxg6+", "Qh8+", "Rxh3+", "Rxh7+", "Nf5+", "Rxf7+", "Rf7+", "f5+", "Rh8+", "Qxf2+", "Qxf8+", "Re8+", "Rxf6+", "Qh3+", "Nf3", "Qxe6+", "Rg8+", "Qe8+", "Rxf5+", "Qxh2+", "Rxf8+", "Rxg6+", "Bf2+", "Qxc3+", "Nd4+", "Qxh3+", "Nf4+", "Qg2+", "Qxh7+", "Qh2+", "Qh1+", "Qxh3+", "Rxg7+", "Qd8+", "Rd8+", "Rd8+", "Nd5+", "Rc8+", "g5+", "Rh4+", "Ng6+", "Qxe6+", "Bf7+", "Ne7+", "Nh8+", "Rxf1+", "Bxg6+", "Nxf7+", "Re5+", "Rf8+", "Rxe6+", "Rxh7+", "Nxb7+", "Qg8+", "Qxh6+", "Ra1+", "Rh8+", "Bg6+", "Qd8+", "Qh5+", "Qxg6+", "Qxa3+", "Bg6+", "Nf4+", "Qxc3+", "Ne6+", "Nxf7+", "Rxd8+", "Ng3+", "Re8+", "Bxf3+", "Rh2+", "Re8+", "Bh6", "Qb5+", "Qh6+", "Rxh7+", "Rxf7+", "Rxf8+", "Rh6", "Bf5+", "Rxh6+", "Qe6+", "Rxa7+", "Rg2+", "Qg4+", "Qh1+", "g4+", "Qc6+", "Rg8+", "Bf6+", "Qc6", "f2+", "Ne2+", "Rh6+", "Rc1+", "Ne4+", "Ng4", "Rf7+", "Qd8+", "Rxh6+", "Qg7+", "Be5+", "Rxh6+", "Re4+", "Nf7+", "Rxh6+", "Rf1+", "Rg8+"]
    //https://stackoverflow.com/questions/5525071/how-to-wait-until-an-element-exists
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

    function update(v) {
        span.innerHTML = v
    };
    function wait(ms) {
        var start = Date.now(),
            now = start;
        while (now - start < ms) {
            now = Date.now();
        }
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
            if ($(".geo .rule-icon").src.includes("checkmark.svg")) { update(saved + " " + i.toLowerCase()) }
            else geoguess(idx + 1)
        }, 50)
    }
    var span;
    let stat = document.createElement("p")
    stat.style.textAlign = "center"
    $(".password-wrapper").insertBefore(stat, $(".password-box"))
    stat.innerText = "Please enter anything to the box (i cant do that) (why the heck neal use br instead of empty span)"
    //password box
    waitForElm("[contenteditable=true] p span").then(e => {
        span = e
	// in case paul and the fire change the password
	span.addEventListener("DOMSubtreeModified", ()=>{
	    password=span.innerText
	})
	update('maypepsi1111111111111111111114AVIIVHe🌑🌘🌗🌖🌕🌔🌓🌒🌑');
    })
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
        }, 4000)
    })
    //chess
    waitForElem(".chess").then(()=>{
	let idx = + $(".chess-wrapper img").src.split("puzzle").slice(-1)[0].split(".png")[0]
	    update(password+chessSolutions[idx-1])
    })
}

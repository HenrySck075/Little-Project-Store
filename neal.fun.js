function ThePasswordGame(){
let password = '';
let countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "St Lucia", "Samoa", "San Marino", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "America", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe", "England", "United States", "Britain"]
function $(s) {
    return document.querySelector(s)
};
// let span = $('[contenteditable=true] p span');
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
    password = v;
    span.innerText = v
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
    for (let i of dcapt) {dint = dint + parseInt(i)}
    // reroll if sum is higher than 25
    if (dint > 25) {
        $(".captcha-refresh").click();
        setTimeout(captcha, 1000)
    }
    else if (dint != 0) update(password.replace("1".repeat(dint),"")+str)
    else update(password+str)
}
let saved = password.slice()
function geoguess(idx) {
    let i = countries[idx]
    update(password+" "+i.toLowerCase())
    setTimeout(()=>{
        if ($(".geo .rule-icon").src.includes("checkmark.svg")) {update(saved+" "+i.toLowerCase())}
        else geoguess(idx+1)
    }, 100)
}
var span;
let stat = document.createElement("p")
stat.style.textAlign="center"
$(".password-wrapper").insertBefore(stat,$(".password-box"))
stat.innerText = "Please enter anything to the box (i cant do that) (why the heck neal use br instead of empty span)"
//init
waitForElm("[contenteditable=true] p span").then(e => {
    span = e;update('maypepsi11111111111111111111111110AVIIVHe🌑🌘🌗🌖🌕🌔🌓🌒🌑');
})
//captcha
waitForElm('.captcha-img').then(() => {captcha()})
//wordle
waitForElm('.wordle').then(()=>{
    stat.innerText="Adding wordle string..."
    let r = new XMLHttpRequest()
    r.open("GET",`https://neal.fun/api/password-game/wordle?date=${new Date().toISOString().split("T")[0]}`)
    r.send()
    r.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            update(password+JSON.parse(r.responseText).answer)
            stat.innerText="Waiting..."
        }
    };
})
//geoguess
waitForElm('.geo').then(()=>{
    setTimeout(()=>{
        saved=password.slice()
        stat.innerText="Cycling through list of supported guesses..."
        geoguess(0)
    },4000)
})
}

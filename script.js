 
fetch('https://iotbackend-pavanapril14.b4a.run/', {
    method : "POST",
    body : JSON.stringify({
        "z1" : 0.25,
    "z2" : 2.5,
    "z3" : 2.4
    }),
    headers :  {
        "Content-type": "application/json; charset=UTF-8"
    }
}).then((e) => e.json())
.then((e) => {
    console.log(e)

    zscores = e.z1.toString() + " " + e.z2.toString() + " " + e.z3.toString()
    console.log(zscores)
    document.getElementById('z-scores').innerHTML = zscores
    risk = document.getElementById('risk')
    let color;
    if(e.pred == 'low') color = 'blue'
    else if(e.pred  == 'medium') color = 'orange'
    else color = 'red'

    risk.innerHTML = e.pred;
    risk.style.color = color;
    console.log(e.pred)
})

import { serverEP } from './index.js'
const rspwForm = document.getElementById('rspwForm')

rspwForm.onsubmit = (e) => {
    e.preventDefault();
    errorMsg.style.color = "grey"
    errorMsg.innerHTML = "Processing Data ..."
    fetch(`${serverEP}/reset_password`, {
        method: 'PATCH',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(e.target)))
    })
    .then(resp => {
        if (resp.status === 200){
            let counter = 3;
            let rspwCounter;
            rspwCounter = setInterval(() =>  {
                errorMsg.style.color = "green"
                errorMsg.innerHTML = `Please check your Email inbox for the OTP. <br> Redirecting to the reset page in ${counter}`
                counter--
                if(counter < 0){
                    clearInterval(rspwCounter)
                    window.location = "/"
                }
            }, 1000)
            
        } else {
            return resp.json()
        }
    })
    .then(res => {
        errorMsg.style.color = "red"
        errorMsg.innerHTML = res.message
    })
}

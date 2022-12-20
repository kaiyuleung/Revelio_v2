import { serverEP } from './index.js'
const fgpwForm = document.getElementById('fgpwForm')

fgpwForm.onsubmit = (e) => {
    e.preventDefault();
    errorMsg.style.color = "grey"
    errorMsg.innerHTML = "Processing Data ..."
    fetch(`${serverEP}/forgot_password`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(e.target)))
    })
    .then(resp => {
        if (resp.status === 200){
            let counter = 3;
            let fgpwCounter;
            fgpwCounter = setInterval(() =>  {
                errorMsg.style.color = "green"
                errorMsg.innerHTML = `Please check your Email inbox for the OTP. <br> Redirecting to the reset page in ${counter}`
                counter--
                if(counter < 0){
                    clearInterval(fgpwCounter)
                    window.location = "/reset_password"
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

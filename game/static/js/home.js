// const regForm = document.getElementById('registerForm')
const errorMsg = document.getElementById('errorMsg')

$('#registerForm').submit( (e) => {
    e.preventDefault();
    $('#errorMsg').html("Processing Data ...")
    $('#errorMsg').css('color', "grey")
    fetch(`/register`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(e.target)))
    })
    .then(resp => {
        if (resp.status === 200){
            $('#errorMsg').html("Successful, Logging you in ...")
            $('#errorMsg').css('color', "green")
            window.location = "/dashboard"
        } else {
            return resp.json()
        }
    })
    .then(res => {
        $('#errorMsg').html(res.message)
        $('#errorMsg').css('color', "red")
    })
})

$('#fgpwBtn').click(() => window.location = '/forgot_password')
$('#rspwBtn').click(() => window.location = '/reset_password')

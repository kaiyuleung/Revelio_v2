$('#logout').click( (e) => {
    e.preventDefault()
    fetch(`/logout`)
    .then(resp => {
        if (resp.status === 200) {
            window.location = "/"
        } else {
            console.warn(`${resp.status}: sth wrong with logout `)
        }
    })
})

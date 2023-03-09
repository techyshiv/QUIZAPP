$("#user_registration_form").submit(function (e) {
    e.preventDefault();
    let fname = $("#firstname").val();
    let lname = $("#lastname").val();
    let email = $("#email").val();
    let password = $("#password").val();
    let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    // apply validation
    if (fname == "" || lname == "" || email == "", password == "") {
        Swal.fire(
            'Warning !',
            'All fields are required !!',
            'error'
        )
        return false;
    }
    if (!(fname.length >= 3 && lname.length >= 3)) {
        Swal.fire(
            'Warning !',
            'Name Length should be equal or greter than 3 !!',
            'error'
        )
        return false;
    }

    if (!email.match(mailformat)) {
        Swal.fire(
            'Warning !',
            'Invalid Email Address !!',
            'error'
        )
        return false;
    }

    if (password.length >= 8) {
        console.log("Yes")
    }
    else {
        console.log("no")
    }

    if (!(password.length >= 8)) {
        Swal.fire(
            'Warning !',
            'Password Length should be equal or greter than 8 !!',
            'error'
        )
        return false;
    }

    let details = {
        "firstname": fname,
        "lastname": lname,
        "email": email,
        "password": password,
        "role": "user"
    }

    console.log(JSON.stringify(details))

    $.ajax({
        type: "POST",
        data: JSON.stringify(details),
        contentType: "application/json",
        url: "http://localhost:5000/v1/auth/register",
        success: function (response) {
            Swal.fire(
                'Success !',
                'Verification Link send to your email address !!',
                'success'
            ).then(function () {
                window.location = "http://localhost:5000/v1/auth/login"
            })
        },
        error: function (err) {
            if (err.status == 409) {
                Swal.fire(
                    'warning !',
                    `${err.responseJSON.message} !!`,
                    'error'
                ).then(function () {
                    window.location = "http://localhost:5000/v1/auth/login"
                })
            }
            else {
                Swal.fire(
                    'warning !',
                    `${err.responseJSON.message} !!`,
                    'error'
                )
            }
        }
    });
})

$("#user_login_form").submit(function (e) {
    e.preventDefault();
    let email = $("#email").val();
    let password = $("#password").val();
    let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    // apply validation
    if (email == "", password == "") {
        Swal.fire(
            'Warning !',
            'All fields are required !!',
            'error'
        )
        return false;
    }

    if (!email.match(mailformat)) {
        Swal.fire(
            'Warning !',
            'Invalid Email Address !!',
            'error'
        )
        return false;
    }
    let details = {
        "email": email,
        "password": password,
    }

    console.log(JSON.stringify(details))

    $.ajax({
        type: "POST",
        data: JSON.stringify(details),
        contentType: "application/json",
        url: "http://localhost:5000/v1/auth/login",
        success: function (response) {
            Swal.fire(
                'Success !',
                'Login Successfull !!',
                'success'
            ).then(function () {
                window.location = "http://localhost:5000"
            })
        },
        error: function (err) {
            console.log("error")
            console.log(err)
            if (err.status == 400) {
                Swal.fire(
                    'warning !',
                    `${err.responseJSON.message} !!`,
                    'error'
                ).then(function () {
                    window.location = "http://localhost:5000/v1/auth/register"
                })
            }
            else {
                Swal.fire(
                    'warning !',
                    `${err.responseJSON.message} !!`,
                    'error'
                )
            }
        }
    });
})

// quiz
function submitForm(e) {
    e.preventDefault();
    let name = document.getElementById("user_name").value;
    sessionStorage.setItem("name", name);
    location.href = "quiz";
}
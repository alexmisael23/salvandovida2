const signinForm = document.querySelector('#login-form');

signinForm.addEventListener('submit', e =>{
    e.preventDefault();
    const email = document.querySelector('#login-email').value;
    const password = document.querySelector('#login-password').value;
    console.log(email, password)

})
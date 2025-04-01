const Toggler = document.getElementById('pwd-toggle');
const TogglerC = document.getElementById('pwd-toggle-cc');

document.getElementById('pwd-toggle').addEventListener('click', () => {
    const passwordInput = document.getElementById('dyn-pwd');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        Toggler.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7s-1.39 3.21-3.5 5.1"></path><path d="M6.61 6.61A13.66 13.66 0 0 0 2 12s3 7 10 7a9.9 9.9 0 0 04.13-.86"></path><line x1="2" y1="2" x2="22" y2="22"></line></svg>';
    } else {
        passwordInput.type = 'password';
        Toggler.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
    }
});

document.getElementById('pwd-toggle-cc').addEventListener('click', () => {
    const confirmPasswordInput = document.getElementById('dyn-pwd-cc');
    if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
        TogglerC.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7s-1.39 3.21-3.5 5.1"></path><path d="M6.61 6.61A13.66 13.66 0 0 0 2 12s3 7 10 7a9.9 9.9 0 0 04.13-.86"></path><line x1="2" y1="2" x2="22" y2="22"></line></svg>';
    } else {
        confirmPasswordInput.type = 'password';
        TogglerC.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
    }
});

document.getElementById('dyn-pwd-cc').addEventListener('input', () => {
    const password = document.getElementById('dyn-pwd').value;
    const confirmPassword = document.getElementById('dyn-pwd-cc').value;

    if (password !== confirmPassword) {
        document.getElementById('dyn-error-msg').innerText = '**Passwords do not match';
    } else {
        document.getElementById('dyn-error-msg').innerText = '.';
    }
});

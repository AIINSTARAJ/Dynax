document.getElementById('pwd-toggle').addEventListener('click', () => {
    const passwordInput = document.getElementById('dyn-pwd');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

document.getElementById('pwd-toggle-cc').addEventListener('click', () => {
    const confirmPasswordInput = document.getElementById('dyn-pwd-cc');
    if (confirmPasswordInput.type === 'password') {
        confirmPasswordInput.type = 'text';
    } else {
        confirmPasswordInput.type = 'password';
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

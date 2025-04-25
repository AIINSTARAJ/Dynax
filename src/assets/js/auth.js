
document.querySelector('.menu-toggle').addEventListener('click', function () {
    document.querySelector('.nav-links').classList.toggle('active');
    document.querySelector('.hamburger').classList.toggle('active');
});

// Password toggle visibility
document.getElementById('passwordToggle').addEventListener('click', function () {
    const passwordField = document.getElementById('password');
    const icon = this.querySelector('i');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        passwordField.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
});

document.getElementById('confirmToggle').addEventListener('click', function () {
    const confirmField = document.getElementById('confirmPassword');
    const icon = this.querySelector('i');

    if (confirmField.type === 'password') {
        confirmField.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        confirmField.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
});

// Password strength meter
document.getElementById('password').addEventListener('input', function () {
    const password = this.value;
    const meter = document.getElementById('strengthMeter');
    const text = document.getElementById('strengthText');

    // Simple strength calculation
    let strength = 0;

    // Length check
    if (password.length >= 8) strength += 1;
    if (password.length >= 12) strength += 1;

    // Complexity checks
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;

    // Update meter
    if (password.length === 0) {
        meter.style.width = '0%';
        meter.className = 'strength-meter';
        text.textContent = 'Password strength';
    } else if (strength < 3) {
        meter.style.width = '30%';
        meter.className = 'strength-meter weak';
        text.textContent = 'Weak';
    } else if (strength < 5) {
        meter.style.width = '60%';
        meter.className = 'strength-meter medium';
        text.textContent = 'Medium';
    } else {
        meter.style.width = '100%';
        meter.className = 'strength-meter strong';
        text.textContent = 'Strong';
    }

    // Check if passwords match
    checkPasswordMatch();
});

// Password match check
document.getElementById('confirmPassword').addEventListener('input', checkPasswordMatch);

function checkPasswordMatch() {
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;
    const matchIndicator = document.getElementById('passwordMatch');

    if (confirm.length === 0) {
        matchIndicator.style.display = 'none';
    } else {
        matchIndicator.style.display = 'block';

        if (password === confirm) {
            matchIndicator.textContent = 'Passwords match!';
            matchIndicator.className = 'password-match valid';
        } else {
            matchIndicator.textContent = 'Passwords do not match!';
            matchIndicator.className = 'password-match invalid';
        }
    }
}

// Form submission
document.getElementById('signupForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // You would typically handle the form submission with AJAX here
    alert('Account creation would be processed here!');
});


function showAiMessage(messageId, delay, callback) {
    // Show typing indicator
    document.getElementById('typingIndicator').style.display = 'flex';

    // After delay, hide typing indicator and show the message
    setTimeout(() => {
        document.getElementById('typingIndicator').style.display = 'none';
        const message = document.getElementById(messageId);
        message.style.display = 'block';

        // Apply fade-in animation
        gsap.from(message, {
            duration: 0.5,
            y: 10,
            opacity: 0,
            ease: 'power2.out',
            onComplete: () => {
                // If there's a callback, execute it
                if (callback) callback();
            }
        });
    }, delay);
}
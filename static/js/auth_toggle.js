document.addEventListener('DOMContentLoaded', function () {
    const toggleLink = document.getElementById('toggle-link');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const formTitle = document.getElementById('form-title');

    toggleLink.addEventListener('click', function (e) {
        e.preventDefault();

        if (loginForm.style.display === 'block') {
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
            formTitle.textContent = 'Register';
            toggleLink.textContent = 'Already have an account? Login';
        } else {
            loginForm.style.display = 'block';
            registerForm.style.display = 'none';
            formTitle.textContent = 'Login';
            toggleLink.textContent = "Don't have an account? Register";
        }
    });
});
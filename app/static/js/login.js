document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector(".auth-form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    const errorBox = document.getElementById('form-error');

    if (form) {
        form.addEventListener("submit", (e) => {
            let valid = true;
            let message = '';

            if (usernameInput && usernameInput.value.trim() === "") {
                valid = false;
                message = 'Please enter your phone number.';
            }

            if (passwordInput && passwordInput.value.trim() === "") {
                valid = false;
                message = message ? message + ' Password is required.' : 'Please enter your password.';
            }

            if (!valid) {
                e.preventDefault();
                if (errorBox) {
                    errorBox.textContent = message;
                    errorBox.style.display = 'block';
                } else {
                    alert(message);
                }
            }
        });

        // Clear error when user types
        [usernameInput, passwordInput].forEach((el) => {
            if (!el) return;
            el.addEventListener('input', () => {
                if (errorBox) errorBox.style.display = 'none';
            });
        });
    }

});

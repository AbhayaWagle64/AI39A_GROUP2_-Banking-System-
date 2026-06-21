document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".auth-form");
    if (form) {
        form.addEventListener("submit", (e) => {
            const password = document.getElementById("password");
            const confirmPassword = document.getElementById("confirm_password");
            if (password && confirmPassword) {
                if (password.value !== confirmPassword.value) {
                    e.preventDefault();
                    alert("Passwords do not match.");
                    return false;
                }
            }
        });
    }
});

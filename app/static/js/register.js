<<<<<<< HEAD
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
=======
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const strengthBar = document.getElementById("strengthBar");
const strengthText = document.getElementById("strengthText");
const registerForm = document.getElementById("registerForm");

const btnText = document.getElementById("btnText");
const btnLoader = document.getElementById("btnLoader");

const phone = document.getElementById("phone");
const email = document.getElementById("email");

const toast = document.getElementById("toast");

/* ------------------------------
PASSWORD STRENGTH
------------------------------ */

password.addEventListener("input", () => {

    const value = password.value;

    let strength = 0;

    if (value.length >= 8) strength++;
    if (/[A-Z]/.test(value)) strength++;
    if (/[0-9]/.test(value)) strength++;
    if (/[^A-Za-z0-9]/.test(value)) strength++;

    switch (strength) {

        case 1:
            strengthBar.style.width = "25%";
            strengthBar.className = "h-full bg-red-500";
            strengthText.innerText = "Weak Password";
            break;

        case 2:
            strengthBar.style.width = "50%";
            strengthBar.className = "h-full bg-yellow-500";
            strengthText.innerText = "Moderate Password";
            break;

        case 3:
            strengthBar.style.width = "75%";
            strengthBar.className = "h-full bg-blue-500";
            strengthText.innerText = "Strong Password";
            break;

        case 4:
            strengthBar.style.width = "100%";
            strengthBar.className = "h-full bg-emerald-500";
            strengthText.innerText = "Very Strong Password";
            break;

        default:
            strengthBar.style.width = "0%";
            strengthText.innerText = "Password strength";
    }
});

/* ------------------------------
CONFIRM PASSWORD
------------------------------ */

confirmPassword.addEventListener("input", () => {

    const confirmError = document.getElementById("confirmError");

    if (confirmPassword.value !== password.value) {
        confirmError.innerText = "Passwords do not match";
    } else {
        confirmError.innerText = "";
    }
});

/* ------------------------------
PHONE VALIDATION
------------------------------ */

phone.addEventListener("input", () => {

    const phoneError = document.getElementById("phoneError");

    const npPhoneRegex = /^(98|97)\d{8}$/;

    if (!npPhoneRegex.test(phone.value)) {
        phoneError.innerText = "Enter valid Nepali mobile number";
    } else {
        phoneError.innerText = "";
    }
});

/* ------------------------------
EMAIL VALIDATION
------------------------------ */

email.addEventListener("input", () => {

    const emailError = document.getElementById("emailError");

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email.value)) {
        emailError.innerText = "Enter valid email address";
    } else {
        emailError.innerText = "";
    }
});

/* ------------------------------
PASSWORD TOGGLE
------------------------------ */

document.getElementById("togglePassword")
.addEventListener("click", () => {

    if (password.type === "password") {
        password.type = "text";
    } else {
        password.type = "password";
    }
});

/* ------------------------------
FORM SUBMIT
------------------------------ */

registerForm.addEventListener("submit", (e) => {

    e.preventDefault();

    btnText.classList.add("hidden");
    btnLoader.classList.remove("hidden");

    setTimeout(() => {

        showToast("Registration Successful!", "success");

        btnText.classList.remove("hidden");
        btnLoader.classList.add("hidden");

        registerForm.submit();

    }, 2000);
});

/* ------------------------------
TOAST
------------------------------ */

function showToast(message, type) {

    toast.innerText = message;

    toast.classList.remove("hidden");

    if (type === "success") {
        toast.className =
            "fixed top-5 right-5 px-6 py-4 rounded-2xl shadow-2xl text-white bg-emerald-500 z-50";
    }

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}

/* ------------------------------
 DARK MODE
 ------------------------------ */

const themeToggle = document.getElementById("themeToggle");
if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        document.documentElement.classList.toggle("dark");
    });
}
>>>>>>> origin/sakina-maharjan

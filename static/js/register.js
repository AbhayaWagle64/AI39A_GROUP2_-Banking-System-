const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const strengthBar = document.getElementById("strengthBar");
const strengthText = document.getElementById("strengthText");
const registerForm = document.getElementById("registerForm");
const btnText = document.getElementById("btnText");
const btnLoader = document.getElementById("btnLoader");
const toast = document.getElementById("toast");

/* ------------------------------
   PASSWORD STRENGTH MONITOR
------------------------------ */
password.addEventListener("input", () => {
    const value = password.value;
    let strength = 0;
    if (value.length >= 8) strength++;
    if (/[A-Z]/.test(value)) strength++;
    if (/[0-9]/.test(value)) strength++;
    if (/[^A-Za-z0-9]/.test(value)) strength++;
    switch (strength) {
        case 0:
            strengthBar.style.width = "0%";
            strengthBar.className = "h-full bg-slate-400 transition-all duration-500 ease-out";
            strengthText.innerText = "Password Requirements: At least 8 characters.";
            strengthText.className = "text-xs text-slate-400 mt-1 font-medium";
            break;
        case 1:
            strengthBar.style.width = "25%";
            strengthBar.className = "h-full bg-rose-500 transition-all duration-500 ease-out";
            strengthText.innerText = "Weak Password";
            strengthText.className = "text-xs text-rose-400 mt-1 font-semibold";
            break;
        case 2:
            strengthBar.style.width = "50%";
            strengthBar.className = "h-full bg-amber-500 transition-all duration-500 ease-out";
            strengthText.innerText = "Medium Strength";
            strengthText.className = "text-xs text-amber-400 mt-1 font-semibold";
            break;
        case 3:
        case 4:
            strengthBar.style.width = "100%";
            strengthBar.className = "h-full bg-emerald-500 transition-all duration-500 ease-out";
            strengthText.innerText = "Strong Secure Password";
            strengthText.className = "text-xs text-emerald-400 mt-1 font-semibold";
            break;
    }
});

/* ------------------------------
   REAL-TIME CONFIRM PASSWORD MATCH
------------------------------ */
if (!document.getElementById("matchIndicator")) {
    const matchDiv = document.createElement("div");
    matchDiv.id = "matchIndicator";
    matchDiv.className = "hidden";
    confirmPassword.parentElement.appendChild(matchDiv);
}

confirmPassword.addEventListener("input", () => {
    const matchIndicator = document.getElementById("matchIndicator");
    if (!matchIndicator) return;
    if (confirmPassword.value === "") {
        matchIndicator.className = "hidden";
    } else if (password.value === confirmPassword.value) {
        matchIndicator.innerHTML = '<i class="fa-solid fa-check-circle text-emerald-400 mr-1"></i> Passwords match';
        matchIndicator.className = "text-xs text-emerald-400 mt-1 font-medium flex items-center";
    } else {
        matchIndicator.innerHTML = '<i class="fa-solid fa-circle-xmark text-rose-400 mr-1"></i> Passwords do not match';
        matchIndicator.className = "text-xs text-rose-400 mt-1 font-medium flex items-center";
    }
});

/* ------------------------------
   PHONE VALIDATION (NEPALI FORMAT)
------------------------------ */
const phoneInput = document.getElementById("phone");
if (phoneInput) {
    phoneInput.addEventListener("input", () => {
        const phoneRegex = /^(98|97)\d{8}$/;
        const isValid = phoneRegex.test(phoneInput.value);
        if (phoneInput.value && !isValid) {
            phoneInput.classList.add("border-rose-400");
            phoneInput.classList.remove("border-slate-200", "dark:border-slate-700");
        } else {
            phoneInput.classList.remove("border-rose-400");
            phoneInput.classList.add("border-slate-200", "dark:border-slate-700");
        }
    });
}

/* ------------------------------
   SUBMISSION EVENT WORKFLOWS
------------------------------ */
registerForm.addEventListener("submit", (e) => {
    const name = document.querySelector('input[name="name"]')?.value.trim();
    const email = document.getElementById("email")?.value.trim();
    const phone = document.getElementById("phone")?.value.trim();

    if (!name || name.length < 2) {
        e.preventDefault();
        showToast("Please enter your full name (minimum 2 characters).", "error");
        shakeElement(document.querySelector('input[name="name"]'));
        return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
        e.preventDefault();
        showToast("Please enter a valid email address.", "error");
        shakeElement(document.getElementById("email"));
        return;
    }

    const phoneRegex = /^(98|97)\d{8}$/;
    if (!phone || !phoneRegex.test(phone)) {
        e.preventDefault();
        showToast("Please enter a valid Nepali phone number (98/97 + 8 digits).", "error");
        shakeElement(document.getElementById("phone"));
        return;
    }

    if (password.value !== confirmPassword.value) {
        e.preventDefault();
        showToast("Passwords do not match. Please verify both fields.", "error");
        shakeElement(confirmPassword);
        return;
    }

    if (password.value.length < 8) {
        e.preventDefault();
        showToast("Password must be at least 8 characters long.", "error");
        shakeElement(password);
        return;
    }

    btnText.innerText = "Processing Setup...";
    btnLoader.classList.remove("hidden");
    document.getElementById("submitBtn").disabled = true;
});

function shakeElement(element) {
    if (!element) return;
    element.classList.add("animate-shake");
    setTimeout(() => element.classList.remove("animate-shake"), 500);
}

function showToast(message, type = "info") {
    toast.className = "fixed top-5 right-5 px-6 py-4 rounded-2xl shadow-2xl text-white z-50 transform transition-all duration-300 font-medium text-sm";
    if (type === "success") {
        toast.classList.add("bg-emerald-500");
    } else if (type === "error") {
        toast.classList.add("bg-rose-500");
    } else {
        toast.classList.add("bg-blue-500");
    }
    toast.innerText = message;
    toast.classList.remove("hidden");
    requestAnimationFrame(() => {
        toast.classList.add("translate-x-0", "opacity-100");
        toast.classList.remove("translate-x-full", "opacity-0");
    });
    setTimeout(() => {
        toast.classList.add("translate-x-full", "opacity-0");
        toast.classList.remove("translate-x-0", "opacity-100");
        setTimeout(() => toast.classList.add("hidden"), 300);
    }, 4000);
}

/* ------------------------------
   THEME TOGGLE
------------------------------ */
const themeToggleBtn = document.getElementById("toggleTheme");
if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
        const isDark = document.documentElement.classList.toggle("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");
        const icon = themeToggleBtn.querySelector("i");
        if (icon) {
            icon.className = isDark ? "fa-solid fa-sun text-amber-400" : "fa-solid fa-moon text-slate-400";
        }
    });
    const isDark = document.documentElement.classList.contains("dark");
    const icon = themeToggleBtn.querySelector("i");
    if (icon) {
        icon.className = isDark ? "fa-solid fa-sun text-amber-400" : "fa-solid fa-moon text-slate-400";
    }
}

if (localStorage.getItem("theme") === "dark" || 
    (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.classList.add("dark");
} else {
    document.documentElement.classList.remove("dark");
}

/* ------------------------------
   PASSWORD TOGGLES
------------------------------ */
document.getElementById("togglePassword").addEventListener("click", function() {
    const icon = this.querySelector('i');
    if (password.type === "password") {
        password.type = "text";
        icon.className = "fa-solid fa-eye-slash text-sm text-emerald-400";
    } else {
        password.type = "password";
        icon.className = "fa-solid fa-eye text-sm text-slate-400";
    }
});

const toggleConfirmBtn = document.getElementById("toggleConfirmPassword");
if (toggleConfirmBtn) {
    toggleConfirmBtn.addEventListener("click", function() {
        const icon = this.querySelector('i');
        if (confirmPassword.type === "password") {
            confirmPassword.type = "text";
            icon.className = "fa-solid fa-eye-slash text-sm text-emerald-400";
        } else {
            confirmPassword.type = "password";
            icon.className = "fa-solid fa-eye text-sm text-slate-400";
        }
    });
} else {
    const confirmWrapper = confirmPassword.parentElement;
    if (confirmWrapper) {
        const toggleBtn = document.createElement("button");
        toggleBtn.type = "button";
        toggleBtn.id = "toggleConfirmPassword";
        toggleBtn.className = "absolute right-3 top-9 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200";
        toggleBtn.innerHTML = '<i class="fa-solid fa-eye text-sm"></i>';
        confirmWrapper.style.position = "relative";
        confirmWrapper.appendChild(toggleBtn);
        toggleBtn.addEventListener("click", function() {
            const icon = this.querySelector('i');
            if (confirmPassword.type === "password") {
                confirmPassword.type = "text";
                icon.className = "fa-solid fa-eye-slash text-sm text-emerald-400";
            } else {
                confirmPassword.type = "password";
                icon.className = "fa-solid fa-eye text-sm text-slate-400";
            }
        });
    }
}
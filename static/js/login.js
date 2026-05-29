document.addEventListener("DOMContentLoaded", () => {

    // =========================
    // Dark Mode Toggle
    // =========================

    const themeToggle =
        document.getElementById("themeToggle");

    if(themeToggle){

        themeToggle.addEventListener("click", () => {

            document.documentElement.classList.toggle("dark");

        });
    }


    // =========================
    // Show / Hide Password
    // =========================

    const passwordInput =
        document.getElementById("password");

    const togglePassword =
        document.getElementById("togglePassword");

    if(togglePassword){

        togglePassword.addEventListener("click", () => {

            const type =
                passwordInput.getAttribute("type") === "password"
                ? "text"
                : "password";

            passwordInput.setAttribute("type", type);

            togglePassword.innerHTML =
                type === "password"
                ? '<i class="fa-solid fa-eye"></i>'
                : '<i class="fa-solid fa-eye-slash"></i>';

        });
    }


    // =========================
    // Form Validation
    // =========================

    const loginForm =
        document.getElementById("loginForm");

    const emailInput =
        document.getElementById("email");

    const emailError =
        document.getElementById("emailError");

    const passwordError =
        document.getElementById("passwordError");


    if(loginForm){

        loginForm.addEventListener("submit", (e) => {

            let valid = true;

            // Reset Errors
            emailError.innerText = "";
            passwordError.innerText = "";


            // Email Validation
            if(emailInput.value.trim() === ""){

                emailError.innerText =
                    "Email is required";

                valid = false;
            }


            // Password Validation
            if(passwordInput.value.trim() === ""){

                passwordError.innerText =
                    "Password is required";

                valid = false;
            }


            // Prevent Submit
            if(!valid){
                e.preventDefault();
                return;
            }


            // =========================
            // Button Loader
            // =========================

            const btnText =
                document.getElementById("btnText");

            const btnLoader =
                document.getElementById("btnLoader");

            if(btnText && btnLoader){

                btnText.classList.add("hidden");

                btnLoader.classList.remove("hidden");
            }

        });

    }


    // =========================
    // Toast Notification
    // =========================

    function showToast(message, color="green") {

        const toast =
            document.getElementById("toast");

        if(!toast) return;

        toast.innerText = message;

        toast.className =
            `fixed top-5 right-5 px-6 py-4 rounded-2xl shadow-2xl text-white z-50 bg-${color}-500`;

        toast.classList.remove("hidden");

        setTimeout(() => {
            toast.classList.add("hidden");
        }, 3000);
    }

});
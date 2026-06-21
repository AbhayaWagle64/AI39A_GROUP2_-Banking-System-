document.addEventListener("DOMContentLoaded", () => {

    const fileInput = document.getElementById("profile_image");
    const preview = document.getElementById("avatarPreview");
    const labelBtn = document.querySelector(".avatar-edit-btn");

    if (fileInput && preview) {

        fileInput.addEventListener("change", (e) => {

            const file = e.target.files[0];

            if (file) {

                if (preview._oldObjectUrl) {
                    URL.revokeObjectURL(preview._oldObjectUrl);
                }

                const objectUrl = URL.createObjectURL(file);
                preview.src = objectUrl;
                preview._oldObjectUrl = objectUrl;
                preview.classList.remove("avatar-default-fit");

                if (labelBtn) {
                    labelBtn.innerHTML = '<span class="upload-icon">\uD83D\uDCC1</span> ' + file.name;
                }
            }
        });
    }

    const form = document.querySelector(".pm-form-inner");
    const passwordInput = document.querySelector("input[name='password']");
    const strengthEl = document.querySelector(".password-strength");
    const strengthBar = document.querySelector(".password-strength-bar");

    if (passwordInput && strengthEl && strengthBar) {

        passwordInput.addEventListener("input", (e) => {

            const val = e.target.value;

            if (val.length === 0) {
                strengthEl.classList.remove("active");
                strengthBar.className = "password-strength-bar";
                return;
            }

            strengthEl.classList.add("active");

            if (val.length < 6) {
                strengthBar.className = "password-strength-bar weak";
            } else if (val.length < 10) {
                strengthBar.className = "password-strength-bar medium";
            } else {
                strengthBar.className = "password-strength-bar strong";
            }
        });
    }

    if (form) {
        form.addEventListener("submit", (e) => {

            const pw = document.querySelector("input[name='password']")?.value || "";
            const cpw = document.querySelector("input[name='confirm_password']")?.value || "";

            if (pw && pw !== cpw) {

                e.preventDefault();

                alert("Passwords do not match. Please try again.");

                return false;
            }
        });
    }
<<<<<<< HEAD
=======

>>>>>>> abhaya-wagle
});


// PROFILE IMAGE PREVIEW


const profileImageInput = document.getElementById("profileImage");
const profilePreview = document.getElementById("profilePreview");
const profilePlaceholder = document.getElementById("profilePlaceholder");

// Set placeholder initial from the displayed name (falls back to 'J')
const displayNameEl = document.querySelector('.profile-details h2');
const displayName = displayNameEl ? displayNameEl.textContent.trim() : (document.getElementById('fullName')?.value || '');
const initial = displayName ? displayName.charAt(0).toUpperCase() : 'J';
if (profilePlaceholder) profilePlaceholder.textContent = initial;

function updateAvatarVisibility(){
    const src = profilePreview && profilePreview.src ? profilePreview.src : '';

    if (src.includes('default-profile.png') || src === '' ){
        if (profilePreview) profilePreview.style.display = 'none';
        if (profilePlaceholder) profilePlaceholder.style.display = 'flex';
    } else {
        if (profilePreview) profilePreview.style.display = 'block';
        if (profilePlaceholder) profilePlaceholder.style.display = 'none';
    }
}

// Initialize visibility on load
updateAvatarVisibility();

profileImageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (file) {

        // Validate image type
        const allowedTypes = ["image/jpeg", "image/png", "image/jpg"];

        if (!allowedTypes.includes(file.type)) {
            alert("Only JPG, JPEG, and PNG files are allowed.");
            profileImageInput.value = "";
            return;
        }

        // Validate file size (2MB max)
        if (file.size > 2 * 1024 * 1024) {
            alert("Image size must be less than 2MB.");
            profileImageInput.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            profilePreview.src = e.target.result;
            // Show uploaded image and hide placeholder
            if (profilePreview) profilePreview.style.display = 'block';
            if (profilePlaceholder) profilePlaceholder.style.display = 'none';
        };

        reader.readAsDataURL(file);
    }
});


// PASSWORD VALIDATION


const newPassword = document.getElementById("newPassword");
const confirmPassword = document.getElementById("confirmPassword");

function validatePasswordMatch() {

    if (newPassword.value !== confirmPassword.value) {

        confirmPassword.setCustomValidity("Passwords do not match");

    } else {

        confirmPassword.setCustomValidity("");
    }
}

newPassword.addEventListener("keyup", validatePasswordMatch);
confirmPassword.addEventListener("keyup", validatePasswordMatch);


// PHONE NUMBER VALIDATION


const phoneInput = document.getElementById("phone");

phoneInput.addEventListener("input", function () {

    // Remove non-numeric characters
    this.value = this.value.replace(/\D/g, '');

    // Limit to 10 digits
    if (this.value.length > 10) {
        this.value = this.value.slice(0, 10);
    }
});


// DATE OF BIRTH VALIDATION


const dobInput = document.getElementById("dob");

dobInput.addEventListener("change", function () {

    const selectedDate = new Date(this.value);
    const today = new Date();

    let age = today.getFullYear() - selectedDate.getFullYear();

    const monthDifference = today.getMonth() - selectedDate.getMonth();

    if (
        monthDifference < 0 ||
        (monthDifference === 0 && today.getDate() < selectedDate.getDate())
    ) {
        age--;
    }

    // Minimum age restriction
    if (age < 18) {

        alert("You must be at least 18 years old.");

        this.value = "";
    }
});


// FORM VALIDATION


const profileForm = document.getElementById("profileForm");

profileForm.addEventListener("submit", function (event) {

    // Prevent default form submission initially
    event.preventDefault();

    // Get all required inputs
    const requiredFields = profileForm.querySelectorAll("[required]");

    let isValid = true;

    requiredFields.forEach(field => {

        if (!field.value.trim()) {

            field.style.borderColor = "#ef4444";
            isValid = false;

        } else {

            field.style.borderColor = "#22c55e";
        }
    });

    // Password strength validation
    if (newPassword.value.length > 0) {

        const passwordRegex =
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{6,}$/;

        if (!passwordRegex.test(newPassword.value)) {

            alert(
                "Password must contain:\n\n" +
                "- At least 6 characters\n" +
                "- One uppercase letter\n" +
                "- One lowercase letter\n" +
                "- One number\n" +
                "- One special character"
            );

            isValid = false;
        }
    }

    // Check password match
    if (newPassword.value !== confirmPassword.value) {

        alert("Passwords do not match.");
        isValid = false;
    }

    // Username validation
    const username = document.getElementById("username").value;

    const usernameRegex = /^[a-zA-Z0-9_]+$/;

    if (!usernameRegex.test(username)) {

        alert(
            "Username can only contain letters, numbers, and underscores."
        );

        isValid = false;
    }

    // Final submission
    if (isValid) {

        alert("Profile updated successfully!");

        // Uncomment this when backend is ready
        // profileForm.submit();
    }
});

// Real time input styling

const allInputs = document.querySelectorAll(
    "input, textarea, select"
);

allInputs.forEach(input => {

    input.addEventListener("input", function () {

        if (this.checkValidity()) {

            this.style.borderColor = "#22c55e";

        } else {

            this.style.borderColor = "#ef4444";
        }
    });
});

// Reset button functionality

const resetButton = document.querySelector(".reset-btn");

resetButton.addEventListener("click", function () {

    setTimeout(() => {

        // Reset border colors
        allInputs.forEach(input => {
            input.style.borderColor = "#d1d5db";
        });

        // Reset profile image
        profilePreview.src = "/static/images/default-profile.png";
        // Toggle visibility back to placeholder
        if (profilePreview) profilePreview.style.display = 'none';
        if (profilePlaceholder) profilePlaceholder.style.display = 'flex';

    }, 100);
});

// Auto hide alert messages

function showMessage(message, type = "success") {

    const messageBox = document.createElement("div");

    messageBox.classList.add("message-box");

    messageBox.innerText = message;

    messageBox.style.position = "fixed";
    messageBox.style.top = "20px";
    messageBox.style.right = "20px";
    messageBox.style.padding = "15px 20px";
    messageBox.style.borderRadius = "10px";
    messageBox.style.color = "white";
    messageBox.style.fontWeight = "500";
    messageBox.style.zIndex = "9999";

    if (type === "success") {
        messageBox.style.background = "#22c55e";
    } else {
        messageBox.style.background = "#ef4444";
    }

    document.body.appendChild(messageBox);

    setTimeout(() => {
        messageBox.remove();
    }, 3000);
}
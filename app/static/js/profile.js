document.addEventListener("DOMContentLoaded", () => {

    const avatar = document.querySelector(".profile-avatar");

    if (avatar && avatar.classList.contains("avatar-blur")) {
        avatar.style.cursor = "pointer";
        avatar.title = "Tap to upload a profile photo";
        avatar.addEventListener("click", () => {
            window.location.href = "/profile-management";
        });
    }

});

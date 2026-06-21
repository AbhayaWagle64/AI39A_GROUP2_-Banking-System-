document.addEventListener("DOMContentLoaded", () => {
    const logoutLinks = document.querySelectorAll(".logout-link");
    const modal = document.getElementById("logoutModal");
    const cancel = document.getElementById("modalCancel");

    logoutLinks.forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();
            if (modal) modal.style.display = "flex";
        });
    });

    if (cancel) {
        cancel.addEventListener("click", () => {
            if (modal) modal.style.display = "none";
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("logoutModal");
    const cancelBtn = document.getElementById("modalCancel");
    const logoutLinks = document.querySelectorAll(".logout-link");

    function openModal(e) {
        e.preventDefault();
        modal.classList.add("active");
    }

    function closeModal() {
        modal.classList.remove("active");
    }

    logoutLinks.forEach(link => link.addEventListener("click", openModal));
    cancelBtn.addEventListener("click", closeModal);

    modal.addEventListener("click", (e) => {
        if (e.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && modal.classList.contains("active")) {
            closeModal();
        }
    });

    document.querySelectorAll(".nav-links a").forEach(link => {
        const href = link.getAttribute("href");
        if (href && window.location.pathname === href.split("?")[0] && href !== "/logout") {
            link.classList.add("active");
        }
    });

    document.querySelectorAll(".mobile-nav-item").forEach(link => {
        const href = link.getAttribute("href");
        if (href && window.location.pathname === href.split("?")[0] && href !== "/logout") {
            link.classList.add("active");
        }
    });

});

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".nav-links a").forEach(link => {
        const href = link.getAttribute("href");
        if (href && window.location.pathname === href.split("?")[0]) {
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

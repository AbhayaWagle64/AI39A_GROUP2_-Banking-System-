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
 
    const qrCodeBtn = document.getElementById("qrCodeBtn");
    const qrCodeModal = document.getElementById("qrCodeModal");
    const qrImage = document.getElementById("qrImage");
    const closeQrModal = document.getElementById("closeQrModal");
    const downloadQr = document.getElementById("downloadQr");
 
    if (qrCodeBtn) {
        qrCodeBtn.addEventListener("click", () => {
            qrImage.src = "/qr-code?" + new Date().getTime();
            qrCodeModal.classList.add("active");
        });
    }
 
    if (closeQrModal) {
        closeQrModal.addEventListener("click", () => {
            qrCodeModal.classList.remove("active");
        });
    }
 
    if (qrCodeModal) {
        qrCodeModal.addEventListener("click", (e) => {
            if (e.target === qrCodeModal) {
                qrCodeModal.classList.remove("active");
            }
        });
    }
 
    if (downloadQr && qrImage) {
        downloadQr.addEventListener("click", () => {
            const link = document.createElement("a");
            link.href = qrImage.src;
            link.download = "epaisa-qr-code.png";
            link.click();
        });
    }
 
    const scanQrBtn = document.getElementById("scanQrBtn");
    const qrScannerModal = document.getElementById("qrScannerModal");
    const closeScannerModal = document.getElementById("closeScannerModal");
    const scannerVideo = document.getElementById("scannerVideo");
    const scannerPlaceholder = document.getElementById("scannerPlaceholder");
    
    function isMobileScreen() {
        return window.matchMedia("(max-width: 768px)").matches;
    }
    
    async function waitForJsQr() {
        return new Promise((resolve) => {
            if (typeof jsQR !== 'undefined') {
                resolve();
            } else {
                const checkInterval = setInterval(() => {
                    if (typeof jsQR !== 'undefined') {
                        clearInterval(checkInterval);
                        resolve();
                    }
                }, 100);
                setTimeout(() => {
                    clearInterval(checkInterval);
                    resolve();
                }, 3000);
            }
        });
    }
    
    async function startScanner() {
        if (scannerPlaceholder) scannerPlaceholder.style.display = "none";
        if (!scannerVideo) return;
        
        await waitForJsQr();
        
        if (typeof jsQR === 'undefined') {
            if (scannerPlaceholder) {
                scannerPlaceholder.textContent = "Scanner library not loaded. Please refresh.";
                scannerPlaceholder.style.display = "flex";
            }
            return;
        }
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: "environment" } 
            });
            scannerVideo.style.display = "block";
            scannerVideo.srcObject = stream;
            await scannerVideo.play();
            
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            
            function scanFrame() {
                if (!scannerVideo.srcObject) return;
                
                canvas.width = scannerVideo.videoWidth;
                canvas.height = scannerVideo.videoHeight;
                ctx.drawImage(canvas, 0, 0);
                
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(imageData.data, imageData.width, imageData.height);
                
                if (code) {
                    stopScanner();
                    handleScannedCode(code.data);
                    return;
                }
                
                requestAnimationFrame(scanFrame);
            }
            
            setTimeout(scanFrame, 500);
        } catch (err) {
            if (scannerPlaceholder) {
                scannerPlaceholder.textContent = "Camera access denied. Please allow camera permission.";
                scannerPlaceholder.style.display = "flex";
            }
        }
    }
    
    function stopScanner() {
        if (scannerVideo && scannerVideo.srcObject) {
            const stream = scannerVideo.srcObject;
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            scannerVideo.srcObject = null;
            scannerVideo.style.display = "none";
        }
        if (qrScannerModal) qrScannerModal.classList.remove("active");
    }
    
    async function handleScannedCode(scannedData) {
        const token = document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        if (token) headers['X-CSRFToken'] = token;
        
        try {
            const res = await fetch('/api/lookup-user', {
                method: 'POST',
                headers,
                credentials: 'same-origin',
                body: JSON.stringify({ epaisa_id: scannedData })
            });
            const data = await res.json();
            
            if (data.success) {
                window.location.href = `/wallet?to=${encodeURIComponent(data.epaisa_id)}&name=${encodeURIComponent(data.username)}`;
            } else {
                alert(data.message || "User not found");
            }
        } catch (err) {
            alert("Error scanning QR code");
        }
    }
    
    function initScannerBtnVisibility() {
        if (scanQrBtn) {
            scanQrBtn.style.display = isMobileScreen() ? "flex" : "none";
        }
    }
    
    if (scanQrBtn) {
        initScannerBtnVisibility();
        window.addEventListener("resize", initScannerBtnVisibility);
        
        scanQrBtn.addEventListener("click", () => {
            qrScannerModal.classList.add("active");
            startScanner();
        });
    }
    
    if (closeScannerModal) {
        closeScannerModal.addEventListener("click", stopScanner);
    }
    
    if (qrScannerModal) {
        qrScannerModal.addEventListener("click", (e) => {
            if (e.target === qrScannerModal) {
                stopScanner();
            }
        });
    }
});

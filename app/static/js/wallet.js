document.addEventListener("DOMContentLoaded", () => {
    const epaisaNumber = document.getElementById("epaisaNumber");
    const accountHolder = document.getElementById("accountHolder");
    const amount = document.getElementById("amount");
    const sendMoneyForm = document.getElementById("sendMoneyForm");
    const epaisaError = document.getElementById("epaisaError");
    const amountError = document.getElementById("amountError");
    const confirmModal = document.getElementById("confirmModal");
    const confirmYes = document.getElementById("confirmYes");
    const confirmNo = document.getElementById("confirmNo");
    const confirmMessage = document.getElementById("confirmMessage");
 
    const urlParams = new URLSearchParams(window.location.search);
    const toEpaisa = urlParams.get("to");
    const toName = urlParams.get("name");
    
    if (toEpaisa && epaisaNumber) {
        epaisaNumber.value = toEpaisa;
    }
    if (toName && accountHolder) {
        accountHolder.value = toName;
    }
    
    let pendingFormData = null;
    
    function getCsrfToken() {
        const meta = document.querySelector('meta[name=csrf-token]');
        return meta ? meta.getAttribute('content') : '';
    }
 
    async function startTransaction() {
        const token = getCsrfToken();
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        if (token) headers['X-CSRFToken'] = token;
        const res = await fetch('/api/send-money', {
            method: 'POST',
            headers,
            credentials: 'same-origin',
            body: JSON.stringify(pendingFormData)
        });
        return res.json();
    }
 
    async function requestOtp() {
        const token = getCsrfToken();
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        if (token) headers['X-CSRFToken'] = token;
        const res = await fetch('/api/request-otp', { method: 'POST', headers, credentials: 'same-origin', body: JSON.stringify({}) });
        return res.json();
    }
 
    async function verifyOtp(code) {
        const token = getCsrfToken();
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        if (token) headers['X-CSRFToken'] = token;
        const res = await fetch('/api/verify-otp', { method: 'POST', headers, credentials: 'same-origin', body: JSON.stringify({ otp: code }) });
        return res.json();
    }
 
    function navigateTo(path) {
        window.location.href = path;
    }
 
    sendMoneyForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const epaisaVal = epaisaNumber.value.trim();
        const accountHolderVal = accountHolder.value.trim();
        const amountVal = amount.value;
        
        if (!epaisaVal) {
            epaisaError.textContent = "Recipient ePaisa ID is required";
            epaisaError.className = "field-hint error";
            return;
        }
        
        const amt = parseFloat(amountVal);
        if (isNaN(amt) || amt <= 0) {
            amountError.textContent = "Amount must be greater than 0";
            amountError.className = "field-hint error";
            return;
        }
        
        pendingFormData = {
            epaisaNumber: epaisaVal,
            accountHolder: accountHolderVal,
            amount: amt
        };
        
        confirmMessage.innerHTML = `Are you sure you want to make the transaction?<br><br><small>Send ₹ ${amt.toFixed(2)} to <strong>${accountHolderVal}</strong> (${epaisaVal})?</small>`;
        confirmModal.style.display = "flex";
    });
 
    confirmNo.addEventListener("click", () => {
        confirmModal.style.display = "none";
        pendingFormData = null;
    });
 
    confirmModal.addEventListener("click", (e) => {
        if (e.target === confirmModal) {
            confirmModal.style.display = "none";
            pendingFormData = null;
        }
    });
 
    confirmYes.addEventListener("click", async (e) => {
        e.stopPropagation();
        e.preventDefault();
        if (!pendingFormData) {
            alert("No pending transaction");
            return;
        }
        confirmYes.disabled = true;
        confirmNo.disabled = true;
        confirmYes.textContent = "Processing...";
 
        try {
            const txRes = await startTransaction();
            if (!txRes.success) {
                alert(txRes.message || "Could not start transaction");
                confirmYes.disabled = false;
                confirmNo.disabled = false;
                confirmYes.textContent = "Yes, Send";
                return;
            }
            if (txRes.next === "otp" || txRes.redirect) {
                confirmYes.textContent = "Sending OTP...";
                const otpRes = await requestOtp();
                if (!otpRes || !otpRes.success) {
                    alert(otpRes?.message || "Could not send OTP email. Please try again.");
                    confirmYes.disabled = false;
                    confirmNo.disabled = false;
                    confirmYes.textContent = "Yes, Send";
                    return;
                }
                confirmModal.style.display = "none";
                navigateTo(otpRes.redirect || txRes.redirect || "/verify-otp");
            }
        } catch (error) {
            alert("Error: " + error.message);
            confirmYes.disabled = false;
            confirmNo.disabled = false;
            confirmYes.textContent = "Yes, Send";
        }
    });
});
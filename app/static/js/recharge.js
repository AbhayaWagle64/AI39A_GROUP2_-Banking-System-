document.addEventListener("DOMContentLoaded", () => {
    const rechargeForm = document.getElementById("rechargeForm");
    const phoneInput = document.getElementById("phone");
    const operatorInput = document.getElementById("operator");
    const amountInput = document.getElementById("rechargeAmount");
    const phoneError = document.getElementById("phoneError");
    const operatorError = document.getElementById("operatorError");
    const amountError = document.getElementById("amountError");

    const confirmModal = document.getElementById("confirmModal");
    const confirmYes = document.getElementById("confirmYes");
    const confirmNo = document.getElementById("confirmNo");
    const confirmMessage = document.getElementById("confirmMessage");

    let pendingFormData = null;

    function getCsrfToken() {
        const meta = document.querySelector('meta[name=csrf-token]');
        return meta ? meta.getAttribute('content') : '';
    }

    async function initiateRecharge() {
        const token = getCsrfToken();
        const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
        if (token) headers['X-CSRFToken'] = token;
        const res = await fetch('/api/initiate-recharge', {
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
        const res = await fetch('/api/request-recharge-otp', { method: 'POST', headers, credentials: 'same-origin', body: JSON.stringify({}) });
        return res.json();
    }

    rechargeForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const phone = phoneInput.value.trim();
        const operator = operatorInput.value;
        const amount = parseFloat(amountInput.value);

<<<<<<< HEAD
        // RESET ERRORS
=======
        // Reset errors
>>>>>>> abhaya-wagle
        phoneError.textContent = "";
        phoneError.className = "field-hint";
        operatorError.textContent = "";
        operatorError.className = "field-hint";
        amountError.textContent = "";
        amountError.className = "field-hint";

<<<<<<< HEAD
        // VALIDATION
=======
        // Validation
>>>>>>> abhaya-wagle
        if (!phone || !/^[0-9]{10}$/.test(phone)) {
            phoneError.textContent = "Enter a valid 10-digit phone number";
            phoneError.className = "field-hint error";
            return;
        }

        if (!operator) {
            operatorError.textContent = "Select an operator";
            operatorError.className = "field-hint error";
            return;
        }

        if (isNaN(amount) || amount < 10) {
            amountError.textContent = "Minimum amount is 10";
            amountError.className = "field-hint error";
            return;
        }

        pendingFormData = {
            phone,
            operator,
            amount
        };

        confirmMessage.innerHTML = `Confirm Mobile Recharge?<br><br><small>Recharge ₹ ${amount.toFixed(2)} for <strong>${phone}</strong> (${operator})?</small>`;
        confirmModal.style.display = "flex";
    });

    if (confirmNo) {
        confirmNo.addEventListener("click", () => {
            confirmModal.style.display = "none";
            pendingFormData = null;
        });
    }

    if (confirmModal) {
        confirmModal.addEventListener("click", (e) => {
            if (e.target === confirmModal) {
                confirmModal.style.display = "none";
                pendingFormData = null;
            }
        });
    }

    if (confirmYes) {
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
                const txRes = await initiateRecharge();
                if (!txRes.success) {
                    alert(txRes.message || "Could not initiate recharge");
                    confirmYes.disabled = false;
                    confirmNo.disabled = false;
                    confirmYes.textContent = "Yes, Recharge";
                    return;
                }
                if (txRes.next === "otp" || txRes.redirect) {
                    confirmYes.textContent = "Sending OTP...";
                    const otpRes = await requestOtp();
                    if (!otpRes || !otpRes.success) {
                        alert(otpRes?.message || "Could not send OTP email. Please try again.");
                        confirmYes.disabled = false;
                        confirmNo.disabled = false;
                        confirmYes.textContent = "Yes, Recharge";
                        return;
                    }
                    confirmModal.style.display = "none";
                    window.location.href = otpRes.redirect || txRes.redirect || "/verify-recharge-otp";
                }
            } catch (error) {
                alert("Error: " + error.message);
                confirmYes.disabled = false;
                confirmNo.disabled = false;
                confirmYes.textContent = "Yes, Recharge";
            }
        });
    }
});
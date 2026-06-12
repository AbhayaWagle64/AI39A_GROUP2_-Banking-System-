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

    let pendingFormData = null;

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

    confirmYes.addEventListener("click", async () => {
        if (!pendingFormData) {
            alert("No form data - pendingFormData is null");
            return;
        }
        const dataToSend = pendingFormData;
        pendingFormData = null;
        confirmModal.style.display = "none";
        confirmYes.disabled = true;
        confirmYes.textContent = "Processing...";

        try {
            const response = await fetch("/api/send-money", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "same-origin",
                body: JSON.stringify(dataToSend)
            });
            const result = await response.json();
            if (result.success) {
                alert("Transfer successful!");
                const balancePill = document.querySelector(".balance-pill");
                if (balancePill) {
                    balancePill.textContent = "₹ " + parseFloat(result.new_balance).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
                }
                sendMoneyForm.reset();
            } else {
                alert(result.message || "Transfer failed");
            }
        } catch (error) {
            alert("Error: " + error.message);
        } finally {
            confirmYes.disabled = false;
            confirmYes.textContent = "Yes, Send";
        }
    });
});
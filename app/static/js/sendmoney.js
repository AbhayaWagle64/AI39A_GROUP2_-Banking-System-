document.addEventListener("DOMContentLoaded", () => {

    const form =
        document.getElementById("sendMoneyForm");

    const receiver =
        document.getElementById("receiver");

    const amount =
        document.getElementById("amount");

    const receiverError =
        document.getElementById("receiverError");

    const amountError =
        document.getElementById("amountError");

    form.addEventListener("submit", (e) => {

        let valid = true;

        receiverError.innerText = "";
        amountError.innerText = "";

        // Receiver Validation
        const nepaliNumber = /^98\d{8}$/;

        if(!nepaliNumber.test(receiver.value)){

            receiverError.innerText =
                "Enter valid Nepali number";

            valid = false;
        }

        // Amount Validation
        if(amount.value <= 0){

            amountError.innerText =
                "Enter valid amount";

            valid = false;
        }

        if(!valid){
            e.preventDefault();
            return;
        }

        // Loader
        const btnText =
            document.getElementById("btnText");

        const btnLoader =
            document.getElementById("btnLoader");

        btnText.classList.add("hidden");

        btnLoader.classList.remove("hidden");

    });
});
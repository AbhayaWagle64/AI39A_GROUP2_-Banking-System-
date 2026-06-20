// Generate User QR Code
document.addEventListener("DOMContentLoaded", function () {

    const qrContainer = document.getElementById("my-qr");

    if (qrContainer && typeof userId !== "undefined") {

        const qrData = JSON.stringify({
            user_id: userId,
            app: "ePaisa"
        });

        new QRCode(qrContainer, {
            text: qrData,
            width: 180,
            height: 180,
            colorDark: "#1a1a2e",
            colorLight: "#ffffff"
        });
    }
});


// Download QR Code
function downloadQR() {

    const canvas =
        document.querySelector("#my-qr canvas");

    if (!canvas) {
        alert("QR not ready.");
        return;
    }

    const link =
        document.createElement("a");

    link.download = "epaisa_qr.png";
    link.href = canvas.toDataURL();

    link.click();
}


// Scan QR Code
async function startScan() {

    const container =
        document.getElementById("scanner-container");

    const video =
        document.getElementById("preview");

    container.style.display = "block";

    try {

        const stream =
            await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: "environment"
                }
            });

        video.srcObject = stream;
        video.play();

        const canvas =
            document.createElement("canvas");

        const ctx =
            canvas.getContext("2d");

        const script =
            document.createElement("script");

        script.src =
            "https://cdnjs.cloudflare.com/ajax/libs/jsqr/1.4.0/jsQR.min.js";

        script.onload = function () {

            const scanner = setInterval(() => {

                if (
                    video.readyState ===
                    video.HAVE_ENOUGH_DATA
                ) {

                    canvas.height =
                        video.videoHeight;

                    canvas.width =
                        video.videoWidth;

                    ctx.drawImage(
                        video,
                        0,
                        0,
                        canvas.width,
                        canvas.height
                    );

                    const imageData =
                        ctx.getImageData(
                            0,
                            0,
                            canvas.width,
                            canvas.height
                        );

                    const code =
                        jsQR(
                            imageData.data,
                            imageData.width,
                            imageData.height
                        );

                    if (code) {

                        clearInterval(scanner);

                        stream
                            .getTracks()
                            .forEach(track =>
                                track.stop()
                            );

                        container.style.display = "none";

                        try {

                            const data =
                                JSON.parse(code.data);

                            if (data.user_id) {

                                document.getElementById(
                                    "receiver-id"
                                ).value =
                                    data.user_id;

                                alert(
                                    "QR scanned successfully!\nUser ID: " +
                                    data.user_id
                                );
                            }

                        } catch {

                            alert(
                                "Invalid QR Code."
                            );
                        }
                    }
                }

            }, 200);
        };

        document.body.appendChild(script);

    } catch (error) {

        alert(
            "Camera access denied or unavailable."
        );

        console.error(error);
    }
}
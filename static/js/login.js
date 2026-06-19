function togglePassword() {
    const passwordInput = document.getElementById("password");
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault(); // evita recargar la página

    const correo = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            correo: correo,
            password: password
        })
    });

    const data = await response.json();

    if (data.status === 1) {
        // guardar token
        localStorage.setItem("token", data.access_token);

        // 🔥 REDIRECCIÓN
        window.location.href = "/home";
    } else {
        alert(data.message);
    }
});
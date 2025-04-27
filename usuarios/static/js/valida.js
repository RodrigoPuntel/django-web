document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        const inputs = form.querySelectorAll("input[required]");
        let valid = true;

        inputs.forEach(input => {
            input.classList.remove("error");
            if (!input.value.trim()) {
                input.classList.add("error");
                valid = false;
            }

            if (input.type === "email" && !input.value.includes("@")) {
                input.classList.add("error");
                valid = false;
            }

            if (input.name.toLowerCase().includes("senha") && input.value.length < 6) {
                input.classList.add("error");
                valid = false;
            }
        });

        if (!valid) {
            e.preventDefault();
            alert("Por favor, preencha todos os campos corretamente.");
        }
    });
});

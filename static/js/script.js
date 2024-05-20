document.addEventListener("DOMContentLoaded", function() {
    // Selecciona el elemento scroll-indicator
    var scrollIndicator = document.getElementById("scroll-indicator");

    // Selecciona el botón "Probar"
    var testButton = document.getElementById("download-button");

    // Función para realizar el desplazamiento suave
    function smoothScrollToSection() {
        // Selecciona el elemento al que quieres desplazarte
        var cardsSection = document.getElementById("cardsSection");

        // Realiza el desplazamiento suave
        cardsSection.scrollIntoView({ behavior: "smooth" });
    }

    // Añade un evento de clic al scroll-indicator
    scrollIndicator.addEventListener("click", smoothScrollToSection);

    // Añade un evento de clic al botón "Probar"
    testButton.addEventListener("click", smoothScrollToSection);
});

  
document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const mainContainer = document.getElementById("main-container");
    const toggleBtn = document.getElementById("toggle-btn");
    const charts = document.querySelectorAll(".chart > div"); // Sélectionner les div des graphiques Plotly

    // Fonction pour redimensionner les graphiques
    function resizeCharts() {
        charts.forEach(chart => {
            Plotly.relayout(chart, { autosize: true }); // Redimensionne chaque graphique
        });
    }

    // Vérifier l'état initial de la sidebar
    if (sidebar.classList.contains("collapsed")) {
        mainContainer.classList.add("collapsed");
        toggleBtn.textContent = "❯";
    } else {
        mainContainer.classList.remove("collapsed");
        toggleBtn.textContent = "❮";
    }

    // Ajouter l'écouteur d'événement pour le bouton toggle
    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
        mainContainer.classList.toggle("collapsed");

        // Inverse le symbole de la flèche
        toggleBtn.textContent = sidebar.classList.contains("collapsed") ? "❯" : "❮";

        // Redimensionner les graphiques après la transition
        setTimeout(resizeCharts, 300); // Attendre la fin de la transition CSS (0.3s)
    });

    // Redimensionner les graphiques au chargement de la page
    resizeCharts();
});


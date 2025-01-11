/* Function to change selected graph */
document.addEventListener("DOMContentLoaded", function () {
    const selector = document.getElementById("graph-selector-num");
    const graphs_num = document.querySelectorAll(".graph-num");

    // Fonction pour afficher le graphique sélectionné
    function showSelectedGraph() {
        const selectedValue = selector.value;
        graphs_num.forEach(graph => {
            if (graph.id === selectedValue.replace(" ", "-").toLowerCase()) {
                graph.classList.add("active");
            } else {
                graph.classList.remove("active");
            }
        });
    }

    // Afficher le premier graphique par défaut
    showSelectedGraph();

    // Ajouter un écouteur d'événement pour le menu déroulant
    selector.addEventListener("change", showSelectedGraph);
});
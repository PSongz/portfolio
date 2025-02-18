document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-link");
    const views = document.querySelectorAll(".view");

    navLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            // Retirer la classe "active" de tous les liens
            navLinks.forEach(link => link.classList.remove("active"));

            // Ajouter la classe "active" au lien cliqué
            this.classList.add("active");

            // Masquer toutes les vues
            views.forEach(view => view.classList.remove("active"));

            // Afficher la vue correspondante
            const viewId = this.dataset.view;
            const activeView = document.getElementById(viewId);
            if (activeView) {
                activeView.classList.add("active");
            }
        });
    });
});
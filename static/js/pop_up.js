document.addEventListener("DOMContentLoaded", function () {
    // Récupérer tous les éléments de la classe recent-work-item
    const workItems = document.querySelectorAll(".gallery-items");

    workItems.forEach((item) => {
        item.addEventListener("click", function () {
            console.log("WAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
            const projectId = this.dataset.id;
            const projectTitle = this.dataset.title;
            const projectDescription = this.dataset.description;
            const projectImage = this.dataset.image;
            const projectUrl = this.dataset.project_url;

            // Debug: Vérifier l'URL dans la console
            console.log("Project URL:", projectUrl);

            // Remplir les données de la pop-up
            document.getElementById("popup-title").textContent = projectTitle;
            document.getElementById("popup-description").textContent = projectDescription;
            document.getElementById("popup-image").src = projectImage;
           
            // Mettre à jour l'URL du bouton "View Data"
            const popupUrlElement = document.getElementById("popup-url");
            if (projectUrl && projectUrl.trim() !== "") {
                popupUrlElement.href = projectUrl; // Assigner l'URL correcte
                popupUrlElement.style.display = "inline-block";
            } else {
                console.error("Invalid project URL:", projectUrl);
                popupUrlElement.style.display = "none"; // Cacher le bouton si aucune URL
            }

            // Afficher la pop-up
            document.getElementById("popup").style.display = "flex";
        });
    });

    // Fermer la pop-up
    document.querySelector(".close").addEventListener("click", function () {
        document.getElementById("popup").style.display = "none";
    });
});



// Assurez-vous que vous avez inclus jQuery dans votre template HTML.

document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const mealId = button.dataset.mealId;
            const addToCartUrl = button.dataset.addToCartUrl;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Envoie d'une requête AJAX POST pour ajouter le repas au panier
            $.ajax({
                url: addToCartUrl,
                method: 'POST',
                data: {
                    meal_id: mealId,
                    csrfmiddlewaretoken: csrfToken,  // Assurez-vous d'inclure le jeton CSRF
                },
                success: function (response) {
                    // Gérer la réponse du serveur (peut inclure une confirmation, une mise à jour du panier, etc.)
                    // Vous pouvez mettre à jour le panier côté client si nécessaire.
                    console.log(response);
                },
                error: function (error) {
                    // Gérer les erreurs de la requête AJAX
                    console.error(error);
                }
            });
        });
    });
});

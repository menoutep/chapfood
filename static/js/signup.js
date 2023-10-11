// script.js

const form = document.getElementById('registration-form');

form.addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone_number').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    // Validation des champs (vous pouvez ajouter des règles de validation personnalisées ici)
    if (username.trim() === '') {
        showError('username-error', 'Le nom d\'utilisateur est requis');
    } else {
        clearError('username-error');
    }

    if (!isValidEmail(email)) {
        showError('email-error', 'Email invalide');
    } else {
        clearError('email-error');
    }

    if (!isValidPhoneNumber(phone)) {
        showError('phone-error', 'Numéro de téléphone invalide');
    } else {
        clearError('phone-error');
    }

    if (password1.length < 6) {
        showError('password1-error', 'Le mot de passe doit avoir au moins 6 caractères');
    } else {
        clearError('password1-error');
    }

    if (password1 !== password2) {
        showError('password2-error', 'Les mots de passe ne correspondent pas');
    } else {
        clearError('password2-error');
    }

    // Si tous les champs sont valides, vous pouvez envoyer le formulaire ici
});

function showError(id, message) {
    const errorElement = document.getElementById(id);
    errorElement.textContent = message;
}

function clearError(id) {
    const errorElement = document.getElementById(id);
    errorElement.textContent = '';
}

function isValidEmail(email) {
    // Ajoutez votre logique de validation d'email ici
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhoneNumber(phone) {
    // Ajoutez votre logique de validation de numéro de téléphone ici
    return /^[0-9]{10}$/.test(phone);
}

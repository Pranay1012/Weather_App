document.getElementById('weatherForm').addEventListener('submit', function() {
    // Show spinner, hide button text
    document.getElementById('submitText').classList.add('d-none');
    document.getElementById('spinner').classList.remove('d-none');

    // Reset animations for cards and icons
    const cards = document.querySelectorAll('.card');
    const icons = document.querySelectorAll('.weather-icon');
    cards.forEach(card => {
        card.style.animation = 'none';
        card.offsetHeight; // Trigger reflow
        card.style.animation = 'fadeIn 0.5s ease-out forwards';
    });
    icons.forEach(icon => {
        icon.style.animation = 'none';
        icon.offsetHeight; // Trigger reflow
        icon.style.animation = 'bounce 0.6s ease-in-out';
    });
});
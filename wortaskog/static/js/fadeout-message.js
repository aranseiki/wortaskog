document.addEventListener('DOMContentLoaded', () => {
    const successMessage = document.getElementById('success-message');
    if (successMessage) {
        // Delay before starting the fade-out
        setTimeout(() => {
            successMessage.style.transition = 'opacity 1s';
            successMessage.style.opacity = '0';
            // Wait for the fade-out transition to complete
            setTimeout(() => {
                // Remove the element from the DOM after fading out
                successMessage.remove();
            }, 1000);
        }, 3000);
    }
});

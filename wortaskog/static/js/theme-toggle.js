// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', () => {
    // Get the theme toggle button
    const themeToggle = document.getElementById('theme-toggle');

    // Check for saved user preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
        themeToggle.textContent = savedTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';
    }

    // Add a click event listener to the button
    themeToggle.addEventListener('click', () => {
        // Get the current theme
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Set the new theme
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        themeToggle.textContent = newTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';

        // Save the user's preference
        localStorage.setItem('theme', newTheme);
    });
});
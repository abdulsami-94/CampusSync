document.addEventListener('DOMContentLoaded', () => {
    // Theme switcher logic
    const themeSwitchers = document.querySelectorAll('.theme-switcher');
    const themeIcon = document.getElementById('theme-icon');

    const setTheme = (theme) => {
        if (theme === 'system') {
            const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', systemTheme);
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
        }

        // Update icon based on selection
        if (themeIcon) {
            if (theme === 'light') themeIcon.textContent = '☀️';
            else if (theme === 'dark') themeIcon.textContent = '🌙';
            else themeIcon.textContent = '💻';
        }
    };

    // Apply theme on load
    const currentTheme = localStorage.getItem('theme') || 'system';
    setTheme(currentTheme);

    // Listen for system theme changes in real-time
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (localStorage.getItem('theme') === 'system' || !localStorage.getItem('theme')) {
            setTheme('system');
        }
    });

    // Handle dropdown clicks
    themeSwitchers.forEach(switcher => {
        switcher.addEventListener('click', (e) => {
            e.preventDefault();
            const theme = switcher.getAttribute('data-theme');
            localStorage.setItem('theme', theme);
            setTheme(theme);
        });
    });
});

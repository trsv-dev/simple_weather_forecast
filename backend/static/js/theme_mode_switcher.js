(() => {
    'use strict'

    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)

    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme()
        if (storedTheme) {
            return storedTheme
        }

        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }

    const setTheme = theme => {
        document.documentElement.setAttribute('data-bs-theme', theme)
        updateButtonText(theme)
    }

    const updateButtonText = (theme) => {
        const button = document.querySelector('#theme-toggle-btn');
        button.textContent = theme === 'light' ? '🌚' : '☀️';
    }

    window.addEventListener('DOMContentLoaded', () => {
        setTheme(getPreferredTheme())

        document.querySelector('#theme-toggle-btn').addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme')
            const newTheme = currentTheme === 'light' ? 'dark' : 'light'
            setStoredTheme(newTheme)
            setTheme(newTheme)
        })
    })
})()

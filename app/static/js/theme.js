const toggle = document.getElementById("themeToggle");
const html = document.documentElement;

toggle.addEventListener("click", () => {
    const theme = html.getAttribute("data-theme") === "light" ? "dark" : "light";
    html.setAttribute("data-theme", theme);
    toggle.textContent = theme === "light" ? "🌙" : "☀";
    localStorage.setItem("theme", theme);
});

const saved = localStorage.getItem("theme");
if (saved) {
    html.setAttribute("data-theme", saved);
    toggle.textContent = saved === "light" ? "🌙" : "☀";
}

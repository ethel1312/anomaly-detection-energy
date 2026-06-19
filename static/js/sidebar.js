function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    const icon = document.getElementById("toggle-icon");

    sidebar.classList.toggle("collapsed");
    mainContent.classList.toggle("expanded");

    if (sidebar.classList.contains("collapsed")) {
        icon.classList.remove("fa-chevron-left");
        icon.classList.add("fa-chevron-right");
    } else {
        icon.classList.remove("fa-chevron-right");
        icon.classList.add("fa-chevron-left");
    }
}
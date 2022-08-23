window.addEventListener("DOMContentLoaded", (e) => {
    document.querySelector('#permaneny-year').innerHTML = new Date().getFullYear();
    // Menu Show and close
    let open_menu = document.querySelector('.main-menu.me-3'),
        show_menu = document.querySelector('.menu-modal-content'),
        close_menu = document.querySelector('.btn.menu-close');
    // Show Menu
    open_menu.addEventListener('click', (e) => {
        show_menu.classList.remove('d-none');
    })
    // Close Menu
    close_menu.addEventListener('click', (e) => {
        show_menu.classList.add('d-none');
    })
})
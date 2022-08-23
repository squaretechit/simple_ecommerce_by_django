window.addEventListener("DOMContentLoaded", (e) => {
    let navigation_bar = document.querySelector('#navigation-bar'),
        bottom_nav = document.querySelector('#bottom-nav'),
        admin_notification = document.querySelector('#admin-notification'),
        notification_body = document.querySelector('#notification-body');
    window.addEventListener("mouseup", (e) => {
        navigation_bar.addEventListener('click', function () {
            bottom_nav.classList.toggle('d-none');
        });
        if (e.target != bottom_nav && e.target.parentNode != bottom_nav){
            bottom_nav.classList.add('d-none');
        }
        admin_notification.addEventListener('click', function(){
            notification_body.classList.toggle('d-none');
        })
        if (e.target != notification_body && e.target.parentNode != notification_body){
            notification_body.classList.add('d-none');
        }
    })
})

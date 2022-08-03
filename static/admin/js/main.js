document.addEventListener('DOMContentLoaded', ()=> {
    const pathname = window.location.pathname;
    const items = Array.prototype.map.call(document.querySelectorAll('nav ul.pcoded-item li'), item => item);

    const liElement = items.find(item => {
        return item.querySelector('a.waves-effect').getAttribute('href').includes(pathname);
    });

    if (liElement) {
        liElement.classList.add('active');
    }
});
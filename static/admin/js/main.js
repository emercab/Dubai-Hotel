document.addEventListener('DOMContentLoaded', async ()=> {
    activateMenu();

    cliente();
});

const activateMenu = () => {
    const pathname = window.location.pathname;
    const items = Array.prototype.map.call(document.querySelectorAll('nav ul.pcoded-item li'), item => item);

    const liElement = items.find(item => {
        return item.querySelector('a.waves-effect').getAttribute('href').includes(pathname);
    });

    if (liElement) {
        liElement.classList.add('active');
    }
}

const cliente = async () => {
    const info = {
        'input1': 'mensaje'
    }

    const opciones = {
        method: 'post',
        body: JSON.stringify(info),
        headers: {
            'Content-Type': 'application/json; charset=utf-8' //se va a retornar
            //'Accept': 'applicacion/json'
        }
    };

    await fetch(`${window.location.origin}/api/clientes`, opciones)
        //.then(response => response.json())
        .then(response => response.text())
        .then(response => {
            console.log(response)
        })
        .catch(err => { 
            console.error(err);
         });
};
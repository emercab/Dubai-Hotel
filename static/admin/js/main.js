document.addEventListener('DOMContentLoaded', () => {
    const txtBusquedaClienteHTML = document.getElementById('txtBusquedaCliente');
    const btnBusquedaClienteHTML = document.getElementById('btnBusquedaCliente');

    if (txtBusquedaClienteHTML) {
        txtBusquedaClienteHTML.addEventListener('keyup', function(e) {
            if (btnBusquedaClienteHTML && e.target) {
                //const txtBusquedaHTML = e.target;
                //const valorBusqueda = txtBusquedaHTML.value;
                const valorBusqueda = txtBusquedaClienteHTML.value;
    
                if (valorBusqueda.trim() !== '') {
                    btnBusquedaClienteHTML.removeAttribute('disabled'); 
                    txtBusquedaClienteHTML.classList.remove('is-invalid');
                } 
                else if (valorBusqueda === '') {
                    const txtClienteHTML = document.getElementById('txtCliente');
                    if (txtClienteHTML) {
                        txtClienteHTML.value = '';
                    }

                    txtBusquedaClienteHTML.classList.remove('is-invalid');
                    btnBusquedaClienteHTML.setAttribute('disabled', 'disabled');
                }
                else {
                    txtBusquedaClienteHTML.classList.add('is-invalid');
                    btnBusquedaClienteHTML.setAttribute('disabled', 'disabled');
                }
            }
        });
    }

    if (btnBusquedaClienteHTML) {
        btnBusquedaClienteHTML.addEventListener('click', function(e){
            if (txtBusquedaClienteHTML) {
                const valorBusqueda = txtBusquedaClienteHTML.value;
                if (valorBusqueda.trim() !== '') {
                    //e.target.classList.remove('is-invalid');
                    btnBusquedaClienteHTML.classList.remove('is-invalid');
    
                    cliente(valorBusqueda);
                } else {
                    //e.target.classList.add('is-invalid');
                    btnBusquedaClienteHTML.add('is-invalid');
                }
            }
        });
    }

    activateMenu();
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

const cliente = async (valorBusqueda) => {
    const data = {
        'cliente': valorBusqueda
    }

    const opciones = {
        method: 'post',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json; charset=utf-8'   
        }
    };

    await fetch(`${window.location.origin}/api/clientes`, opciones)
        .then(response => response.json())
        //.then(response => response.text())
        .then(response => {
            if (typeof response.nombres !== 'undefined') {
                const txtClienteHTML = document.getElementById('txtCliente');

                if (txtClienteHTML) {
                    txtClienteHTML.value = `${response.nombres} ${response.apellidos}`;
                }

                console.log(response)
            }
        })
        .catch(err => { 
            console.error(err);
         });
};
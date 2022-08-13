document.addEventListener('DOMContentLoaded', () => {
    const txtBusquedaClienteHTML = document.getElementById('txtBusquedaCliente');
    const btnBusquedaClienteHTML = document.getElementById('btnBusquedaCliente');
    const txtFechaIngreso = document.getElementById('txtFechaIngreso');
    const txtFechaSalida = document.getElementById('txtFechaSalida');

    if (txtBusquedaClienteHTML) {
        txtBusquedaClienteHTML.addEventListener('keyup', function(e) {
            if (btnBusquedaClienteHTML && e.target) {
                const valorBusqueda = txtBusquedaClienteHTML.value;
                const hiddenReserva = document.getElementById('hiddenReserva');

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
                    hiddenReserva.value = "";
                }
                else {
                    txtBusquedaClienteHTML.classList.add('is-invalid');
                    btnBusquedaClienteHTML.setAttribute('disabled', 'disabled');
                    hiddenReserva.value = "";
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

    const selectHabitacionHTML = document.getElementById('selectHabitacion');
    if (selectHabitacionHTML) {
        selectHabitacionHTML.addEventListener('change', (e) => {
            const target = e.target;
            const valor = Number(target.value);

            if (valor > 0) {
                buscarHabitacion(txtFechaIngreso.value, txtFechaSalida.value, valor)
                .then(response => { 
                    if (response.type === 'ok') {
                        document.getElementById('txtTotalReserva').value = response.response.total;
                    } else {
                        console.log(response.messaga)
                    }
                }).catch(err => {
                    console.log(err);
                });
            }
        });
    }

    $(document).on('change', '.date-field', function() {
        const hora = ' 00:00:00';

        if (txtFechaIngreso && txtFechaSalida) {
            const fechaIngreso = new Date(txtFechaIngreso.value + hora);
            const fechaSalida = new Date(txtFechaSalida.value + hora);

            if (fechaIngreso >= fechaSalida || txtFechaSalida.value === '') {
                fechaIngreso.setDate(fechaIngreso.getDate() + 1);

                const fechaMasUnDia = format(fechaIngreso);
                txtFechaSalida.value = fechaMasUnDia;
            }

            if (txtFechaIngreso.value !== '' && txtFechaSalida.value !== '' && fechaIngreso) {
                buscarHabitacion(txtFechaIngreso.value, txtFechaSalida.value, null).then((response) => {
                    if (response.type == 'ok') {
                        const list_rooms = response.response.list_rooms;
                        cargarHabitacion(list_rooms);
                        document.getElementById('txtTotalReserva').value = '';
                    } else {
                        console.log(response.messaga)
                    }
                }).catch((err) => {
                    console.log('No se encontro habitacion.')
                });
            }

            if (txtFechaIngreso.value === '' || txtFechaSalida.value === '') {
                limpiarHabitacion();
            }
        } else {
            limpiarHabitacion();
        }
    });

    activarMenu();
});

const activarMenu = () => {
    const pathname = window.location.pathname;
    const items = Array.prototype.map.call(document.querySelectorAll('nav ul.pcoded-item li'), item => item);

    const liElement = items.find(item => {
        return item.querySelector('a.waves-effect').getAttribute('href').includes(pathname);
    });

    if (liElement) {
        liElement.classList.add('active');
    }
}

//retorna un formato de fecha valido para los input[type=date]
const format = (date) => {
    const setValue = (value) => {
        return value < 10 ? `0${value}` : value;
    };

    if (date) {
        const newDate = new Date(date);
        let year = newDate.getFullYear();
        let month = setValue(newDate.getMonth() + 1);
        let day = setValue(newDate.getDate());
        const formatDate =  `${year}-${month}-${day}`;

        return formatDate;
    }

    return null;
};

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

    fetch(`${window.location.origin}/api/clientes`, opciones)
        .then(response => response.json())
        //.then(response => response.text())
        .then(response => {
            if (typeof response.nombres !== 'undefined') {
                const txtClienteHTML = document.getElementById('txtCliente');
                const hiddenReserva = document.getElementById('hiddenReserva');

                if (txtClienteHTML && hiddenReserva) {
                    txtClienteHTML.value = `${response.nombres} ${response.apellidos}`;
                    hiddenReserva.value = response.id;
                }
            }
        })
        .catch(err => { 
            console.error(err);
         });
};

const cargarHabitacion = (rooms) => {
    const selectHabitaciones = document.getElementById('selectHabitacion');

    if (selectHabitaciones && rooms.length > 0) {
        const options = rooms.map(room => `<option value="${room.value}">${room.info}</option>`).join('');
        const optionfirst = '<option value="0">Seleccione una habitación</option>';

        selectHabitaciones.innerHTML = null;
        selectHabitaciones.insertAdjacentHTML('beforeend', optionfirst);
        selectHabitaciones.insertAdjacentHTML('beforeend', options);
    }
};

const limpiarHabitacion = () => {
    const selectHabitaciones = document.getElementById('selectHabitacion');

    if (selectHabitaciones) {
        const optionfirst = '<option value="0">Seleccionar una habitación</option>';
        selectHabitaciones.innerHTML = optionfirst;

        document.getElementById('txtTotalReserva').value = '';
    }
};

const buscarHabitacion = async (fecha1, fecha2, habitacionId) => {
    try {
        if (fecha1 && fecha2) {
            console.log(9);
            const data = {
                'fecha1': fecha1,
                'fecha2': fecha2,
                'habitacion_id': habitacionId,
            }
        
            const opciones = {
                method: 'post',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json; charset=utf-8'   
                }
            };
        
            const response = await fetch(`${window.location.origin}/api/info-reserva`, opciones).then(response => response.json())

            return {
                type: 'ok',
                response: response
            }
        }
    
        return { type: 'err', message: 'No se pudo encontrar la habitación.' };
    } catch (err) {
        console.log(err);
        return { type: 'err', message: 'No se pudo encontrar la habitación.' }
    }
};
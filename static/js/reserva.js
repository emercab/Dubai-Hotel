let fecha_inicio = document.getElementById("fecha_inicio");
let fecha_final = document.getElementById("fecha_final");
let selectHabitaciones = document.getElementById("selHabitacionesDisponibles");
let total = document.getElementById("total");

function input_vacio(input) {
    if (input.value.length == 0) {
        return true;
    }
    else {
        return false;
    }
}

function datos_listos() {
    if (input_vacio(fecha_inicio) && input_vacio(fecha_final) && selectHabitaciones.value != -1) {
        return false;
    }
    else {
        return true;
    }
}

const URL_API = 'http://localhost:5005/api/info-reserva';

// Llamo a la función fetch de Node y le mando la url de mi API y
// retorno los datos devueltos por la API
async function fetchData(urlApi) {
    fetch(urlApi)
    const response = await fetch(urlApi);
    const data = await response.json();
    return data;
}

// Función que recibe los datos de la API y los muestra en la página HTML
async function load_total() {
    // Gestiono posibles errores al conectar con la API
    try {
        // Armo la URL de la api con los parámetros que le permitirán
        // calcular el precio de la reserva
        const newUrlAPI = `
            ${URL_API}?fecha1=${fecha_inicio.value}&fecha2=${fecha_final.value}&habitacion_id=${selectHabitaciones.value}
        `;
        // Llamo a la función asíncrona que pide los datos a la API
        const response = await fetchData(newUrlAPI);
        // Valido la respuesta de la API por si hubo error
        if (response.total != 0) {
            // Significa que se recibió el total con éxito y lo muestro
            total.innerText = `Precio: \$ ${response.total.toLocaleString("es-CO")}`;
        }
        else {
            total.innerText = "Precio: No disponible.";
        }
    }
    catch {
        total.innerText = "Precio: No disponible.";
    }
}

function clearSelect() {
    while (selectHabitaciones.options.length > 0) {                
        selectHabitaciones.remove(0);
    }        
}

async function llenarSelect() {
    try {
        // Armo la URL de la api con los parámetros que le permitirán
        // calcular el precio de la reserva
        const newUrlAPI = `
            ${URL_API}?fecha1=${fecha_inicio.value}&fecha2=${fecha_final.value}&habitacion_id=${selectHabitaciones.value}
        `;
        // Llamo a la función asíncrona que pide los datos a la API
        const response = await fetchData(newUrlAPI);
        // Valido que no haya error en la respuesta
        if (response.list_rooms[0].value != -1) {
            clearSelect();
            response.list_rooms.forEach((item) => {
                const option = document.createElement('option');
                option.text = item.info;
                option.value=item.value;
                selectHabitaciones.appendChild(option);
            });
        }  
    }
    catch (error) {
        console.log(error)
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

document.querySelectorAll('#fecha_inicio,#fecha_final').forEach(input => {
    input.addEventListener('change', () => {
        if (fecha_inicio && fecha_final) {
            const fechaIngreso = new Date(fecha_inicio.value + ' 00:00:00');
            const fechaSalida = new Date(fecha_final.value + ' 00:00:00');

            if (fechaIngreso >= fechaSalida || fecha_final.value === '') {
                fechaIngreso.setDate(fechaIngreso.getDate() + 1);

                const fechaMasUnDia = format(fechaIngreso);
                fecha_final.value = fechaMasUnDia;
            }
        }
    });
});

// Hago que se actualice el precio de la reserva cada vez que se haga
// cambios en los controles de fecha y habitaciones
fecha_inicio.addEventListener("blur", () => {
    // Cuando pierda el foco
    if (datos_listos()) {
        load_total();
        llenarSelect();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

fecha_final.addEventListener("blur", () => {
    if (datos_listos()) {
        load_total();
        llenarSelect();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

selectHabitaciones.addEventListener("change", () => {
    if (datos_listos()) {
        load_total();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

// Cargo el total cuando se cargue la página
load_total();

fecha_inicio = document.getElementById("fecha_inicio");
fecha_final = document.getElementById("fecha_final");
habitacion = document.getElementById("selHabitacionesDisponibles");
total = document.getElementById("total");

function input_vacio(input) {
    if (input.value.length == 0) {
        return true;
    }
    else {
        return false;
    }
}

function fechas_listas() {
    if (input_vacio(fecha_inicio) && input_vacio(fecha_final)) {
        return false;
    }
    else {
        return true;
    }
}

const URL_API = 'http://localhost:5005/api/calcular-total-reserva';

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
            ${URL_API}?fecha1=${fecha_inicio.value}&fecha2=${fecha_final.value}&habitacion_id=${habitacion.value}
        `;
        // Llamo a la función asíncrona que pide los datos a la API
        const response = await fetchData(newUrlAPI);
        // Valido la respuesta de la API por si hubo error
        if (response.total != 'error') {
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

// Hago que se actualice el precio de la reserva cada vez que se haga
// cambios en los controles de fecha y habitaciones
fecha_inicio.addEventListener("blur", () => {
    // Cuando pierda el foco
    if (fechas_listas()) {
        load_total();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

fecha_final.addEventListener("blur", () => {
    if (fechas_listas()) {
        load_total();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

habitacion.addEventListener("change", () => {
    if (fechas_listas()) {
        load_total();
    }
    else {
        total.innerText = "Precio: No disponible.";
    }
});

// Cargo el total cuando se cargue la página
load_total();

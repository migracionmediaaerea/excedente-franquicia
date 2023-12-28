// const divCantidad = document.getElementById("div-cantidad");
const divPrecio = document.getElementById("div-precio");

// const cantidadInput = document.getElementById("id_mercancia-cantidad");
const precioInput = document.getElementById("id_mercancia-precio");

// console.log(cantidadInput, precioInput);

function toggleFields(producto) {
    // cantidadInput.value = "";
    precioInput.value = "";
    if (producto.valuable) {
        console.log("if")
        divPrecio.classList.remove("d-none");
        // divCantidad.classList.remove("d-none");
    } else {
        console.log('else')
        divPrecio.classList.add("d-none");
        // divCantidad.classList.remove("d-none");
    }
}

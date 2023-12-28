const medioTransporte = {
    residente: "1",
};

const template = document.getElementById("producto-row-template");
const tbody = document.querySelector("tbody");

const btnAgregarProducto = document.getElementById("agregar-producto-btn");

const unidadesExcedentesInput = document.getElementById("id_mercancia-unidades_excedentes");


// let valorDolar = 20;

const arrProductos = [];
const arrProductoPais = [];

btnAgregarProducto.addEventListener("click", async (event) => {
    document.getElementById("id_medio_transporte").readonly = true;
    beforeAddTable()
    let producto = await getProducto(selectProductos.value);
    let categoria = await getCategoria(producto.categoria);
    // let cantidad = cantidadInput.value;
    let precio = precioInput.value != "" ? precioInput.value : 0;

    if (
        categoria.nombre_categoria == "Vino y bebidas alcohólicas" &&
        producto.medio_transporte == 1
    ) {
        let graduacion = paisesGraduacion.find(
            (e) => e.pais_id === parseInt(selectPais.value)
        );
        console.log("graduacion", graduacion);
        producto.graduacion = selectGraduacion.value;
        producto.tasa_impuesto = graduacion.tasa_impuesto;
        console.log(producto.graduacion, producto.tasa_impuesto);
    } else if (
        categoria.nombre_categoria ==
            "Cigarrillos y otros productos que contienen tabaco" &&
        producto.medio_transporte == 1
    ) {
        let tasa_impuesto = paisesTabaco.find(e => e.pais[0].id == selectPais.value)
        producto.tasa_impuesto = tasa_impuesto.tasa_impuesto

    }
    // console.log('cantidad', cantidad)
    addProductoTable(producto, precio);
});

function addProductoTable(producto, precio) {
    let productoJson = {
        id: producto.id,
        nombre_producto: producto.nombre_producto,
        // cantidad: cantidad,
        precio: precio,
        valor_usd: precio,
        tasa_impuesto: producto.tasa_impuesto ? producto.tasa_impuesto : "0",
        // unidades_excedentes: calcUnidadesExcedentes(producto, cantidad),
        unidades_excedentes: parseInt(unidadesExcedentesInput.value),
        pais_origen: producto.pais_tlc.length > 0 ? selectPais.value : null,
        // graduacion :
    };

    arrProductos.push(productoJson);
    console.log(productoJson);


    renderTable()
}

// function calcUnidadesExcedentes(producto, cantidad) {
//     let unidadesExcedentes = 0;
//     //si es residente entonces siempre que el producto tenga franquicia, se va a la franquicia sin importar la cantidad
//     if (selectMedioTransporte.value == medioTransporte["residente"]) {
//         return calcUnidadesExcedentesResidente(producto, cantidad);
//     } else {
//         return calcUnidadesExcedentesInternacional(producto, cantidad);
//     }
// }

// function calcUnidadesExcedentesResidente(producto, cantidad) {
//     if (producto.infinitos) return 0;
//     let unidadesExcedentes = 0;
//     if (producto.aplica_franquicia) {
//         unidadesExcedentes = cantidad;
//     } else {
//         if (cantidad > producto.cantidad_por_persona) {
//             unidadesExcedentes = cantidad - producto.cantidad_por_persona;
//         }
//     }
//     console.log("excedentes: ", unidadesExcedentes);

//     //tabaco o vino
//     return unidadesExcedentes;
// }

// function calcUnidadesExcedentesInternacional(producto, cantidad) {
//     if (producto.infinitos) return 0;
//     let unidadesExcedentes = 0;
//     if (producto.aplica_franquicia) {
//         if (cantidad > producto.cantidad_por_persona) {
//             unidadesExcedentes = cantidad - producto.cantidad_por_persona;
//         }
//     } else {
//         if (cantidad > producto.cantidad_por_persona) {
//             unidadesExcedentes = cantidad - producto.cantidad_por_persona;
//         }
//     }
//     console.log("excedentes: ", unidadesExcedentes);

//     //tabaco o vino

//     return unidadesExcedentes;
// }

function deleteProducto(element) {
    deleteProductById(element.parentNode.parentNode.dataset.id);
    renderTable();
}

function deleteProductById(id) {
    // alert(id)
    //arrProductos.find(e => e.id == parseInt(id))
    arrProductos.splice(id, 1);
}

function renderTable(){
    tbody.innerHTML = "";

    arrProductos.forEach((e, index) => {
        let templateClone = document.importNode(template.content, true);
        let tds = templateClone.querySelectorAll("td");

        tds[0].textContent = e.nombre_producto;
        // tds[1].textContent = e.cantidad;
        tds[1].textContent = e.precio;
        tds[2].textContent = e.valor_usd;
        tds[3].textContent = e.tasa_impuesto;
        tds[4].textContent = e.unidades_excedentes;

        templateClone.querySelector("tr").dataset.id = index;
        tbody.appendChild(templateClone);
    });
}


function beforeAddTable(){
    let visibles = document.getElementById("div-mercancia").querySelectorAll('div:not(.d-none):not(.mb-3)')
    let invisibles = document.getElementById('div-mercancia').querySelectorAll('.d-none')
    

}


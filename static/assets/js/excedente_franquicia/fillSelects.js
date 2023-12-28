const mediosTransporte = {
    residente: "1",
    terrestre: "2",
    maritimo: "3",
    aereo: "4",
};


const selectCategorias = document.getElementById("id_mercancia-categoria");
const selectSubCategorias = document.getElementById(
    "id_mercancia-subcategoria"
);
const selectProductos = document.getElementById("id_mercancia-producto");
const selectPais = document.getElementById("id_mercancia-pais_origen");
const selectGraduacion = document.getElementById("id_mercancia-graduacion");

const selectMedioTransporte = document.getElementById("id_medio_transporte");

const divSucategorias = document.getElementById("div-subcategoria");
const divProductos = document.getElementById("div-producto");
const divPais = document.getElementById("div-pais");
const divGraduacion = document.getElementById("div-graduacion");
const divUnidadesExcedentes = document.getElementById(
    "div-unidades-excedentes"
);

const divNumVuelo = document.getElementById("div-numero-vuelo");
const divNombreEMbarcacion = document.getElementById("div-nombre-embarcacion");
const divNumeroTransporte = document.getElementById("div-numero-transporte");

const divProcedencia = document.getElementById("div-procedencia");
const divNacionalidad = document.getElementById("div-nacionalidad");
const divResidente = document.getElementById("div-residente");

const checkResidente = document.getElementById("residente-id");
const selectProcedencia = document.getElementById("id_procedencia");
const selectNacionalidad = document.getElementById("id_nacionalidad");

const divMercancia = document.getElementById("div-mercancia");

const divAgregarBtn = document.getElementById("div-btn-agregar");

let graduacionPais = [];
let paisesGraduacion = [];

let paisesTabaco = [];

window.onbeforeunload = function(){
    const excludeIds = [
        "id_mercancia-tipo_cambio",
        "id_identificacion-numero_pasajeros_menores"
    ]
    cleanInputs(excludeIds)
}

document.addEventListener("DOMContentLoaded", async (event) => {
    //campos a excluir de la limpieza
    // const excludeIds = [
    //     "id_mercancia-tipo_cambio",
    //     "id_identificacion-numero_pasajeros_menores"
    // ]
    // cleanInputs(excludeIds)
    categorias = await getCategorias();
    fillCategorias(categorias);
});

selectCategorias.addEventListener("change", async (event) => {
    hideFields(divPrecio);
    // hideFields(divCantidad);
    hideFields(divPais);
    hideFields(divSucategorias);
    hideFields(divProductos);
    hideFields(divUnidadesExcedentes);
    if (selectCategorias.value !== "") {
        let subcatgeorias = await getSubcategorias(selectCategorias.value);
        if (subcatgeorias.length != 0) {
            fillSubcategorias(subcatgeorias);
            showFields(divSucategorias);
            hideFields(divProductos);
            hideFields(divPrecio);
            // hideFields(divCantidad);
            hideFields(divPais);
            hideFields(divGraduacion);
            hideFields(divUnidadesExcedentes);

            divAgregarBtn.classList.add("d-none");
        } else {
            let productos = await getProductsByCat(selectCategorias.value);
            divSucategorias.classList.add("d-none");
            hideFields(divSucategorias);
            showFields(divProductos);
            hideFields(divPrecio);
            // hideFields(divCantidad);
            hideFields(divPais);
            hideFields(divGraduacion);
            hideFields(divUnidadesExcedentes);
            fillProductos(productos);

            divAgregarBtn.classList.remove("d-none");
        }
    } else {
        hideFields(divProductos);
        hideFields(divPrecio);
        // hideFields(divCantidad);
        hideFields(divPais);
        hideFields(divGraduacion);
        hideFields(divSucategorias);
        hideFields(divUnidadesExcedentes);

        divAgregarBtn.classList.add("d-none");
    }
});

selectSubCategorias.addEventListener("change", async (event) => {
    hideFields(divPrecio);
    // hideFields(divCantidad);
    hideFields(divPais);
    hideFields(divGraduacion);
    hideFields(divProductos);
    hideFields(divUnidadesExcedentes);

    if (selectSubCategorias.value !== "") {
        let productos = await getProductosBySub(selectSubCategorias.value);
        productos.forEach((p) => console.log(p.valuable));
        if (productos.length != 0) {
            showFields(divProductos);
            hideFields(divPrecio);
            // hideFields(divCantidad);
            hideFields(divPais);
            hideFields(divUnidadesExcedentes);

            fillProductos(productos);
            divAgregarBtn.classList.remove("d-none");
        }
    } else {
        hideFields(divPrecio);
        // hideFields(divCantidad);
        hideFields(divPais);
        hideFields(divProductos);
        hideFields(divUnidadesExcedentes);

        divAgregarBtn.classList.add("d-none");
    }
});

selectProductos.addEventListener("change", async (event) => {
    hideFields(divPrecio);
    // hideFields(divCantidad);
    hideFields(divPais);
    hideFields(divGraduacion);
    hideFields(divUnidadesExcedentes);

    if (selectProductos.value != "") {
        producto = await getProducto(selectProductos.value);
        categoria = await getCategoria(producto.categoria);

        //si es alimentos
        if (
            producto.pais_tlc.length != 0 &&
            categoria.nombre_categoria != "Vino y bebidas alcohólicas" &&
            categoria.nombre_categoria !=
                "Cigarrillos y otros productos que contienen tabaco"
        ) {
            let paises = await getPaises(producto.id);
            fillPaisTlc(paises);
            showFields(divPais);
            showFields(divPrecio);
            // showFields(divCantidad);
        }
        //si es alcohol residente
        else if (
            categoria.nombre_categoria == "Vino y bebidas alcohólicas" &&
            producto.medio_transporte == 1
        ) {
            graduacionPais = await getGraduaciones();
            fillGraduacion(graduacionPais);
            showFields(divGraduacion);
            showFields(divUnidadesExcedentes);
            hideFields(divPais);
            // hideFields(divCantidad);
            hideFields(divPrecio);
        }
        //si es tabaco residente
        else if (
            selectCategorias.value == "10" &&
            producto.medio_transporte == 1
        ) {
            //cambia pais y tasa impuesto
            let totalPaisesTabaco = await getProductoPaisNotNulls();
            paisesTabaco = totalPaisesTabaco.filter(
                (e) => e.producto == selectProductos.value
            );
            fillPaisTlc(paisesTabaco);
            showFields(divPais);
            // showFields(divCantidad);
            showFields(divPrecio);
            showFields(divUnidadesExcedentes);
        }
        //si no tiene pais
        else {
            toggleFields(producto);
            hideFields(divPais);
            hideFields(divGraduacion);
        }
    }
    //si no tiene pais
    else {
        hideFields(divPrecio);
        // hideFields(divCantidad);
        hideFields(divPais);
    }
    showFields(divUnidadesExcedentes);
});

selectGraduacion.addEventListener("change", async (event) => {
    hideFields(divPais);
    hideFields(divPrecio);
    // hideFields(divCantidad);
    hideFields(divUnidadesExcedentes);

    if (selectGraduacion.value != "") {
        let graduacion = graduacionPais.find(
            (e) => e.id == selectGraduacion.value
        );
        paisesGraduacion = graduacion.pais;

        fillPaisTlc(paisesGraduacion);
        showFields(divPais);
        showFields(divPrecio);
        // showFields(divCantidad);
        showFields(divUnidadesExcedentes);
    } else {
        hideFields(divPais);
        hideFields(divPrecio);
        // hideFields(divCantidad);
        // hideFields(divUnidadesExcedentes);
        hideFields(divUnidadesExcedentes);
    }
});

selectMedioTransporte.addEventListener("change", (event) => {
    if (selectMedioTransporte.value != "") {
        switch (selectMedioTransporte.value) {
            case mediosTransporte["aereo"]:
                hideFields(divNombreEMbarcacion);
                hideFields(divNumeroTransporte);
                showFields(divNumVuelo);

                hideFields(divProcedencia)
                hideFields(divNacionalidad)
                hideFields(divResidente)
                divMercancia.classList.remove("d-none");
                break;
            case mediosTransporte["maritimo"]:
                showFields(divNombreEMbarcacion);
                hideFields(divNumeroTransporte);
                hideFields(divNumVuelo);

                hideFields(divProcedencia)
                hideFields(divNacionalidad)
                hideFields(divResidente)
                divMercancia.classList.remove("d-none");
                break;
            case mediosTransporte["terrestre"]:
                hideFields(divNombreEMbarcacion);
                hideFields(divNumVuelo);
                showFields(divNumeroTransporte)

                showFields(divProcedencia)
                // showFields(divNacionalidad)
                // showFields(divResidente)
                divMercancia.classList.remove("d-none");

                break;
        }
    } else {
        hideFields(divNombreEMbarcacion);
        hideFields(divNumVuelo);
        divMercancia.classList.add("d-none");
    }
});

selectProcedencia.addEventListener("change", (event) => {
    if (selectProcedencia.value != "") {
        if (selectProcedencia.options[selectProcedencia.selectedIndex].innerText == "Franja o región fronteriza") {
            hideFields(divNacionalidad);
            hideFields(divResidente);
        } else if (selectProcedencia.options[selectProcedencia.selectedIndex].innerText == "Extranjero") {
            showFields(divNacionalidad);
            hideFields(divResidente);
        }
    }
    else{
        hideFields(divNacionalidad);
        hideFields(divResidente);
        checkResidente.checked = false;
    }
});

selectNacionalidad.addEventListener("change", (event) => {
    if (selectNacionalidad.value != "") {
        if (selectNacionalidad.options[selectNacionalidad.selectedIndex].innerText == "Mexicana") {
            showFields(divResidente);
        } else if (selectNacionalidad.options[selectNacionalidad.selectedIndex].innerText == "Extranjera") {
            checkResidente.checked = false;
            hideFields(divResidente);
        }

    }
    else{
        hideFields(divResidente);
        
        checkResidente.checked = false;
    }
});

//llenado de campos mediante API
function fillCategorias(categorias) {
    let selectedOption = document.createElement("option");
    selectedOption.value = "";
    selectedOption.text = "---------";
    selectedOption.selected = true;
    selectCategorias.appendChild(selectedOption);

    categorias.forEach((cat) => {
        let option = document.createElement("option");
        option.value = cat.id;
        option.text = cat.nombre_categoria;
        selectCategorias.appendChild(option);
    });
    //cambia los registros duplicados
    // changeDuplicated()
}

function fillSubcategorias(subcategorias) {
    selectSubCategorias.innerHTML = "";
    let selectedOption = document.createElement("option");
    selectedOption.value = "";
    selectedOption.text = "---------";
    selectSubCategorias.selected = true;
    selectSubCategorias.appendChild(selectedOption);
    subcategorias.forEach((sub) => {
        let option = document.createElement("option");
        option.value = sub.id;
        option.text = sub.nombre_subcategoria;
        selectSubCategorias.appendChild(option);
    });
}

function fillProductos(productos) {
    selectProductos.innerHTML = "";
    let selectedOption = document.createElement("option");
    selectedOption.value = "";
    selectedOption.text = "---------";
    selectProductos.selected = true;
    selectProductos.appendChild(selectedOption);

    let terrestre = isTerrestreResidente(productos);
    let internacional = isOnlyInternacional(productos);

    //terrestre residente

    //si los productos son solo para residentes
    if (terrestre[2] && !residenteCheck.checked) {
        // alert(
        //     "Estos productos solo pueden ser portados por residentes de la frontera"
        // );
        hideFields(divProductos);
        showAlert(
            "Estos productos solo pueden ser portados por residentes de la frontera",
            "error",
            "Error",
            "warning", 
            true
        );
        return;
    } else if (terrestre[0] && residenteCheck.checked) {
        //se muestran solo los proudctos que tengan medio de transporte terrestre residente
        productos = terrestre[1];
    }
    //si los productos son solo para internacionales
    else if (internacional[0] && selectMedioTransporte.value == "1") {
        // alert(
        //     "Estos productos no pueden ser portados por residentes de la frontera"
        // );
        hideFields(divProductos);
        showAlert(
            "Estos productos no pueden ser portados por residentes de la frontera",
            "error",
            "Error",
            "warning",
            true
        );
        return;
    } else if (internacional[0]) {
        productos = internacional[1];
    } else if (productos[0].clave == "CT" || productos[0].clave == "VB" && !residenteCheck.checked) {
        //si es tabaco y no es residente muestra solo los poroductos que no apliquen para residentes
        productos = productos.filter((prod) => {
            return !prod.medio_transporte;
        });
    }
    
    

    productos = productos.filter((prod) => {

        return prod.cantidad_por_persona != null;
    });

    //si no hay productos es porque se pueden portar libremente esos productos
    if (productos.length == 0) {
        hideFields(divProductos);
        showAlert(
            "Estos productos entran dentro de tu equipaje",
            "info",
            "Estos productos entran dentro de tu equipaje",
            "warning",
            true
        );
        return;
    }    


    productos.forEach((prod) => {
        let option = document.createElement("option");
        option.value = prod.id;
        option.text = prod.nombre_producto;
        selectProductos.appendChild(option);
    });

    showFields(divProductos);
}

function fillPaisTlc(paises) {
    selectPais.innerHTML = "";
    let selectedOption = document.createElement("option");
    selectedOption.value = "";
    selectedOption.text = "---------";
    selectPais.appendChild(selectedOption);
    console.log("PAISES", paises)

    paises.forEach((pais) => {
        // console.log(pais.pais.id, pais.pais.pais_tlc, pais, pais.pais.id);
        let option = document.createElement("option");
        console.log(("PAIS PAIS_ID", pais.pais))
        //alimentos / alcohol /tabaco
        option.value =  pais.pais_id || pais.pais.id || pais.pais[0].id;
        option.text =
        pais.pais_tlc || pais.pais.pais_tlc || pais.pais[0].pais_tlc;
        selectPais.appendChild(option);
    });
}

function fillGraduacion(graduaciones) {
    selectGraduacion.innerHTML = "";
    let selectedOption = document.createElement("option");
    selectedOption.value = "";
    selectedOption.text = "---------";
    selectGraduacion.appendChild(selectedOption);

    graduaciones.forEach((graduacion) => {
        let option = document.createElement("option");
        option.value = graduacion.id;
        option.text = graduacion.graduacion;
        selectGraduacion.appendChild(option);
    });
}

/**
 *
 * @param {*} productos
 * @returns [0] true si los productos aplican para residentes
 * @returns [1] los productos que son para residentes
 * @returns [2] true si solo es para residentes
 *
 */
function isTerrestreResidente(productos) {
    let test = productos.filter((e) => e.medio_transporte == 1);
    return [test.length > 0, test, test.length == productos.length];
}
/**
 *
 * @param {*} productos
 * @returns [0] true si los productos aplican para pasajeros internacionales
 * @returns [1] los productos que son para pasajeros internacionales
 *
 */
function isOnlyInternacional(productos) {
    let test = productos.filter((e) => e.only_internacional);
    return [test.length > 0, test];
}

// //script por si una el nombre de una categoría se repite
// // ! por cuestiones de tiempo cambiará después
// function changeDuplicated(){
//     //options del select
//     let duplicados = []
//     //obtengo los duplicados
//     let optionsCategorias = selectCategorias.querySelectorAll("option")
//     optionsCategorias.forEach(async (option)=>{
//         if (option.text == "Ropa y calzado nuevo"){
//             let productos = []
//             duplicados.push(option)
//             //busco los productos de la categoria y los ahrego al array
//             productos = await getProductsByCat(option.value);
//             // obtengo los profuctos para saber para qué tipo de viaje aplican
//             productos.forEach((prod, index)=>{
//                 if(prod.medio_transporte == 1){
//                     option.text = "Ropa y calzado nuevo (residentes)"
//                 }
//             })
//         }
//     })
//     selectCategorias.innerHTML = optionsCategorias
// }

//limpia los inputs al cargar la página
function cleanInputs(excludeIds){
    document.querySelectorAll("input, select").forEach((input)=>{
        let clean = !excludeIds.includes(input.id)
        
        if(clean){
            input.value = ""
        }
    })
}
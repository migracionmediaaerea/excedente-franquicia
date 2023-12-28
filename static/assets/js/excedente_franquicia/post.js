let franquiciaDispoible = {
    residente: 150,
    internacional: 500,
};

let limiteDisponible = {
    residente: 3000,
    internacional: 3000,
    equipoComputo: 4000,
};

const form = document.getElementById("form_id");
const numAdultosInput = document.getElementById(
    "id_identificacion-numero_pasajeros_mayores"
);
const numMenoresInput = document.getElementById(
    "id_identificacion-numero_pasajeros_menores"
);
const equipoComputoInput = document.getElementById("id_equipo_computo");

const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

form.addEventListener("submit", (event) => {
    event.preventDefault();
    

    let formData = new FormData(form);
    formData.append("producto", JSON.stringify(arrProductos));
    console.log("formData", formData);

    showLoading()
    
    $.ajax({
        type: "POST",
        url: URL + "/excedente_franquicia/api/viaje",
        data: formData,
        processData: false, // tell jQuery not to process the data
        contentType: false, // tell jQuery not to set contentType
        success: function (data) {
            hideLoading();
            renderResponse(data);
            console.log("data", data);
            pk = data.pk;
        },
        error: function (err) {
            hideLoading();
            console.error(err);
        },
    });

    return false;
});




function renderResponse(res) {
    console.log("render response", res.mandar_agente);
    if (res.mandar_agente) {
        
        showAlert(
            "Es necesaria la intervención de un agente aduanal",
            "error",
            "Agente aduanal",
            "warning",
            false
        );
    } else if (res.cobro > 0) {
        showAlert(
            `Es necesaria un pago de impuestos con valor de $${res.cobro} dólares`,
            "warning",
            "Cobro de impuestos",
            "warning",
            false
        );
    } else if(res.error){
        let mesage = getInvalidFieldsResponse(res)
        showAlert(
            `${mesage}`,
            "error",
            "Error",
            "warning",
            true
        );
    }
}

function getInvalidFieldsResponse(error){
    //mapea los names de los campos que no son validos, estos vienen desde las respuesta del servidor
    const mapaNames = {
        "identificacion-nombre_jefe_familia": "Nombre(s)",
        "identificacion-apellido_jefe_familia": "Apellido",
        "identificacion-segundo_apellido_jefe_familia": "Segundo apellido",
        "identificacion-numero_pasajeros_mayores": "Cantidad de pasajeros que viajan juntos",
        "identificacion-numero_pasajeros_menores": "Cantidad de pasajeros menores de edad",
        "fecha_fin": "Fecha de arribo",
    }

    let str = "El/los campo(s) "
    for(key in error){
        if(key != 'error'){
            let value = mapaNames[key]
            str += `"${value}", `
        }
    }

    return str += " debe(n) contener caracteres y/o dígitos válidos."
}
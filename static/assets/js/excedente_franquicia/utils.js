
//eliminar valores de los campos
function clearFields(container) {
    // console.log('container', container)
    container.querySelectorAll("input, select").forEach((el) => {
        el.value = "";
        el.removeAttribute("required")
    });
}



function hideFields(div){
    clearFields(div)
    div.classList.add('d-none')
}

function showFields(div){
    div.classList.remove('d-none')
}

function makeFieldsUndisabled(div){
    div.querySelectorAll("input, select").forEach((el) => {
        el.removeAttribute("disabled")
    });
}
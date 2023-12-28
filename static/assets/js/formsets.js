import { separateIdStringFromFinalIndex, initialConfig } from './formsetFunctions.js'


// Your form must have "form_id" as id
let formulario = document.getElementById("form_id");





// START: CUSTOM LOGIC
// Array with the ids of the main containers that contain our formsets. These will always have at least one formset.
const oneToNFormsets = [];

formulario.addEventListener("input", (e) => {
    
    // e.target will return the HTML element of the input that was changed. Use your logic accordingly
    let [initialString, selectIndex] = separateIdStringFromFinalIndex(e.target.id);

    // If the input that was changed is one of our selects, then unhide out hidden text input
    if (initialString == 'id_select') {
        let hiddenInput = document.getElementById(`id_hidden-${selectIndex}`);
        hiddenInput.hidden = (e.target.value !== '3');
    }
})
// END: CUSTOM LOGIC





// Do not modify this for god's sake
initialConfig(formulario, oneToNFormsets);
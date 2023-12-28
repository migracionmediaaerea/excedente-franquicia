const URL = window.location.origin;

async function getSubcategorias(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/subcategorias/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getProductosBySub(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/productos/subcategoria/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getProductsByCat(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/productos/categoria/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getProducto(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/productos/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getPaises(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/producto_pais/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getCategorias() {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/categorias`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getCategoria(id) {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/categoria/${id}`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getGraduaciones() {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/graduaciones`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}

async function getProductoPaisNotNulls() {
    try {
        const res = await fetch(
            `${URL}/excedente_franquicia/api/productos/producto_pais`
        );
        const resJson = await res.json();
        return resJson;
    } catch (err) {
        return console.log(err);
    }
}







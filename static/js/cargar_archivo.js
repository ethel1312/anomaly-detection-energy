const archivoInput =
    document.getElementById("archivo");

const archivoSeleccionado =
    document.getElementById("selected-file");

function mostrarError(mensaje){

    archivoSeleccionado.style.display = "block";

    archivoSeleccionado.innerHTML = `
        <div class="file-error">
            <i class="fa-solid fa-circle-xmark"></i>
            ${mensaje}
        </div>
    `;
}

archivoInput.addEventListener("change", function(){

    const errorServidor =
        document.getElementById("server-error");

    if(errorServidor){
        errorServidor.style.display = "none";
    }

    if(this.files.length === 0){
        return;
    }

    const archivo = this.files[0];

    // Archivo vacío
    if(archivo.size === 0){

        mostrarError(
            "Archivo vacío"
        );

        return;
    }

    // Validar extensión
    if(
        !archivo.name
            .toLowerCase()
            .endsWith(".csv")
    ){

        mostrarError(
            "Formato incorrecto. Solo se permiten archivos CSV"
        );

        return;
    }

    const tamañoMB =
        (archivo.size / 1024 / 1024)
        .toFixed(2);

    const reader = new FileReader();

    reader.onload = function(e){

        const contenido =
            e.target.result;

        const lineas =
            contenido
            .split(/\r\n|\n/)
            .filter(l => l.trim() !== "");

        if(lineas.length === 0){

            mostrarError(
                "Archivo vacío"
            );

            return;
        }

        const encabezados =
            lineas[0]
            .split(",")
            .map(c => c.trim());

        if(
            !encabezados.includes("CONS_NO")
        ){

            mostrarError(
                "Falta la columna CONS_NO"
            );

            return;
        }

        const registros =
            Math.max(
                lineas.length - 1,
                0
            );

        archivoSeleccionado.style.display =
            "block";

        archivoSeleccionado.innerHTML = `
            <div class="file-valid">
                <i class="fa-solid fa-circle-check"></i>
                Archivo seleccionado correctamente
            </div>

            <div>
                <strong>Nombre:</strong>
                ${archivo.name}
            </div>

            <div>
                <strong>Tamaño:</strong>
                ${tamañoMB} MB
            </div>

            <div>
                <strong>Registros estimados:</strong>
                ${registros}
            </div>
        `;
    };

    reader.readAsText(archivo);

});
function removeCard(idCarta){
    const carta = document.getElementById(idCarta)
    carta.remove()
}


function respuestaDocente(dibujo,aprueba, justificacion=''){
    const alumno = document.getElementById("buscarAlumno");
    const id_alumno = alumno.value;
    console.log(justificacion)
    $.ajax({
        type: 'GET',
        url: '/respuesta_docente/',
        data: {
            'idUsuario' : id_alumno,
            'idDibujo' : dibujo,
            'aprueba' : aprueba,
            'justificacion' : justificacion
        },
        success: function(data){
            console.log(data)
            removeCard(data.data.idDibujo)
        },error: function(error){
            console.log(error)
        }

    })
}

function prueba(dibujo){
    imagenModal = document.getElementById("modal-body");
    imagenModal.innerHTML='<img id="dibujo-modal" style="height:auto; width:110vh;" src="data:image/jpeg;base64, ' + dibujo + '" alt="dibujo">'
    $("#exampleModal").modal("show")
}

function justificar(dibujo_id){
    imagenModal = document.getElementById("modal-body");
    imagenModal.innerHTML = `
    <h3>¿Por que no aprueba este dibujo?</h3>
    <label for="justificacion">Justificación:  </label>
    <input id="justificacion" type="text" name="name_field">
    <button class='btn btn-short btn-primary' onclick='guardar_justificacion(`+dibujo_id+`)'>Guardar Justificacion</button>`
    $("#exampleModal").modal("show")
}

function guardar_justificacion(dibujo_id){
    respuesta = document.getElementById('justificacion').value;
    respuestaDocente(dibujo_id,0,respuesta);
    $("#exampleModal").modal("hide");
    alert("Justificación guardada!");
}

//data-toggle="modal" data-target="#exampleModal"
$(function () {
    $('#buscar').on('click', function () {
        const loader = document.getElementById("loader")
        loader.style.visibility = 'visible'
        const alumno = document.getElementById("buscarAlumno");
        const id_alumno = alumno.value;
        document.getElementById("nombreAlumno").innerHTML = alumno.options[alumno.selectedIndex].text
        const id_actividad = document.getElementById("actividad_id").innerHTML;
        $.ajax({
            type: 'GET',
            url: '/traer_dibujos/',
            data: {
                'id_alumno': id_alumno,
                'id_actividad': id_actividad
            },
            success: function (data) {
                loader.style.visibility = 'hidden'
                const contenido = document.getElementById("Dibujos_alumno");
                contenido.innerHTML = "";
                let container = document.querySelector('.dibujos_de_alumno');
                for (const [id, dibujo] of Object.entries(data.dibujos)) {
                    let myDiv = document.createElement("div");
                    myDiv.className = "card-container"
                    myDiv.setAttribute('id',id)
                    myDiv.innerHTML = `
                    <div class="card">
                        <div id ="card-image" class="card-image">
                        <a onclick="prueba('`+dibujo+`')"><img id="dibujo-modal" style="height:auto; width:100%;" src="data:image/jpeg;base64, ` + dibujo + `" alt="dibujo"></a>       
                        </div>
                        <div class="card-body">
                        <button class= "btn btn-success btn-large" onclick="respuestaDocente(`+id+`,1)" data-tootip="tooltip" title="Aprobar" ><i class="fas fa-check"></i></button>
                        <button class= "btn btn-danger btn-large" onclick="justificar(`+id+`)" data-tootip="tooltip" title="No Aprobar"><i class="fas fa-ban"></i></button>
                        </div>
                    </div>
                    ` 
                    container.appendChild(myDiv);
                  }
                  
            },error: function(error){
                console.log(error)
            }
        });
    });
});
function guardar(id){
    tabla = document.getElementById("table");

    idAlumno = tabla.rows[id].cells[1].getAttribute("data-id");
    fecha_creacion = tabla.rows[id].cells[2].innerHTML;
    propuesta = tabla.rows[id].cells[3].innerHTML;
    evaluacion = document.getElementById("calificacion"+id).value;


    $.ajax({
        type:'GET',
        url: '/guardarCalificacion/',
        data:{
            'idAlumno' :idAlumno,
            'fechaCreacion': fecha_creacion,
            'evaluacion': evaluacion,
            'propuesta': propuesta
        },
        success:function(respuesta){
            if(respuesta == "Si"){
                console.log("Se ha agregado con exito")
                document.getElementById("guardado"+id).disabled = true;
                document.getElementById("calificacion"+id).disabled = true;

            }else{
                console.log("Hubo un problema con agregar la evaluacion")
            }
        }
    })
}

function prueba(){

        alumno_a_buscar = document.getElementById("alumno_a_buscar");
        id_alumno = alumno_a_buscar.value;
        
        $.ajax({
            type: 'GET',
            url: '/traer_datos/',
            data:{
                'id_alumno': id_alumno
            },
            success:function(datos){
                console.log("Filtrando...")
                document.getElementById("table").remove()
                contenido_tabla = document.getElementById("tabla")

                rows = ``
                for(const [id, alumno] of Object.entries(datos)){
                    console.log(alumno[2])
                    rows +=  `
                    <tr>
                        <td>`+id+`</td>
                        <td data-id = `+alumno[1]+`>`+alumno[0]+`</td>
                            <td>`+alumno[2][0]+`</td>
                            <td>`+alumno[2][1]+`</td>
                            <td><select name="calificacion" id="calificacion`+id+`">
                                <option value="">Calificar</option>
                                <option value="1">No Logrado</option>
                                <option value="2">Casi Logrado</option>
                                <option value="3">Logrado</option>
                            </select></td>
                            <td id="boton"><button onclick="guardar(`+id+`)" data-id=`+id+` id="guardado`+id+`">Guardar</button></td>    
                        </tr>
                        `
                }


                contenido_tabla.innerHTML = `
                <table style="width:100%" id="table">
                <tr>
                    <th>#</th>  
                    <th>Alumno</th>
                    <th>Fecha Respuesta</th>
                    <th>Respuesta</th>
                    <th>Calificacion</th>
                    <th>Guardar</th>
                </tr>
                `+rows+`</table>
                <button onclick="window.location.reload();">Ver todos</button>
                `
                
                
                  
                
            }

        })
}

    


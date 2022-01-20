
function crearCarta(actividades,curso,reimId,reimnombre){
    actividades_con_dibujos = [10005,20014]
    actividades_con_propuestas = [9050]
    let container = document.querySelector('.actividades');
    for (const [nombre, id] of Object.entries(actividades)) {
        let myDiv = document.createElement("div");
        myDiv.className = "card-container"
        myDiv.innerHTML = `
        <div class="card">
            <div class="card-image">
             <img class= "imagen-carta" src="/static/iconos/`+reimnombre+`/`+id+`.png">
            </div>
            <div class="card-body">
                <div class="card-title">
                    <h5 class="card-title">`+nombre+`</h5>
                </div>
                <div class="card-functions">
                    <a id="curso" data-id ="`+id+`" onclick = 'guardarId("`+nombre+`",`+ id +`,`+ reimId+`)' href="../../../../../resultados/`+reimId+`">Ver Resultados</a>
                    <div class="dropdown" id="`+id+`dropdown"></div>
                    `
                    if(actividades_con_dibujos.includes(id)){
                       
                    };
                    `                    
                </div>
            </div>
        </div>
        ` 
        container.appendChild(myDiv);

        if(actividades_con_dibujos.includes(id)||actividades_con_propuestas.includes(id)){
            funciones = document.getElementById(id+"dropdown");
            funciones.innerHTML =`
            <button class="masFunciones"><i class="fa fa-caret-down"></i></button>
            <div class="dropdown-content" id="`+id+`dropdown-content"></div>
                `
        }
        
        insertarfunciones = document.getElementById(id+"dropdown-content")
        if(actividades_con_dibujos.includes(id)){
            insertarfunciones.innerHTML +=`<a  id= "revisionDibujo`+id+`" href="../../../../../revisionDibujo/`+id+`">Revisar Dibujos</a>`
        }
        if(actividades_con_propuestas.includes(id)){
            insertarfunciones.innerHTML +=`<a  id= "evaluacionPropuesta`+id+`" href="../../../../../evaluacionPropuesta">Evaluacion Propuesta</a>`
        }
    }
}

function removerCartas(){
    const cartas = document.querySelectorAll(".card")
    cartas.forEach(function(carta){
        carta.remove()
    })
};


function guardarId(nombre,id, reimId){
    localStorage.setItem("actividadElegida",nombre)
    localStorage.setItem("idActividad",id)
    localStorage.setItem("idReim",reimId)
}




$(function(){
    $('#sidebar a').on('click',function(){
        const nombre_reim = $(this).attr("title");
        const curso = document.getElementById("curso").getAttribute("data-curso");

        $.ajax({
            type: 'GET',
            url: '/home_reim_ajax/',
            data: {
                'reim': nombre_reim,
                'curso': curso
            },
            success: function(response){
                const datos = response.data
                const actividades = Object.values(datos)[0]
                const jsoncurso = JSON.parse(Object.values(datos)[1])
                const reimId = Object.values(datos)[2]
                const reimnombre = Object.keys(datos)[0]
                document.getElementById('nombre_reim').innerHTML =reimnombre
                document.getElementById('iconoREIM').src= "/static/iconos/"+reimnombre+"/"+reimId+".png"
                document.getElementById('iconoREIM').style.visibility = 'visible';
                
                removerCartas()
                crearCarta(actividades,jsoncurso,reimId,reimnombre)

            },
            
        })
    })
})

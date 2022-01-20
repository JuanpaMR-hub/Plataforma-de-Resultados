
//-----------------FUNCIONES------------------
function create_chart(tipo,datos,opciones = undefined){
    if(myChart != undefined){
        myChart.destroy()
    }
    if(datos.backgroundColor == undefined){
        datos.backgroundColor = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)'
        ]
        datos.borderColor = [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)'
        ]
    }
    var ctx = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(ctx, {
        type : tipo,
        data : {
            labels : datos.labels,
            datasets: [{
                label : datos.label,
                data : datos.datos,
                backgroundColor : datos.backgroundColor,
                borderColor : datos.borderColor,
                borderWidth : 1
            }]
        },
        options : opciones
    })
}



function rellenar_actividades(actividades) {
    var select = document.getElementById("Actividad");
    select.options.length = 0;
    for (var i = 0; i < actividades.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = actividades[i];
        opt.value = actividades[i];
        select.appendChild(opt);
    }
}

function cambiar_titulo(nuevo_titulo){
    myChart.options.plugins.title.text = nuevo_titulo;
    myChart.update();
}

function borrarData() {
    return new Promise((resolve, reject) => {
        myChart.data.labels = []    
        myChart.data.datasets.forEach((dataset) => {
        dataset.data = []
        });
        myChart.update();
        resolve(true)
    })    
}

async function actualizardatos(configuracion) {
    await borrarData();
    console.log("Estoy en actualizar datos")
    for (i in configuracion.labels) {
        myChart.data.labels.push(configuracion.labels[i]);
        myChart.data.datasets.forEach((dataset) => {
            dataset.data.push(configuracion.datos[i]);
        });
        myChart.update();
    }

    //Cambiar el tipo de grafico
    // myChart.configuracion.type = configuracion['tipoGrafico']
}



async function creaciondeGrafico(){
    var tabla = document.getElementById('tabla_datos');
    var operacion = document.getElementById('operacion').value;
    var valores = document.getElementById('valores').value;
    var orden = document.getElementById('orden').value;
    var tipoGrafico = document.getElementById('tipoGrafico').value;

    console.log(valores)

    datos = {
        'target' : tabla.name,
        'target_value' : tabla.value,
        'operacion': operacion,
        'valores' : valores,
        'orden' : orden
    }
    datos_grafico = await traer_datos(datos);
    create_chart(tipoGrafico,datos_grafico)
}
//-------------------- FIN FUNCIONES------------

//-------------------FUNCIONES AJAX-------------
function traer_datos(datos) {
    return new Promise((resolve,reject) => {
        $.ajax({
            type: 'GET',
            url: '/ajax_handler/',
            data: datos,
            success: function (response) {
                console.log(response.data)
                console.log("Estos son los datos" + datos.target)
                if (datos.target == 'Reim') {
                    rellenar_actividades(response.data);
                }else if (datos.target == 'datos') {
                    resolve (response.data)
    
                }
            },
            error: function (error) {
                console.log(error)
            }
        })
    })
   
};
//------------------FIN FUNCIONES AJAX----------


//----------------------FUNCIONES EN LLAMADAS-------------

$('#creargrafico').on('click',function(){
    creaciondeGrafico()
})
// $('#reims').on('change', function () {
//     var datos = {
//         target: $(this).context.name,
//         value: $(this).context.value
//     }
//     traer_datos(datos);
// })

// $('#Actividad').on('change', function () {
//     value = $(this).context.value
//     cambiar_titulo(value)
// })


// $('#tabla_datos').on('change', function () {
//     var eleccion = document.getElementById('tabla_datos')
//     var texto = eleccion.options[eleccion.selectedIndex].text;
//     var ordenarpor = document.getElementById('por');
//     var datos = {
//         target: 'datos',
//         value: 'AlumnoRespuestaActividad',
//         orden: 'Alumno'
//     }
//     traer_datos(datos)
// })

// $('#Operation').on('change',function(){

// })

//------------------FIN FUNCIONES EN LLAMADA---------------


//------------------CREACIÓN DE GRAFICO DE PRUEBA----------
/*
Estructura de un grafico en chartjs
datos = {
    labels= []  una lista de los datos que van en el eje (ejemplo : el nombre de los alumnos)
    datasets : [{    Es una lista que contiene un diccionario, dicho diccionario contiene los datos del grafico
        label : string que representa la leyenda
        data : los datos que se visualizarán
        //colores
        backgroundcolor : color de cada uno de los datos
        borderColor : color del borde
        borderWidth : 1 
    }]
}
*/
var myChart;
var datos= {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
        ],
        borderWidth: 1
    }]
}
var opciones ={
    plugins: {
        title: {
            display: true,
            text: 'Grafico de prueba',
            font: {
                size: 20
            }
        }
    }
}

create_chart('bar',datos,opciones)
//-----------------------FIN CREACION GRAFICO DE PRUEBA----------
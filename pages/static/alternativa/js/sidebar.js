function abrir_modal(url){
    $('#info').load(url,function(){
        $(this).modal('show');
    })
}




function getFilters () {
    console.log("Estamos en getfilters")
    var datosCurso = document.getElementById("jsonData").getAttribute('data-json')
    var curso = JSON.parse(datosCurso)
    var fecha = curso.fecha
    var colegio = parseInt(curso.colegio)
    var nivel = parseInt(curso.nivel)
    var letra = parseInt(curso.letra)
    const filter1 = {$schema: "http://powerbi.com/product/schema#advanced",target: {table: "ulearnet_reim_pilotaje pertenece",column: "fecha"},logicalOperator: "Or",conditions: [{operator: "GreaterThan",value: fecha},{operator: "Is",value:fecha}]};
    const filter2 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "colegio_id"},operator: "In",values: [colegio]};
    const filter3 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "nivel_id"},operator: "In",values: [nivel]};
    const filter4 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "letra_id"},operator: "In",values: [letra]};
    var allFilters = [filter1,filter2,filter3,filter4];

    console.log(allFilters);
    return allFilters;
    }

function embed(nombre_actividad,idActividad) {   
    var reportContainer = $("#report-container").get(0);
    var models = window["powerbi-client"].models;
    var filtros = getFilters()
    var reportLoadConfig = {
        type: "report",
        tokenType: models.TokenType.Embed,
        filters : filtros,
        // Enable this setting to remove gray shoulders from embedded report
        settings: {
            background: models.BackgroundType.Transparent,
            filterPaneEnabled : false,
            navContentPaneEnabled: true
        }

    };

    $.ajax({
        type: "GET",
        url: "/getembedinfo",
        dataType: "json",
        data:{
            'nombre_actividad':nombre_actividad,
            'id_actividad':idActividad
        },
        success: function (datos) {
            embedData = $.parseJSON(JSON.stringify(datos));
            console.log("EmbedData: "+embedData)
            reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            // Embed Power BI report when Access token and Embed URL are available
            var report = powerbi.embed(reportContainer, reportLoadConfig);
            
            document.getElementById('report-container').style.opacity = '1';
            document.getElementById('loader').style.visibility='hidden';
            

            // Triggers when a report is successfully embedded in UI
            report.on("rendered", function () {
                console.log("Report render successful")
            });

            // Clear any other error handler event
            report.off("error");

            // Below patch of code is for handling errors that occur during embedding
            report.on("error", function (event) {
                var errorMsg = event.detail;

                // Use errorMsg variable to log error in any destination of choice
                console.error(errorMsg);
                return;
            });
        },
        error: function (err) {
            console.log("Hola");
            // Show error container
            var errorContainer = $(".error-container");
            // $(".embed-container").hide();
            errorContainer.show();

            // Format error message
            var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
            errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html(errMessageHtml);
        }
    });
};







window.onload=function(){

    const nombre_actividad = localStorage.getItem("actividadElegida")
    const id_actividad = localStorage.getItem("idActividad")
    if(nombre_actividad != ""){
        console.log(nombre_actividad)
        $.ajax({
            type: 'GET',
            url: '/contenido/',
            data: {
                'actividad': nombre_actividad,
                'id_actividad':id_actividad
            },
            success: function(datos){
                console.log(datos)
                document.getElementById('nombre_actividad').innerHTML = nombre_actividad;
                document.getElementById('loader').style.visibility = 'visible';
                document.getElementById('report-container').style.opacity = '0.2';

                embed(nombre_actividad,id_actividad);
            },
            error: function(error){
                console.log(error)
            }
        })
        localStorage.setItem("actividadElegida","")
    }
     
}

function informacion_modal(){
    console.log("Hola")
    imagenModal = document.getElementById("modal-body");
    nombre_actividad = document.getElementById("nombre_reim").innerHTML
    $("#exampleModal").modal("show")   
}

$(function(){
    $('#actividades a').on('click',function(){
        const nombre_actividad = $(this).attr("alt")
        const id_actividad = $(this).attr("data-idActividad")
        console.log(id_actividad)
        console.log(nombre_actividad)
        $.ajax({
            type: 'GET',
            url: '/contenido/',
            data: {
                'actividad': nombre_actividad,
                'id_actividad':id_actividad
            },
            success: function(datos){
                document.getElementById('nombre_actividad').innerHTML =nombre_actividad
                document.getElementById('loader').style.visibility = 'visible';
                document.getElementById('report-container').style.opacity = '0.2';
                document.getElementById("modal-body").innerHTML = Object.keys(datos)[1] + ": " + Object.values(datos)[1]


                embed(nombre_actividad,id_actividad);
            },
            error: function(error){
                console.log(error)
            }
        })
    })
})


// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
// function filtrar(){
//     alumno = document.querySelector("#alumnos_list")
//     alumno_elegido = alumno.options[alumno.selectedIndex].value;
//     return alumno_elegido;
// }



function loadJson(selector) {
    return JSON.parse(document.querySelector(selector).getAttribute('data-json'));
  }


function getFilters () {
    var curso = loadJson('#jsonData')
    var fecha = curso.map((item) => item.fecha);
    var colegio = curso.map((item) => item.colegio);
    var nivel = curso.map((item) => item.nivel);
    var letra = curso.map((item) => item.letra);


    const filter1 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "fecha"},operator: "In",values: [fecha]};
    const filter2 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "colegio_id"},operator: "In",values: [colegio]};
    const filter3 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "nivel_id"},operator: "In",values: [nivel]};
    const filter4 = {$schema: "http://powerbi.com/product/schema#basic",target: {table: "ulearnet_reim_pilotaje pertenece",column: "letra_id"},operator: "In",values: [letra]};
    var allFilters = [filter1,filter2,filter3,filter4];

    console.log(allFilters);
    return allFilters;
    }

$(function () {
    var reportContainer = $("#report-container").get(0);
    var models = window["powerbi-client"].models;
    var reportLoadConfig = {
        type: "report",
        tokenType: models.TokenType.Embed,

        // Enable this setting to remove gray shoulders from embedded report
        settings: {
            background: models.BackgroundType.Transparent,
            filterPaneEnabled : false,
            navContentPaneEnabled: false
        }

    };

    $.ajax({
        type: "GET",
        url: "/getembedinfo",
        dataType: "json",
        success: function (data) {
            embedData = $.parseJSON(JSON.stringify(data));
            reportLoadConfig.accessToken = embedData.accessToken;

            // You can embed different reports as per your need
            reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

            // Use the token expiry to regenerate Embed token for seamless end user experience
            // Refer https://aka.ms/RefreshEmbedToken
            tokenExpiry = embedData.tokenExpiry;

            // Embed Power BI report when Access token and Embed URL are available
            var report = powerbi.embed(reportContainer, reportLoadConfig);

            // Triggers when a report schema is successfully loaded
            report.on("loaded", function () {
                
                report.getFilters()
                .then(function(filters) {
                    
                    var allFilters = getFilters();

                    filters.push(allFilters);
                    
                    if (allFilters != null) return report.setFilters(allFilters);
                }).catch (function (error) {
                    console.log(error.message);
                });
                console.log("Report load successful")
            });

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
            $(".embed-container").hide();
            errorContainer.show();

            // Format error message
            var errMessageHtml = "<strong> Error Details: </strong> <br/>" + $.parseJSON(err.responseText)["errorMsg"];
            errMessageHtml = errMessageHtml.split("\n").join("<br/>")

            // Show error message on UI
            errorContainer.html(errMessageHtml);
        }
    });
});
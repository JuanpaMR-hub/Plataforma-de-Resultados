$(function(){
    $("#actividades a").on('click',function(){
        console.log("Se ha clickeado una actividad")
        $("#loader").style.visibility = visible;
    })
})
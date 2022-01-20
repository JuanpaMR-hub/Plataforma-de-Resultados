function curso_elegido(id_colegio,id_nivel,id_letra,str_fecha){
    console.log("Se ha presionado el boton")
    const colegio = id_colegio;
    const nivel = id_nivel;
    const letra = id_letra;
    const fecha = str_fecha;
    $.ajax({
        type:'GET',
        url: '/home_ajax/',
        data:{
            'colegio':colegio,
            'nivel':nivel,
            'letra':letra,
            'fecha':fecha,
        },
        success:function(curso){
            console.log(curso);
            window.location.href = window.location.href + "reims/";
            console.log(window.location.href);
        }
    })
}
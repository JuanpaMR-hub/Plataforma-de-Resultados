var curso = document.getElementById("curso").getAttribute("data")
  console.log(curso)
  console.log(typeof(curso))


  $.ajax({
            type: 'GET',
            url: '/resultados/',
            data: {
                'curso': datos
            },
            success: function(response){
                console.log(response.data)
            },
            error: function(error){
                console.log(error)
            }
        })
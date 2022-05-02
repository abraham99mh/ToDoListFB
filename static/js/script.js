
var clicked = 0;
var id = 0;

$('#buttonAdd').click(function newTask(){
    console.log($('#newTask').val())
    $.ajax({
        type: "POST",
        url: '/',
        data: {
            Task: $('#newTask').val()
        },
        async: false, 
        success:
            window.location.href = '/'
      });
})

$('#tablaAdd').toggle();

$("#agregar").click(function(){
    $('#tablaAdd').toggle();
})

$("tbody tr").click(function () {
    $('.table-active').removeClass('table-active')
    $(this).addClass("table-active")
    console.log($(this).attr('id'))
    id = $(this).attr('id')

    if(id == "tablaAdd"){
        console.log("id es tablaAdd")
        $('#modificar').prop( "disabled", true );
        $('#eliminar').prop( "disabled", true );
    }
    else{
        $('#modificar').prop( "disabled", false );
        $('#eliminar').prop( "disabled", false );
    }
    if(clicked == 0){
        $('#modificar').prop( "disabled", false );
        $('#eliminar').prop( "disabled", false );
        clicked = 1
    }
});


$("#modificar").click(function(){
    text = $("#name" + id).text()
    console.log(text)
    $("#inputEdit").val(text)
})

$("#modificarConfirmar").click(function(){
    $.ajax({
        type: "POST",
        url: '/update-task-name',
        data: {
            id: id,
            nameText: $("#inputEdit").val()
        }
    });
    $("#name" + id).text($("#inputEdit").val())
    $("#closeModal").click()
    console.log("clicked")
})

$("#eliminar").click(function(){
    $.ajax({
        type: "POST",
        url: '/delete',
        data: {
            id: id
        },
        async: false, 
        success:
            window.location.href = '/'
    });
})

function checkbox(cb){
    console.log(cb.checked)
    $.ajax({
        type: "POST",
        url: '/update-check',
        data: {
            id: $(cb).parent().parent().attr('id'),
            cb: cb.checked
        }
    });
}

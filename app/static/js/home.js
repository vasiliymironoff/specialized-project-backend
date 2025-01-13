$(document).ready(function(){
    // make prediction and save data in database
    $('#myForm').on('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение формы
        console.log($('#news'))
        var text = $('#news').val()

        $.ajax({
            url: '/',  
            type: 'POST',
            data: JSON.stringify({
                'text': text,
                'csrfmiddlewaretoken': '{{csrf_token}}' 
            }),
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(123)
                console.log(response)
                document.getElementById('category').innerText = response['category']
                document.getElementById('description').innerText = response['description']
            },
            error: function(xhr, status, error) {
                console.error('Error uploading image:', error);                
            }
        });
    });
});

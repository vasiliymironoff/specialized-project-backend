$(document).ready(function(){

    // Include the CSRF token in the AJAX requests
    function getCookie(name) {
        var cookieValue = null;

        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    // view image and description of specific row
    $('.btn.btn-primary.btn-sm').on('click', function(){
        // collect the id
        console.log('button clicked');
        var row = $(this).closest('tr');
        var id_image = row.find('td:eq(0)').text();
        console.log(id_image);

        // send to backend to process the id and take answer
        $.ajax({
            url: '/report/', 
            type: 'POST', 
            data: {
                'id_filtered': id_image,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(res){
                console.log("success to send data");                
                console.log('file_path: ' + res.file_path);
                console.log('description: ' + res.description);

                if(res.file_path){
                    $('#storedImage').attr('src', '/' + res.file_path);
                    $('#txtDescription').text(res.description);
                }else{
                    console.error('File path not found');
                }
            },
            error: function(xhr, status, err){
                console.error('Error: ', err);
            }
        });
    });

    // refresh web page
    $('.btn.btn-danger.btn-sm').click(function(){
        $('#storedImage').attr('src', '');
        $('#storedImage').attr('src', '/static/images/default.jpg');
        $('#txtDescription').text('the text predicted...');
    });
});

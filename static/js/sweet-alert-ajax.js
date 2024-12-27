function call_sw_alert_func(job_id, message, action='delete') {
    swal({
        title: "Are you sure?",
        text: message,
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
    .then((willProceed) => {
        if (willProceed) {
            if (action === 'delete') {
                // Handle delete
                $.ajax({
                    url: `/dashboard/employer/delete/${job_id}/`,
                    type: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    success: function(response) {
                        if(response.status) {
                            $(`#row_${job_id}`).remove();
                            swal("Success!", "Job has been deleted.", "success");
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        swal("Error", "Could not delete the job.", "error");
                    }
                });
            } else if (action === 'close') {
                // Handle close
                $.ajax({
                    url: `/dashboard/employer/close/${job_id}/`,
                    type: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    success: function(response) {
                        if(response.status) {
                            $(`#change_job_status_${job_id}`).html('<a class="text-white btn btn-success btn-sm">Closed</a>');
                            swal("Success!", "Job has been marked as closed.", "success");
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        swal("Error", "Could not close the job.", "error");
                    }
                });
            }
        }
    });
}

// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set up CSRF token for all AJAX requests
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});
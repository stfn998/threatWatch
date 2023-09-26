$(document).ready(function() {
  var footer = $('.dark-bg');
  var main = $('main');

  var footerHeight = footer.outerHeight();
  main.css('margin-bottom', footerHeight);

  $(window).on('resize', function() {
    var footerHeight = footer.outerHeight();
    main.css('margin-bottom', footerHeight);
  });
});


$(document).ready(function() {
    $('#myTable').DataTable({
        "lengthChange": false,
        "pageLength": 10,
        "responsive": true
    });
});

$(document).ready(function() {
    $('#confirmForm').on('submit', function(e) {
        e.preventDefault();
        const formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/incident/new',
            data: formData,
            success: function(response) {
                if (response.status == 'similar') {
                    // Show modal if a similar incident is detected
                    $('#similarIncidentModal').modal('show');
                } else if (response.status == 'added') {
                    window.location.href = '/';  // Redirect to homepage
                }
            }
        });
    });

    $('#confirmAddIncident').on('click', function() {
        $.ajax({
            type: 'POST',
            url: '/incident/new',
            data: $('#confirmForm').serialize() + '&force_add=true',  // adding a force parameter
            success: function(response) {
                if (response.status == 'added') {
                    window.location.href = '/';  // Redirect to homepage
                }
            }
        });
    });

    $('#cancelAddIncident').on('click', function() {
        $('#similarIncidentModal').modal('hide');
        $('#confirmForm')[0].reset();  // reset the form content
    });
});

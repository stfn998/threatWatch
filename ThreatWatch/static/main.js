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



jQuery(function($) {
  // Show/hide profile info on click of profile button
  $('#show-profile').click(function() {
    $('#profile-col').show();
    $('#update-col').hide();
  });
});

jQuery(function($) {
  // Show/hide update form info on click of profile button
  $('#show-update').click(() => {
    $('#profile-col').hide();
    $('#update-col').show();
  });
});

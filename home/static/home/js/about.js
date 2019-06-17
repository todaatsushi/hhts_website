// Show/Hide sections based on button selection

// Show/Hide Guide & Volunteer modals
jQuery(function() {
  $(document).ready(function() {
    // Show default
    // Guide
    $('#guide-section').css('display', 'block');
    // Volunteer
    $('#adult-section').css('display', 'block');
  });

  // Each button click shows relevant section
  // Guide
  $('#guide-btn').click( function() {
    // Show/Hide sections
    $('#guide-section').css('display', 'block');
    $('#fes-section, #uni-section, #exp-section').css('display', 'none');
  });

  $('#fes-btn').click( function() {
    $('#fes-section').css('display', 'block');
    $('#guide-section, #uni-section, #exp-section').css('display', 'none');
  });

  $('#uni-btn').click( function() {
    $('#uni-section').css('display', 'block');
    $('#guide-section, #fes-section, #exp-section').css('display', 'none');
  });

  $('#exp-btn').click( function() {
    $('#exp-section').css('display', 'block');
    $('#guide-section, #uni-section, #fes-section').css('display', 'none');
  });

  // Volunteer
  $('#adult-btn').click( function() {
    $('#adult-section').css('display', 'block');
    $('#kid-section').css('display', 'none');
  });

  $('#kid-btn').click( function() {
    $('#adult-section').css('display', 'none');
    $('#kid-section').css('display', 'block');
  });
});

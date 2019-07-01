// Toggle visible information by button choice
window.addEventListener('load', (e) => {
    // Show only the picture and basic info at first
    const content_divs = document.getElementsByClassName('profile-content');

    for (let i = 0; i < content_divs.length; i++){
        content_divs[i].style.display = 'none';
    }

    // Show first div
    const basic_info = document.getElementById('profile');
    basic_info.style.display = 'flex';
})

// Listen for clicks on toggle buttons, hide the others bar the one that was clicked
// Gather elements
const buttons = document.getElementsByClassName('profile-toggle');
const content_divs = document.getElementsByClassName('profile-content');
const button_reference = {
    'show-profile': 'profile',
    'show-info': 'profile-about',
    'show-update': 'profile-update',
};

// Add show/hide function to every button
Array.from(buttons).forEach(el => {
    el.addEventListener('click', (el) => {
        const button = el.target;
        let related_div;

        // Cycle through buttons
        for (let i = 0; i < buttons.length; i++){

            // Get relevent div
            if (buttons[i] == button){
                related_div = document.getElementById(
                    button_reference[buttons[i].id]
                );
            }
        }

        // Hide the rest of the divs
        Array.from(content_divs).forEach(elem => {
            elem.style.display = 'none';
        });

        related_div.style.display = 'flex';
    });
});

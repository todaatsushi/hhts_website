// Hide staff options on load
window.onload = () => {
    const staff_options = document.getElementsByClassName('staff');

    for (let i = 0; i < staff_options.length; i++){
        staff_options[i].style.display = 'none';
    }
}

// If authenticted user clicks the the toggle link, display staff options
const toggle = document.getElementById('user-toggle');

// When user clicks the link, show only staff options
toggle.addEventListener('click', e => {
    const public_options = document.getElementsByClassName('public');
    const staff_options = document.getElementsByClassName('staff');

    // toggle all public
    for (let i = 0; i < public_options.length; i++){
        public_options[i].style.display = public_options[i].style.display == 'none' ? 'block' : 'none';
    }

    // toggle all staff
    for (let i = 0; i < staff_options.length; i++){
        staff_options[i].style.display = staff_options[i].style.display == 'none' ? 'block' : 'none';
    }
})
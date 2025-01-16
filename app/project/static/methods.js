
// Simple function for toggling elements with a button
function toggle(button, element){
        
    el = document.querySelector(element);
    but = document.getElementById(button);
    if(el.style.display == 'none'){
        el.style.display = 'flex';
        //Change displayed text to represent new behaviour      
        but.innerHTML = 'Close';
    }else{
        el.style.display = 'none';
        //Change our text back
        but.innerHTML = but.value;
    }
}
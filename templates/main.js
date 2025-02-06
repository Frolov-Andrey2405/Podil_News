// Show Nav Bar

const nav = document.querySelector('.nav');
const toggle = document.querySelector('.nav-toggle');
const close = document.querySelector('.nav-close');

toggle.addEventListener('click', () => {
    nav.classList.add('show-menu');
    close.classList.add('visible');
})

close.addEventListener('click', () => {
    nav.classList.remove('show-menu');
    close.classList.remove('visible');
})

// Remove Menu Bar on Mobile

const navLink = document.querySelectorAll('.nav-link');
function linkAction() {
    nav.classList.remove('show-menu');
    close.classList.remove('visible');
}
navLink.forEach(n => n.addEventListener('click', linkAction))

// Change active link

const linkColor = document.querySelectorAll('.nav-link');
function colorLink() {
    if (linkColor) {
        linkColor.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    }
}
linkColor.forEach(l => l.addEventListener('click', colorLink))

// Header Shadow

let header = document.getElementById('header');
window.addEventListener('scroll', () => {
    if (window.scrollY >= 70) {
        header.classList.add('header-shadow');
    }
    else header.classList.remove('header-shadow');
})
var alert = document.getElementById('alert');
var navbar = document.getElementById('navbar');

if (alert) {
    navbar.classList.remove('mb-5');
}

alert.addEventListener('closed.bs.alert', function () {
    navbar.classList.add('mb-5');
})
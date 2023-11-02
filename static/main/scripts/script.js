var alert = document.getElementById('alert');
var navbar = document.getElementById('navbar');

if (alert) {
    navbar.classList.remove('mb-3');
}

alert.addEventListener('closed.bs.alert', function () {
    navbar.classList.add('mb-3');
})

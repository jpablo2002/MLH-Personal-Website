////////////////////////////////////////////////////////////
// Hamburger Nav Menu
let menuOpen = false;
const burgerButton = document.querySelector('.burger-button');
const menu = document.querySelector('.menu');

burgerButton.addEventListener('click', () => {
    menu.classList.toggle('open');
})

const slideMenu = document.querySelector('.slide-menu');

slideMenu.addEventListener('click', (e) => {
    e.preventDefault();
    const link = e.target.closest('li');
    if (link?.classList.contains('nav__link')) {
        const id = link.querySelector('a').getAttribute('href');
        document.querySelector(id).scrollIntoView({
            behavior: 'smooth'
        })
    }
})

////////////////////////////////////////////////////////////
// Reveal Elements on Scroll
const sections = document.querySelectorAll('section:not(:first-child)');
let cards = [];

sections.forEach((section) => {
    section.querySelectorAll('div').forEach((card) => card.classList.add('hide-card'))
})

const revealSection = function (entries) {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.querySelectorAll('div').forEach((card) => card.classList.remove('hide-card'))
        } else {
            entry.target.querySelectorAll('div').forEach((card) => card.classList.add('hide-card'))
        }
    })
}

const sectionObserver = new IntersectionObserver(revealSection, {
    root: null,
    threshold: 0.3
});

sections.forEach((section) => {
    sectionObserver.observe(section);
})

////////////////////////////////////////////////////////////
// Map
const colours = {
    "juan": "violet",
    "noah": "blue",
    "malik": "orange"
}

let visited;
const member = window.location.href.split('/').slice(-1)[0];

const memberIcon = new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${colours[member]}.png`,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const map = L.map('map', { scrollWheelZoom: false }).setView([40, 0], 2.2);

fetch(`/visited/${member}`)
    .then((res) => res.json())
    .then((data) => {
        visited = data.visited;
        visited.forEach((place) => {
            L.marker(place[1], { icon: memberIcon })
                .addTo(map)
                .bindPopup(
                    L.popup({
                        maxWidth: 250,
                        minWidth: 100,
                    })
                )
                .setPopupContent(
                    `
                <div class="location-card" style="background-image: url(../static/img/travel-images/${place[0].toLowerCase()}-img.jpg);">
                <h3>
                    ${place[0]}
                </h3>
                <div class="location-info">
                    <p>
                        I visited ${place[0]}.
                    </p>
                </div>
                </div>`
                )
        })
        L.tileLayer(`https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=${data['api_key']}`, {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        document.querySelector('.leaflet-pane.leaflet-popup-pane')?.addEventListener('click', event => {
            event.preventDefault();
        });

    })
    .catch(err => console.log(err))


// Typewriter
let text = document.getElementById('typewriter-text');

setTimeout(() => {
    let typewriter = new Typewriter(text, {
        loop: true
    });

    typewriter
        .typeString('UofT CS Student')
        .pauseFor(2000)
        .deleteAll()
        .typeString('Web Developer')
        .pauseFor(2000)
        .deleteAll()
        .typeString('MLH Fellow')
        .pauseFor(2000)
        .deleteAll()
        .start();
}, 3000)

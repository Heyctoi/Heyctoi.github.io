const ics_events = [];

async function fetch_events(){

<<<<<<< HEAD
    return  fetch('http://heyctoi.unaux.com/Projets/Calendar/events.json')
=======
    return  fetch('https://heyctoi.github.io/events.json')
>>>>>>> cdea53251311c9dd717cffe464ff75d1e38d3a2d
        .then((response) => response.json())
}
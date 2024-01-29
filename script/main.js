const ics_events = [];

async function fetch_events(){

    return  fetch('http://heyctoi.unaux.com/Projets/Calendar/events.json')
        .then((response) => response.json())
}
const ics_events = [];

async function fetch_events(){
    return  fetch('https://heyctoi.github.io/events/events.json').then((response) => response.json())
}
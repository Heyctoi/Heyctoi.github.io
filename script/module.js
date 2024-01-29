import FileSaver from 'https://cdn.skypack.dev/file-saver';
window.download_ics = () => {
    let timeZone = "Europe/Brussels";
    let out =
        "BEGIN:VCALENDAR\n" +
        "VERSION:2.0\n" +
        "CALSCALE:GREGORIAN\n" +
        "PRODID:adamgibbons/ics\n" +
        "METHOD:PUBLISH\n" +
        "X-PUBLISHED-TTL:PT1H\n";

    for (let i = 0; i < ics_events.length; i++) {
        let title = ics_events[i].title;
        let description = ics_events[i].description;
        let location = ics_events[i].location.replaceAll("-","").replaceAll(":","");
        let start = ics_events[i].start.replaceAll("-","").replaceAll(":","");
        let end = ics_events[i].end.replaceAll("-","").replaceAll(":","");
        let status = ics_events[i].status.replaceAll("-","").replaceAll(":","");
        out += "BEGIN:VEVENT\n";
        out += "DTSTAMP:" + status + "Z\n";
        out += "UID:" + ics_events[i].uid + "\n";
        out += "SUMMARY:" + title + "\\n" + description + "\n";
        out += "DTSTART;TZID=" + timeZone + ":" + start + "Z\n";
        out += "DTEND;TZID=" + timeZone + ":" + end + "Z\n";
        out += "LOCATION:" + location + "\n";
        out += "END:VEVENT\n";
    }

    out += "END:VCALENDAR";

    const blob = new Blob([out], {type: 'text/calendar;charset=utf-8'});
    FileSaver.saveAs(blob, "cours.ics");
}


window.download_list = () => {
    let list = {}
    let keys = Object.keys(localStorage);
    for(let key of keys) {
        list[key] = localStorage.getItem(key)
    }
    let out = JSON.stringify(list)
    let blob = new Blob([out], {type: "text/plain;charset=utf-8"});
    FileSaver.saveAs(blob, "list.json");
}

window.upload_list = () => {
    let file = document.getElementById("myFile").files[0];
    console.log(file)
    if (file && file.size > 0){
        readFileContent(file).then(content => {
            let courses = JSON.parse(content)
            localStorage.clear()
            for (let course in courses){
                localStorage.setItem(course,courses[course])
            }
            console.log(courses)
            location.reload()
        }).catch(error => console.log(error))
    }
}

function readFileContent(file) {
    const reader = new FileReader()
    return new Promise((resolve, reject) => {
        reader.onload = event => resolve(event.target.result)
        reader.onerror = error => reject(error)
        reader.readAsText(file)
    })
}
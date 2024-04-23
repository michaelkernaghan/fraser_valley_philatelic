document.addEventListener('DOMContentLoaded', function () {
    const monthNames = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();

    const calendar = document.getElementById('calendar');
    const monthAndYear = document.getElementById('monthAndYear');

    function showCalendar(month, year) {
        let firstDay = new Date(year, month).getDay();
        let daysInMonth = 32 - new Date(year, month, 32).getDate();

        calendar.innerHTML = ""; // clear all previous cells

        monthAndYear.textContent = monthNames[month] + " " + year; // set the month and year header

        let date = 1;
        for (let i = 0; i < 6; i++) { // creates 6 rows for the calendar
            let row = document.createElement("tr");
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    let cell = document.createElement("td");
                    let cellText = document.createTextNode("");
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                } else if (date > daysInMonth) {
                    break;
                } else {
                    let cell = document.createElement("td");
                    let cellText = document.createTextNode(date);
                    if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                        cell.classList.add("bg-blue-500", "text-white"); // highlight today's date
                    }
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                    date++;
                }
            }
            calendar.appendChild(row); // appending each row into calendar body
        }
    }

    showCalendar(currentMonth, currentYear); // call function to generate calendar
});

document.getElementById('sort').addEventListener('change', function() {
    sortGallery(this.value);
});

document.getElementById('filter').addEventListener('change', function() {
    filterGallery(this.value);
});

document.getElementById('search').addEventListener('keyup', function() {
    searchGallery(this.value);
});

function sortGallery(criteria) {
    // Add sorting logic based on criteria: name, date, or country
}

function filterGallery(country) {
    // Filter gallery items based on the selected country
    const stamps = document.querySelectorAll('.gallery a');
    stamps.forEach(stamp => {
        stamp.style.display = stamp.getAttribute('data-country') === country || country === 'all' ? '' : 'none';
    });
}

function searchGallery(query) {
    // Filter gallery items based on search query
    const stamps = document.querySelectorAll('.gallery a');
    stamps.forEach(stamp => {
        const title = stamp.getAttribute('data-title').toLowerCase();
        stamp.style.display = title.includes(query.toLowerCase()) ? '' : 'none';
    });
}

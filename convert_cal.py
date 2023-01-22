from icalendar import Calendar, Event
import re
from datetime import datetime, timedelta

year = 2023


_RE_COMBINE_WHITESPACE = re.compile(r"\s+")
cal = Calendar()
cal.add('prodid', '-//Heimatverein Halen//halen.de Dorfkalender//')
cal.add('version', '2.0')

lines = []

with open(f'calendar_{year}.txt') as f:
    for line in f:
        line = _RE_COMBINE_WHITESPACE.sub(" ", line).strip()
        if len(line) > 0 and line[0].isdigit():
            lines.append(line)

for line in lines:
    date_start_str, desc = line.split('. ', 1)
    date_start = datetime.strptime(date_start_str, '%d.%m')
    if desc.strip().startswith('-'):
        date_end_str, desc = desc.strip("- ").split('. ', 1)
        date_end = datetime.strptime(date_end_str, '%d.%m')
    else:
        date_end = date_start + timedelta(days=1)
    date_start = date_start.replace(year=year).date()
    date_end = date_end.replace(year=year).date()

    event = Event()
    event.add('summary', desc.strip())
    event.add('dtstart', date_start)
    event.add('dtend', date_end)
    cal.add_component(event)

with open(f"calendar_{year}.ics", "wb") as f:
    f.write(cal.to_ical())

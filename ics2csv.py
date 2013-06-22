#!/usr/bin/env python
import sys
import csv
from datetime import timedelta
from icalendar import Calendar, Event

# ICS files are in GMT; Guidebook has no concept of timezones, it just displays
# whatever time you give it. It makes sense to display in local time of the conference,
# so this variable defines which is the timezone at the time the conference runs.
LOCAL_TIMEZONE = timedelta(hours=2)

def convert(fn):
    out = csv.writer(sys.stdout)
    out.writerow([
        "Session Title","Date","Time Start","Time End",
        "Room/Location","Schedule Track (Optional)","Description (Optional)",
    ])
    cal = Calendar.from_ical(open(fn,'rb').read())
    for event in cal.walk():
        if isinstance(event, Event):
            start = event.decoded("DTSTART") + LOCAL_TIMEZONE
            end = event.decoded("DTEND") + LOCAL_TIMEZONE

            out.writerow([
                event.decoded("SUMMARY"),
                start.date(),
                start.time(),
                end.time(),
                "",
                event.decoded("LOCATION"),
                event.decoded("DESCRIPTION"),
            ])


if __name__ == "__main__":
    convert(sys.argv[1])

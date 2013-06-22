#!/usr/bin/env python
import sys
import csv
from icalendar import Calendar, Event

def convert(fn):
    out = csv.writer(sys.stdout)
    out.writerow([
        "Session Title","Date","Time Start","Time End",
        "Room/Location","Schedule Track (Optional)","Description (Optional)",
    ])
    cal = Calendar.from_ical(open(fn,'rb').read())
    for event in cal.walk():
        if isinstance(event, Event):
            start = event.decoded("DTSTART")
            end = event.decoded("DTEND")

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

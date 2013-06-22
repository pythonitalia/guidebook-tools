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

    helpdesks = {}

    cal = Calendar.from_ical(open(fn,'rb').read())
    for event in cal.walk():
        if isinstance(event, Event):
            start = event.decoded("DTSTART") + LOCAL_TIMEZONE
            end = event.decoded("DTEND") + LOCAL_TIMEZONE
            title = event.decoded("SUMMARY")
            track = event.decoded("LOCATION")
            abstract = event.decoded("DESCRIPTION")

            if "desk" in track.lower():
                if (title, start.date()) in helpdesks:
                    s1, e1, _ = helpdesks[(title, start.date())]
                    date = start.date()
                    start = min(s1, start.time())
                    end = max(e1, end.time())
                else:
                    date = start.date()
                    start = start.time()
                    end = end.time()
                helpdesks[(title, date)] = start, end, abstract
                continue

            out.writerow([
                title,
                start.date(),
                start.time(),
                end.time(),
                "",
                track,
                abstract,
            ])

    for (title,date),(start,end,abstract) in helpdesks.items():
        out.writerow([
            title,
            date,
            start,
            end,
            "",
            "Track: Help Desk",
            abstract,
        ])


if __name__ == "__main__":
    convert(sys.argv[1])

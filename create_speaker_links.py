import sys
import csv

def create_links(fn_talks, fn_speakers):
    speakers = {}

    out = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    out.writerow([
        "Session ID (Optional)",
        "Session Name (Optional)",
        "Link To Session ID (Optional)",
        "Link To Session Name (Optional)",
        "Link To Item ID (Optional)",
        "Link To Item Name (Optional)",
        "Link To Form Name (Optional)",
    ]) 

    scsv = csv.DictReader(open(fn_speakers))
    for s in scsv:
        fullname = s["Name"]
        family = fullname.split()[-1]
        assert family not in speakers
        speakers[family] = fullname

    talks = csv.DictReader(open(fn_talks))
    for t in talks:
        talk = t["Session Title"]
        if "by" not in talk:
            print >>sys.stderr, "WARNING: skipping", talk
            continue
        names = talk.partition("by")[2]
        names = names.split(",")
        for n in names:
            family = n.strip().split()[-1]
            if family not in speakers:
                print >>sys.stderr, "ERROR: cannot find speaker", n
                sys.exit(2)

            try:
                talk_l1 = talk.decode("utf-8").encode("latin1")
            except:
                talk_l1 = talk
            try:
                speaker_l1 = speakers[family].decode("utf-8").encode("latin1")
            except:
                speaker_l1 = speakers[family]

            out.writerow([
                "", talk,
                "", "",
                "", speakers[family],
                "Talk rating",
            ])


if __name__ == "__main__":
	create_links(sys.argv[1], sys.argv[2])

import os
import sys
import re
import _bibtex

f = _bibtex.open_file(sys.argv[1], True)

l = []
while 1:
    entry = _bibtex.next_unfiltered(f)
    if entry is None:
        break

    if entry[0] != 'entry':
        # skip
        continue

    l.append(entry)


pubs = ""

for entry in l:
    name = entry[1][0]
    entry = entry[1][4]
    pubs += '- name: %s\n' % name

    # author
    assert 'author' in entry

    data = _bibtex.expand(f, entry['author'], -1)[2].strip()
    pubs += "  authors: \"%s\"\n" % data

    # title
    assert 'title' in entry

    data = _bibtex.expand(f, entry['title'], -1)[2].strip()
    pubs += "  title: \"%s\"\n" % data

    # booktitle
    if 'booktitle' in entry:
        data = _bibtex.expand(f, entry['booktitle'], -1)[2].strip()
    elif 'journal' in entry:
        data = _bibtex.expand(f, entry['journal'], -1)[2].strip()
        if 'pages' in entry:
            pages = _bibtex.expand(f, entry['pages'], -1)[2].strip()
            data += ", Pages %s" % pages
        if 'number' in entry:
            number = _bibtex.expand(f, entry['number'], -1)[2].strip()
            data += ", Number %s" % number
        if 'volume' in entry:
            volume = _bibtex.expand(f, entry['volume'], -1)[2].strip()
            data += ", Volume %s" % volume
    elif 'inproceedings' in entry:
        data = _bibtex.expand(f, entry['inproceedings'], -1)[2].strip()
    else:
        assert False
    pubs += "  venue: \"%s\"\n" % data

    # Location
    if 'address' in entry:
        data = _bibtex.expand(f, entry['address'], -1)[2].strip()
        pubs += "  address: \"%s\"\n" % data
    
    # date
    assert 'year' in entry
    yr = _bibtex.expand(f, entry['year'], -1)[2].strip()
    if 'month' in entry:
        mo = _bibtex.expand(f, entry['month'], -1)[2].strip()
        mo += ", "
    else:
        mo = ""
    pubs += "  date: \"%s%s\"\n" % (mo, yr)

    
    # File(s) detection
    cwd = os.getcwd()
    pdf = name.split(":")[0] + ".pdf"
    bib = name.split(":")[0] + ".bib"
    lec = "lecture_" + name.split(":")[0] + ".pdf"
    if os.path.exists(os.path.join(cwd, pdf)):
        pubs += "  pdf: %s\n" % pdf
    if os.path.exists(os.path.join(cwd, bib)):
        pubs += "  bib: %s\n" % bib
    if os.path.exists(os.path.join(cwd, lec)):
        pubs += "  lec: %s\n" % lec
        
    pubs += "\n"

# some hacks
pubs = pubs.replace("$^st$", "st")
pubs = pubs.replace("$^{st}$", "st")
pubs = pubs.replace("$^nd$", "nd")
pubs = pubs.replace("$^rd$", "rd")
pubs = pubs.replace("$^th$", "th")
pubs = pubs.replace("$^{th}$", "th")
pubs = pubs.replace("&", "&amp;")

print pubs

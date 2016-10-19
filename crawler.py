import requests
import json
from bs4 import BeautifulSoup

transient_data = {}
transient_array = []
#change this to wherever you would like the file to save to
path_name = "/Users/landon/Desktop/testJSON"

#transient class to create transient objects to be added to an array
class transient:

    def __init__(self, i_d, ra, dec, ut, mag, last, light):
        self.i_d = i_d
        self.ra = ra
        self.dec = dec
        self.ut = ut
        self.mag = mag
        self.last = last
        self.light = light

    def get_id(self):
        return self.i_d

    def get_ra(self):
        return self.ra

    def get_dec(self):
        return self.dec

    def get_ut(self):
        return self.ut

    def get_mag(self):
        return self.mag

    def get_last(self):
        return self.last

    def get_light(self):
        return self.light

    def show_details(self):
        return self.i_d + " " + self.ra
'''
crawls the website specified and finds the table on the website and returns
the rows
'''
def LSST_crawler():
    url = "http://nesssi.cacr.caltech.edu/MLS/CRTSII_Allns.html"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    table = soup.findChildren("table")
    my_table = table[0]

    rows = my_table.findChildren(["th", "tr"])
    return rows

'''
takes in the rows from the LSST_crawler() function and goes through the rows
and gets the data in the cells and strips the whitespace from them
'''
def set_data(rows):
    for row in rows:
        cells = row.findChildren("td")
        for cell in cells[:8]:
            crts_id = cells[0].text.lstrip().rstrip()
            ra = cells[1].text.lstrip().rstrip()
            dec = cells[2].text.lstrip().rstrip()
            ut_date = cells[3].text.lstrip().rstrip()
            mag = cells[4].text.lstrip().rstrip()
            last = cells[6].text.lstrip().rstrip()
            light_curve = cells[7].text.lstrip().rstrip()
            trans = transient(crts_id, ra, dec, ut_date, mag, last, light_curve)
            transient_array.append(trans)
            break
#takes the transient objects inside the transient_array and creates dictionary objects
def set_JSON():
    for t in transient_array:
        transient_data[t.get_id()] = {
            'ra' : t.get_ra(),
            'dec' : t.get_dec(),
            'ut_date' : t.get_ut(),
            'mag' : t.get_mag(),
            'last_time' : t.get_last(),
            'light_curve' : t.get_light()
        }
    j = json.dumps(transient_data)
    #writes them to a file at a certain path
    with open("%s" % path_name, "w") as f:
        f.write(j)
        print("JSON file created")


set_data(LSST_crawler())
set_JSON()
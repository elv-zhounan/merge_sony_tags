# translate from xml to json

import xml.etree.ElementTree as E
import json

def translate(src:str, dst:str=None):
    tree = E.parse(src)
    root = tree.getroot()[0]
    res = {
        "version": 1,
        "metadata_tags": {}
    }
    for feat in root:
        name = feat.attrib["name"]
        if "Timeline" in name:
            print(name)
            key = name.lower().replace(".", "_")
            label = name.replace(".", "")
            tags = []

            txt = feat.text
            while True:
                s = txt.find("[")
                e = txt.find("]")
                timetxt = txt[s+1: e]
                txt = txt[e+1: ]
                s_next = txt.find("[")
                if s_next == -1:
                    content = txt
                else:
                    content = txt[:s_next]
                    txt = txt[s_next: ]
                
                # TODO not sure what ss means 
                h, m, s, ss = timetxt.split("-")[0].split(":")
                start_time = (3600*int(h) + 60*int(m) + int(s))*1000 + int(int(ss)/60*1000)
                h, m, s, ss = timetxt.split("-")[1].split(":")
                end_time = (3600*int(h) + 60*int(m) + int(s))*1000 + int(int(ss)/60*1000)

                if not content.startswith(" -"):
                    tags.append({
                        "start": start_time,
                        "end": end_time,
                        "text":[content.strip()]
                    })
                else:
                    content = [c.strip() for c in content.split(" -")[1:]]
                    tags.append({
                        "start": start_time,
                        "end": end_time,
                        "text":content
                    })
                if s_next == -1 or txt.strip() == "":
                    break
            res["metadata_tags"][key] = {
                "label": label,
                "tags": tags
            }
    
    json.dump(res, open("test_translate.json", "w"))
if __name__ == "__main__":
    translate('./sony_tags_xml/845138_s01_Ghosbusters_1984.xml')
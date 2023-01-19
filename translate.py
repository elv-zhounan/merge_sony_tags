# translate from xml to json

import xml.etree.ElementTree as E
import json
import os
import tqdm

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
            label = name.replace(".", " ")
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
                
                # TODO some format issue in xml tags from sony
                # need to check more
                if len(timetxt) > 0 and timetxt != "00:00:00:00-00:00:00:00":
                    while timetxt[0] > "9" or timetxt[0] < "0":
                        timetxt = timetxt[1:]
                    timetxt = timetxt[:23].replace(";", ":")
                    h, m, s, ss = timetxt.split("-")[0].split(":")
                    start_time = (3600*int(h) + 60*int(m) + int(s))*1000 + int(int(ss)/24*1000)
                    h, m, s, ss = timetxt.split("-")[1].split(":")
                    end_time = (3600*int(h) + 60*int(m) + int(s))*1000 + int(int(ss)/24*1000)
                    if end_time <= start_time:
                        print(timetxt)
                    else:
                        if key == "transcript_timeline":
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
                        else:
                            content = [c.strip() for c in content.split(";")]
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

    json.dump(res, open(dst, "w"))

if __name__ == "__main__":
    # translate('./sony_tags_xml/845138_s01_Ghosbusters_1984.xml')
    objects = sorted(os.listdir("sony_tags_xml"))
    if ".DS_Store" in objects:
        objects.remove(".DS_Store")

    for object in tqdm.tqdm(objects):
        print(object)
        translate(f"./sony_tags_xml/{object}", f"./translated_tags_json/{object.replace('.xml', '.json')}")
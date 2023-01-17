import json
import os
import tqdm

def clean_shot_tags(shot_tags):
    # downloaded using js, not with a clean format
    res = {
        "label": "Shot Tags",
        "tags": []
    }
    for part in shot_tags:
        res["tags"].extend(part["tags"])
    return res

def shot_merge_features(shot_tags, feat_tags, merge=True):
    # change the label name, specify it is from sony
    label = feat_tags["label"]
    if not label.startswith("Sony"):
        label =  "Sony " + label
    # just in case that the tags is not sorted, since we are using an ugly implementation below
    sorted_tags = sorted(feat_tags["tags"], key=lambda x: x["start"])
    # insert the new tracks
    for i in range(len(shot_tags["tags"])):
        if label not in shot_tags["tags"][i]["text"]:
            shot_tags["tags"][i]["text"][label] = []
    # copy from tagger utils agg.py, 
    # an ugly implement with O(n^2)
    for i in range(len(shot_tags["tags"])):
        shot = shot_tags["tags"][i]
        shot["text"][label] = list()

        for t in sorted_tags:
            if t["start"] >= shot["end_time"]:
                break
            elif t["end"] > shot["start_time"]:
                shot["text"][label].append({
                    "start_time": t["start"],
                    "end_time": t["end"],
                    "text": t["text"]
                })
    
    return shot_tags

if __name__ == "__main__":
    objects = sorted(os.listdir("sony_tags_json"))
    objects.remove(".DS_Store")

    for object in tqdm.tqdm(objects):
        objectId = "_".join(object.split("_")[:3])
        elv_tags = clean_shot_tags(json.load(open(f"elv_tags_json/{objectId}_shot_tags.json")))
        sony_tags = json.load(open(f"sony_tags_json/{object}"))
        sony_features = list(sony_tags["metadata_tags"].keys())        

        merged_tags = elv_tags
        using_sony_features = json.load(open("using_sony_features.json"))

        for feature in sony_features:
            if feature in using_sony_features:
                merged_tags = shot_merge_features(merged_tags, sony_tags["metadata_tags"][feature])

        json.dump(merged_tags, open(f"merged_tags_json/{object.split('.')[0]}_shot_tags.json", "w"))

        """debug use, only test one object one feature"""
        # break
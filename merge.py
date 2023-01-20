import copy
import json
import os
import tqdm
import argparse

def clean_shot_tags(shot_tags):
    # downloaded using js, not with a clean format
    res = {
        "label": "Shot Tags",
        "tags": []
    }
    cuts = []
    for part in shot_tags:
        res["tags"].extend(part["tags"])
        cuts.append(len(part["tags"]))
    return res, cuts

def split(merged_tags, cuts):
    res =[]

    tags = merged_tags["tags"]

    for cut in cuts[:-1]:
        chunks = tags[:cut]
        tags = tags[cut: ]
        res.append({
            "label": "Shot Tags",
            "tags": chunks
        })
    res.append({
        "label": "Shot Tags",
        "tags": tags
    })
    return res

def shot_merge_features(shot_tags, feat_tags, label):
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
        if shot["start_time"] < shot["end_time"]:
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

def add_empty_feature(shot_tags, label):
    for i in range(len(shot_tags["tags"])):
        shot_tags["tags"][i]["text"][label] = []
    return shot_tags


def safety_check_part(pre_part, post_part):
    # 1. check start time and end_time is the same
    assert pre_part["start_time"] == post_part["start_time"]
    assert pre_part["end_time"] == post_part["end_time"]
    shot_s = pre_part["start_time"]
    shot_e = pre_part["end_time"]
    assert shot_e >= shot_s
    # 2 check if the new added tags' time ranges have overlap with the shots
    for feat in post_part["text"]:
        for tag in post_part["text"][feat]:
            tag_s = tag["start_time"]
            tag_e = tag["end_time"]
            # 2.1 check start time <= end time
            assert tag_e >= tag_s
            # 2.2 check overlap
            assert max(shot_e, tag_e) - min(shot_s, tag_s) <= (shot_e-shot_s) + (tag_e-tag_s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', action="store_true")
    args = parser.parse_args()
                
    objects = sorted(os.listdir("sony_tags_json"))
    if ".DS_Store" in objects:
        objects.remove(".DS_Store")

    bar = tqdm.tqdm(objects)
    for object in bar:
        bar.set_postfix_str(object)
        objectId = "_".join(object.split("_")[:3])
        elv_tags = json.load(open(f"elv_tags_json/{objectId}_shot_tags.json"))
        elv_tags, cuts = clean_shot_tags(elv_tags)
        sony_tags = json.load(open(f"sony_tags_json/{object}"))
        sony_features = list(sony_tags["metadata_tags"].keys())
        using_sony_features = json.load(open("using_sony_features.json"))

        merged_tags = elv_tags
        for feature in using_sony_features:
            if feature in sony_features:
                merged_tags = shot_merge_features(merged_tags, sony_tags["metadata_tags"][feature], using_sony_features[feature])
            else:
                merged_tags = add_empty_feature(merged_tags, using_sony_features[feature])

        # basic check
        assert len(merged_tags["tags"]) == sum(cuts)
        elv_tags = json.load(open(f"elv_tags_json/{objectId}_shot_tags.json"))
        if args.split:
            merged_tags = split(merged_tags, cuts)
            # safety check
            for (pre_parts, post_parts) in zip(elv_tags, merged_tags):
                # check len is the same
                assert len(pre_parts) == len(post_parts)
                for pre_part, post_part in zip(pre_parts["tags"], post_parts["tags"]):
                    safety_check_part(pre_part, post_part)

        else:
            elv_tags, _ = clean_shot_tags(elv_tags)
            assert len(elv_tags) == len(merged_tags)
            for pre_part, post_part in zip(elv_tags["tags"], merged_tags["tags"]):
                safety_check_part(pre_part, post_part)


        json.dump(merged_tags, open(f"merged_tags_json/{object.split('.')[0]}_shot_tags.json", "w"))

        """debug use, only test one object one feature"""
        # break
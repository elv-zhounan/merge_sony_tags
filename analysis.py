# analysis the tags given by sony
# it seems that the time range is too long, and search res may return too many shots
import json
import os
from merge import clean_shot_tags
import matplotlib.pyplot as plt

# algo: similar to using binary search to find the insert place
def helper_l(arr, s):
    l =  0
    r = len(arr) - 1
    if s >= arr[-1]:
        return r
    if s == arr[0]:
        return 0
    while r >= l:
        m = (r+l) // 2
        if arr[m] == s:
            return m
        elif arr[m] < s:
            l = m+1
        else:
            r = m-1
    return l-1

def helper_r(arr, e):
    l =  0
    r = len(arr) - 1
    if e <= arr[0]:
        return 0
    if e == arr[-1]:
        return r
    while r >= l:
        m = (r+l) // 2
        if arr[m] == e:
            return m
        elif arr[m] < e:
            l = m+1
        else:
            r = m-1
    return l


def cnt_shot_covered(shot_tags, feat_tags):
    # shots ar enot supposed to have overlaps and should be sorted
    shot_starts = []
    shot_ends = []
    for i in range(len(shot_tags["tags"])):
        shot_starts.append(shot_tags["tags"][i]["start_time"])
        shot_ends.append(shot_tags["tags"][i]["end_time"])
    assert len(shot_ends) > 0
    assert len(shot_ends) == len(shot_starts)
    cnt = []
    for t in feat_tags["tags"]:
        s = t["start"]
        e = t["end"]
        if shot_starts[0] <= s <= shot_ends[-1] and shot_starts[0] <= s <= shot_ends[-1]:
            l = helper_l(shot_starts, s)
            r = helper_r(shot_ends, e)
            cnt.append(r  - l + 1)

    return cnt

    

if __name__ == "__main__":
    objects = sorted(os.listdir("sony_tags_json"))
    objects.remove(".DS_Store")

    for object in objects:
        print(object)
        objectId = "_".join(object.split("_")[:3])
        elv_tags = clean_shot_tags(json.load(open(f"elv_tags_json/{objectId}_shot_tags.json")))
        sony_tags = json.load(open(f"sony_tags_json/{object}"))
        sony_features = list(sony_tags["metadata_tags"].keys())        

        merged_tags = elv_tags
        using_sony_features = json.load(open("using_sony_features.json"))

        names = []
        means = []
        for feature in sony_features:
            if feature in using_sony_features:
                cnt = cnt_shot_covered(merged_tags, sony_tags["metadata_tags"][feature])
                print(feature, sum(cnt) / len(cnt))
                names.append(feature)
                means.append(sum(cnt) / len(cnt))
        plt.figure(figsize=(16, 24))
        plt.bar(names, means)
        plt.xticks(rotation=300)
        for a,b in zip(names, means):
            plt.text(a,b,
                    round(b, 2),
                    ha='center', 
                    va='bottom',
                    )
        plt.savefig(f"shot_covered/{object.split('.')[0]}_shot_covered.jpg")
        


        """debug use, only test one object one feature"""
        # break

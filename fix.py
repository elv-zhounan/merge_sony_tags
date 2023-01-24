import json

tags = json.load(open("/Users/zhounanli/Desktop/work/merge_sony_tags/sony_tags_json/iq__XNK9QbS3weGCm3qDVFvpPsZpLAS_s01_Men_In_Black.json"))

res = {}

for k in tags["metadata_tags"]:
    res[k] = tags["metadata_tags"][k]["label"]

json.dump(res, open("all_sony_features.json", "w"))
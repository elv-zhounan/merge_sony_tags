import argparse
import json
import os

def split(sony_feat_track, part_cnt, part_duration=600600):
    part_starts = [part_duration*i for i in range(part_cnt)]
    part_ends = [part_duration*(i+1) for i in range(part_cnt)]
    res = [[] for _ in range(part_cnt)]
    for tag in sony_feat_track:
        s = tag["start"]
        e = tag["end"]
        # the last one
        if s >= part_starts[-1]:
            res[-1].append({
                "start_time": s,
                "end_time": min(part_ends[-1], e),
                "text": tag["text"]
            })
        else:
            for i, (part_start, next_part_start) in enumerate(zip(part_starts[:-1], part_starts[1:])):
                if s >=  part_start and s < next_part_start-1:
                    res[i].append({
                        "start_time": s,
                        "end_time": min(e, part_ends[i]),
                        "text": tag["text"]
                    })
                    # not sure how should do with case , need discussion
                    if e > next_part_start:
                        res[i+1].append({
                            "start_time": next_part_start,
                            "end_time": e,
                            "text": tag["text"]
                        })
    return res

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default="", type=str)
    args = parser.parse_args()

    merged_files = os.listdir("./merged_tags_json")
    for file in merged_files:
        if args.id == "" or (args.id != ""  and file.startswith(args.id)):
            shot_tags = json.load(open(f"./merged_tags_json/{file}"))
            objectId = "_".join(file.split("_")[:3])
            print(objectId)

            all_sony_feats = json.load(open(f"./sony_tags_json/{file.replace('_shot_tags', '')}"))["metadata_tags"]
            sony_feats_in_use = json.load(open("./using_sony_features.json"))
            sony_feats = {}
            for feat in all_sony_feats:
                if feat in sony_feats_in_use:
                    sony_feats[feat] = all_sony_feats[feat]
            for feat in sony_feats:
                sony_feats[feat] = split(sony_feats[feat]["tags"], len(shot_tags))


            track_tags = json.load(open(f"./elv_track_tags_json/{objectId}_track_tags.json"))
            assert len(track_tags) == len(shot_tags)

            save_root = f"./final_res/{objectId}"
            if not os.path.exists(save_root):
                os.makedirs(save_root)
            for i, (shot_tag, track_tag) in enumerate(zip(shot_tags, track_tags)):
                track_tag["shot_tags"] = shot_tag
                # add sony feat in
                for feat in sony_feats:
                    track_tag[feat] = {
                        "label": sony_feats_in_use[feat],
                        "tags": sony_feats[feat][i]
                    }
                track_tag = {
                    "version": 1,
                    "video_level_tags": {},
                    "metadata_tags": track_tag
                }
                file_name = f"video-tags-tracks-{str(i).zfill(4)}.json"
                json.dump(track_tag, open(os.path.join(save_root, file_name), "w"))
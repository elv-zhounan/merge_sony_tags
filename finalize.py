import json
import os

if __name__ == "__main__":
    merged_files = os.listdir("./merged_tags_json")
    print(merged_files)
    for file in merged_files:
        shot_tags = json.load(open(f"./merged_tags_json/{file}"))
        objectId = "_".join(file.split("_")[:3])
        print(objectId)
        track_tags = json.load(open(f"./elv_track_tags_json/{objectId}_track_tags.json"))
        assert len(track_tags) == len(shot_tags)

        save_root = f"./final_res/{objectId}"
        if not os.path.exists(save_root):
            os.makedirs(save_root)
        for i, (shot_tag, track_tag) in enumerate(zip(shot_tags, track_tags)):
            track_tag["shot_tags"] = shot_tag
            track_tag = {
                "version": 1,
                "video_level_tags": {},
                "metadata_tags": track_tag
            }
            file_name = f"video-tags-tracks-{str(i).zfill(4)}.json"
            json.dump(track_tag, open(os.path.join(save_root, file_name), "w"))

# About merge tags from sony to our tags for search usage

## tasks done

- [x] download tags from fabric
- [x] merge to shot tags
- [x] a few analysis
- [x] translate from xml to json
- [] check the res, upload to fabric and create search index; may need to discuss the file name since we would like to keep our own res

## example for one shot

```json
{
      "end_time": 72281,
      "start_time": 71697,
      "text": {
        "Celebrity Detection": [],
        "Landmark Recognition": [],
        "Logo Detection": [],
        "Object Detection": [],
        "Optical Character Recognition": [],
        "Segment Labels": [
          {
            "end_time": 75060,
            "start_time": 70060,
            "text": [
              "Car",
              "Sport utility vehicle",
              "BMW",
              "Police car",
              "Mini (marque)"
            ]
          }
        ],
        "Speech to Text": [],
        "Sony Description Keywords Timeline": [
          {
            "start_time": 45834,
            "end_time": 135583,
            "text": [
              "city streets",
              "cities",
              "high rises",
              "office buildings",
              "driving",
              "swerving",
              "police officers",
              "chasing",
              "car chases",
              "bullets",
              "sirens",
              "lights",
              "flashing lights",
              "radios",
              "walkie talkies",
              "Park Avenue",
              "jumping",
              "hitting",
              "SUVs",
              "guns",
              "shooting",
              "sparks",
              "hoods",
              "intersections",
              "near collisions",
              "honking",
              "buses",
              "double decker tour buses",
              "crashing",
              "main titles"
            ]
          }
        ],
        "Sony Description Location Timeline": [
          { "start_time": 45834, "end_time": 135583, "text": ["New York"] }
        ],
        "Sony Description Memorable Timeline": [
          {
            "start_time": 45834,
            "end_time": 135583,
            "text": [
              "opening scene",
              "car chase",
              "action sequence",
              "narration"
            ]
          }
        ],
        "Sony Description Setting Timeline": [
          { "start_time": 45834, "end_time": 135583, "text": ["New York"] }
        ],
        "Sony Description Theme Timeline": [
          {
            "start_time": 45834,
            "end_time": 135583,
            "text": ["law enforcement"]
          }
        ],
        "Sony Description Tone Timeline": [
          {
            "start_time": 45834,
            "end_time": 135583,
            "text": ["exciting", "funny", "action-packed"]
          }
        ],
        "Sony Facial ActorName Timeline": [],
        "Sony Facial CharacterName Timeline": [],
        "Sony Keywords Audio Timeline": [],
        "Sony Scene ShortDesc Timeline": [
          {
            "start_time": 45834,
            "end_time": 135583,
            "text": [
              "Danson and Highsmith chase down criminals on the streets of New York."
            ]
          }
        ],
        "Sony ACP ShortDesc Timeline": [],
        "Sony ClipAndShare ShortDesc Timeline": [],
        "Sony ClipAndShare Title Timeline": [],
        "Sony Crackle ShortDescription Timeline": [],
        "Sony ITunesExtra ShortDesc Timeline": [
          {
            "start_time": 54750,
            "end_time": 192959,
            "text": [
              "Danson and Highsmith chase down criminals on the streets of New York."
            ]
          }
        ],
        "Sony MDC ShortDescription Timeline": [],
        "Sony Music Title Timeline": [
          {
            "start_time": 54708,
            "end_time": 131375,
            "text": ["Saturday Night"]
          }
        ],
        "Sony Transcript Timeline": []
      }
    },
```

## need to discuss

1. sony xml format is not good json files given by marc is good. are those json files from sony or marc?

   1. some timestamps are empty
      - []
      - [00:00:00:00-00:00:00:00]
   2. sime timestamps are with bad formatfor example
      - [00:04:22:21-00:04:26;10/1.0]
      - [ [01:14:09:00-01:18:48:09]
      - not sure if there are any other special cases
   3. the content format:
      - in transcripts, sentences are seperated using -
      - in others, according to my check res, items are seperated using ;

   not sure if there are any other strang format I should pay attention to

2. what features we would like to add? currently I added:

   1. "description_keywords_timeline"
      - including object, emotion, action, places
   2. "description_location_timeline"
      - location, including from small buildings (library) to US states
   3. "description_memorable_timeline"
      - not sure, seems like summarizing what was happening in that time period
   4. "description_setting_timeline"
      - similar to location time line
   5. "description_theme_timeline"
   6. "description_tone_timeline"
   7. "facial_actorname_timeline"
   8. "facial_charactername_timeline"
   9. "keywords_audio_timeline"
      - provides some keywords in the audio
   10. "scene_shortdesc_timeline
       - summarying the scene
   11. "sony_acp_shortdesc_timeline"
       - summarizing the short story
   12. "sony_clipandshare_shortdesc_timeline"
       - summarizing the short story, not sure about the difference from 11
   13. "sony_clipandshare_title_timeline"
       - the title the scene (chapter)
   14. "sony_crackle_shortdescription_timeline"
       - scene short descrption
   15. "sony_itunesextra_shortdesc_timeline"
       - scene short descrption
   16. "sony_mdc_shortdescription_timeline"
       - scene short descrption
   17. "sony_music_title_timeline"
       - music title
   18. "sony_sceneslam_title_timeline"
       - ???
   19. "transcript_timeline"

   there are several kinds of scene discrption, we may need to drop some

3. for search, it seems like we are only using shot_tags track, can we only save shot_tags to make files smaller?
4. tags from sony is covering too many shots which may not be a good case
   - can view some results in shot_covered folder
5. more analysis if needed

# About merge tags from sony to our tags for search usage

## tasks done

- [x] download tags from fabric
- [x] merge to shot tags
- [x] a few analysis
- [] translate from xml to json

## need to discuss

1. sony xml format is not good, json files given by marc is good. are those json files from sony or marc?
   1. some timestamps are empty
      - []
      - [00:00:00:00-00:00:00:00]
   2. sime timestamps are with bad format,for example
      - [00:04:22:21-00:04:26;10/1.0]
      - [ [01:14:09:00-01:18:48:09]
      - not sure if there are any other special cases
2. what features we would like to add
3. for search, seems like we are only using shot_tags tracks, can we just save shot_tags to make files smaller?
4. tags from sony is covering too many shots, which may not be a good case
5. maybe more analysis

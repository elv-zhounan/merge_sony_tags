const { ElvClient } = require("@eluvio/elv-client-js");
const fs = require("fs");
const tasks = [
  "iq__XNK9QbS3weGCm3qDVFvpPsZpLAS",
  "iq__3HaR3PRoQnFPMaznzkzDmVHYGxyH",
  "iq__bQt9d3PwJtUzLjowrwEYyA5ryRh",
  "iq__4EDE5uJU3KyVeNAnVwsKEMU2EmRG",
  "iq__MMfCssGQD6pmvgAGBnaDujeSdFa",
  "iq__26cohKnQhoSQQ5X4Vvmn5YE9QeeY",
  "iq__BRU3kSBdbqXedib88DXujJMEKqC",
  "iq__3RpLVUNcnMjSmTR2QKEiCTppyRi4",
  "iq__kT9h4cYqoNZyyK69gvF7pU4Rtdg",
  "iq__3QAJZw8sTkm5E9A6WaxhcAX4LTf9",
];
const getClient = async () => {
  var client = await ElvClient.FromConfigurationUrl({
    configUrl: "https://main.net955305.contentfabric.io/config",
  });
  const wallet = client.GenerateWallet();
  const signer = wallet.AddAccount({ privateKey: process.argv[2] });
  client.SetSigner({ signer });
  return client;
};

getClient()
  .then(async (client) => {
    try {
      for (let objectId of tasks) {
        const libraryId = await client.ContentObjectLibraryId({
          objectId,
        });
        const all_part_tags = await client.ContentObjectMetadata({
          libraryId,
          objectId,
          metadataSubtree: "video_tags/metadata_tags",
        });
        console.log(all_part_tags);
        let shot_tags = [];
        for (let k in all_part_tags) {
          const tags = await client.ContentObjectMetadata({
            libraryId,
            objectId,
            metadataSubtree: `video_tags/metadata_tags/${k}/metadata_tags`,
          });
          console.log(tags.shot_tags);
          shot_tags = shot_tags.concat(tags.shot_tags);
        }
        fs.writeFileSync(
          `./${objectId}_shot_tags.json`,
          JSON.stringify(shot_tags)
        );
      }
    } catch (err) {
      console.log(err);
    }
  })
  .catch((err) => {
    console.log(err);
  });

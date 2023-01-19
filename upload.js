const { ElvClient } = require("@eluvio/elv-client-js");
const fs = require("fs");
const tasks = [
  //   "iq__XNK9QbS3weGCm3qDVFvpPsZpLAS",
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

const uploadFile = async (
  client,
  libraryId,
  objectId,
  filename,
  writeToken
) => {
  try {
    const data = JSON.stringify(
      JSON.parse(
        fs.readFileSync(`./final_res/${objectId}/${filename}`).toString()
      )
    );
    const bufferData = Buffer.from(data);
    console.log(bufferData.length);

    try {
      await client.UploadFiles({
        libraryId,
        objectId,
        writeToken,
        fileInfo: [
          {
            path: `/video_tags/${filename}`,
            mime_type: "application/json",
            size: bufferData.length,
            data: bufferData,
          },
        ],
      });
    } catch (err) {
      console.log(err);
    }
  } catch (err) {
    console.log(err);
  }
};

getClient()
  .then(async (client) => {
    try {
      for (let objectId of tasks) {
        const libraryId = await client.ContentObjectLibraryId({
          objectId,
        });
        const filenames = fs.readdirSync(`./final_res/${objectId}`);
        const editResponse = await client.EditContentObject({
          libraryId,
          objectId,
        });
        const writeToken = editResponse.write_token;
        console.log(writeToken);
        // for (let filename of filenames) {
        //   await uploadFile(client, libraryId, objectId, filename, writeToken);
        // }
        // await client.FinalizeContentObject({
        //   libraryId,
        //   objectId,
        //   writeToken,
        //   commitMessage: "merge sony tags to shot_tags",
        // });
      }
    } catch (err) {
      console.log(err);
    }
  })
  .catch((err) => {
    console.log(err);
  });

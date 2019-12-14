const path = require("path");
const ScatterJS = require("@scatterjs/core").default;
const ScatterEOS = require("@scatterjs/eosjs2").default;
const { JsonRpc, Api } = require("eosjs");
const { TextEncoder, TextDecoder } = require(`util`);
const dotenv = require("dotenv");

require("isomorphic-fetch");

ScatterJS.plugins(new ScatterEOS());

const stages = {
  "local": {
    env: "local",
    name: "LOCAL",
  },
  "eos.test": {
    env: "eos.test",
    name: "TEST",
  },
  "telos.test": {
    env: "telos.test",
    name: "TEST",
  },
  // "prod": {
  //   env: "prod",
  //   contractStage: "prod",
  //   name: "PROD",
  // }
}

const stage = stages[process.argv[2]];
if (!stage) {
  console.log("Invalid stage! Set one of ", Object.keys(stages));
  process.exit(1);
}

const targetAccount = process.argv[3];
if (!targetAccount) {
  console.log("Target account not specified", Object.keys(stages));
  process.exit(1);
}

const moderatorFlag = parseInt(stages[process.argv[4]] || "31", 10);
if (moderatorFlag > 31 || moderatorFlag < 0) {
  console.log("Invalid mogerator flag! Flug must be between [0..31]");
  process.exit(1);
}


const mainAccountName = "peeranhamain";

const stageEnv = dotenv.config({ path: path.resolve(__dirname, `.env.${stage.env}`) }).parsed;
const baseEnv = dotenv.config({ path: path.resolve(__dirname, ".env.common") }).parsed;
const env = { ...stageEnv, ...baseEnv };

async function grantModerator() {
  const network = ScatterJS.Network.fromJson({
    blockchain: env.BLOCKCHAIN_NAME,
    protocol: env.EOS_PROTOCOL,
    host: env.EOS_HOST,
    port: env.EOS_PORT,
    chainId: env.EOS_CHAIN_ID
  });
  const rpc = new JsonRpc(network.fullhost());


  const api = new Api({
    rpc,
    textDecoder: new TextDecoder(),
    textEncoder: new TextEncoder(),
  });
  if (!await ScatterJS.connect(env.SCATTER_APP_NAME, { network })) {
    throw "Scatter not installed";
  }
  const eos = ScatterJS.eos(network, Api, api);
  await ScatterJS.logout();
  await ScatterJS.login();
  const account = ScatterJS.account(env.BLOCKCHAIN_NAME);
  if (account.name != mainAccountName) {
    throw `Invalid account! Use ${mainAccountName}`;
  }
  await eos.transact(
    {
      actions: [
        /*
        {
        account: mainAccountName,
        name: 'setaccrten',
        authorization: [
          {
            actor: mainAccountName,
            permission: env.DEFAULT_EOS_PERMISSION
          }
        ],
        data: {
          "user": "yuliachorno2",
          "energy": "125",
          "rating": "2811",
        },
      }*/
        {
          account: mainAccountName,
          name: 'givemoderflg',
          authorization: [
            {
              actor: mainAccountName,
              permission: env.DEFAULT_EOS_PERMISSION
            }
          ],
          data: {
            "user": "dsasfdvcbvnb",
            "flags": "31"
          }
        }
      ],
    },
    {
      blocksBehind: 3,
      expireSeconds: 30
    }
  );
}

grantModerator().then(() => {
  console.log(`Successfully grant moderator flag to ${targetAccount} on ${stage.name} stage`);
  process.exit(0);
}).catch((err) => {
  console.log("Failed to deploy cause", err);
  process.exit(1);
})
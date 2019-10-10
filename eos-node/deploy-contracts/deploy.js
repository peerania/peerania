const fs = require("fs");
const path = require("path");
const ScatterJS = require("@scatterjs/core").default;
const ScatterEOS = require("@scatterjs/eosjs2").default;
const { JsonRpc, Api, Serialize } = require("eosjs");
const { TextEncoder, TextDecoder } = require(`util`);
const dotenv = require("dotenv");

require("isomorphic-fetch");

ScatterJS.plugins(new ScatterEOS());

const args = process.argv.slice(2);
const pathToFiles = args[0];
const envType = args[1];

const envPath = path.resolve(`.env.${envType}`);
const env = dotenv.config({ path: envPath }).parsed;

if (!env) {
  throw new Error(
    "You have to specify correct type of .env file by the 2d parameter (prod, test, local)"
  );
}

const network = ScatterJS.Network.fromJson({
  blockchain: env.BLOCKCHAIN_NAME,
  protocol: env.EOS_SCATTER_PROTOCOL,
  host: env.EOS_SCATTER_HOST,
  port: env.EOS_SCATTER_PORT,
  chainId: env.EOS_CHAIN_ID
});

const rpc = new JsonRpc(network.fullhost());

const wasm = fs
  .readFileSync(path.resolve(`${pathToFiles}.wasm`))
  .toString(`hex`);

let abi = JSON.parse(
  fs.readFileSync(path.resolve(`${pathToFiles}.abi`), `utf8`)
);

const api = new Api({
  rpc,
  textDecoder: new TextDecoder(),
  textEncoder: new TextEncoder()
});

const buffer = new Serialize.SerialBuffer({
  textEncoder: api.textEncoder,
  textDecoder: api.textDecoder
});

const abiDefinition = api.abiTypes.get(`abi_def`);

abi = abiDefinition.fields.reduce(
  (acc, { name: fieldName }) =>
    Object.assign(acc, { [fieldName]: acc[fieldName] || [] }),
  abi
);

abiDefinition.serialize(buffer, abi);

ScatterJS.connect(env.SCATTER_APP_NAME, { network })
  .then(async connected => {
    if (!connected) {
      throw new Error("Scatter is not installed");
    }

    const eos = ScatterJS.eos(network, Api, { rpc });

    await ScatterJS.logout();

    const id = await ScatterJS.login();

    if (!id) {
      throw new Error("No identity");
    }

    const account = ScatterJS.account(env.BLOCKCHAIN_NAME);

    await eos.transact(
      {
        actions: [
          {
            account: "eosio",
            name: "setcode",
            authorization: [
              {
                actor: account.name,
                permission: env.DEFAULT_EOS_PERMISSION
              }
            ],
            data: {
              account: account.name,
              vmtype: 0,
              vmversion: 0,
              code: wasm
            }
          },
          {
            account: "eosio",
            name: "setabi",
            authorization: [
              {
                actor: account.name,
                permission: env.DEFAULT_EOS_PERMISSION
              }
            ],
            data: {
              account: account.name,
              abi: Buffer.from(buffer.asUint8Array()).toString(`hex`)
            }
          }
        ]
      },
      {
        blocksBehind: 3,
        expireSeconds: 30
      }
    );

    process.exit();
  })
  .catch(err => {
    console.log(err);
    process.exit(1);
  });

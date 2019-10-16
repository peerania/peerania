const fs = require("fs");
const path = require("path");
const ScatterJS = require("@scatterjs/core").default;
const ScatterEOS = require("@scatterjs/eosjs2").default;
const { JsonRpc, Api, Serialize } = require("eosjs");
const { TextEncoder, TextDecoder } = require(`util`);
const dotenv = require("dotenv");

const { spawn } = require('child_process');

require("isomorphic-fetch");

ScatterJS.plugins(new ScatterEOS());

const stages = {
  "local": {
    env: "local",
    contractStage: "debug",
    name: "LOCAL",
  },
  "test": {
    env: "test",
    contractStage: "test",
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

const accounts = {
  "peeranhamain": {
    pathToFiles: path.resolve(__dirname, "../../src/contracts/peeranha.main"),
    wasm: "peeranha.main.wasm",
    abi: "peeranha.main.abi",
    name: "MAIN",
    additionalActions: [
      {
        account: "peeranhamain",
        name: 'init',
        authorization: [
          {
            actor: "peeranhamain",
            permission: "active"
          }
        ],
        data: {},
      }
    ]
  },
  "peeranhatken": {
    pathToFiles: path.resolve(__dirname, "../../src/contracts/peeranha.token"),
    wasm: "peeranha.token.wasm",
    abi: "peeranha.token.abi",
    name: "TOKEN",
    additionalActions: []
  }
};

const stageEnv = dotenv.config({ path: path.resolve(__dirname, `.env.${stage.env}`) }).parsed;
const baseEnv = dotenv.config({ path: path.resolve(__dirname, ".env.common") }).parsed;
const env = { ...stageEnv, ...baseEnv };

function compile(stage) {
  const child = spawn("docker-compose", [`run`, `-w`, `/peeranha`, `eosio`, `./compile`, `--stage=${stage.contractStage}`], { cwd: path.resolve(__dirname, "../../..") });
  child.stdout.on('data', (chunk) => {
    console.log(chunk.toString());
  });

  child.stderr.on('data', (chunk) => {
    console.log(chunk.toString());
  });
  return new Promise((resolve, reject) => {
    child.on('close', (code) => {
      if (code == 0)
        resolve();
      else
        reject("Compilation failed");
    });
  });
}

async function loadContract(api, contract) {
  const wasm = fs
    .readFileSync(path.join(contract.pathToFiles, contract.wasm))
    .toString(`hex`);

  const buffer = new Serialize.SerialBuffer({
    textEncoder: api.textEncoder,
    textDecoder: api.textDecoder,
  });
  let abi = JSON.parse(
    fs.readFileSync(path.join(contract.pathToFiles, contract.abi), 'utf8')
  );
  const abiDefinition = api.abiTypes.get(`abi_def`);
  abi = abiDefinition.fields.reduce(
    (acc, { name: fieldName }) =>
      Object.assign(acc, { [fieldName]: acc[fieldName] || [] }),
    abi
  );
  abiDefinition.serialize(buffer, abi);

  return {
    abi: Buffer.from(buffer.asUint8Array()).toString(`hex`),
    wasm
  };
}

async function deploy(stage, env) {
  await compile(stage);
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
  const contract = accounts[account.name];
  if (!contract) {
    throw "Invalid account";
  }
  console.log(`Deplying ${contract.name} on stage ${stage.name}(${stage.contractStage} contract)`);
  const { wasm, abi } = await loadContract(api, contract);

  const deployActions = [
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
        abi,
      }
    },
  ]
  await eos.transact(
    {
      actions: deployActions,
    },
    {
      blocksBehind: 3,
      expireSeconds: 90
    }
  );
  if (contract.additionalActions.length != 0)
    await eos.transact({
      actions: contract.additionalActions,
    },
    {
      blocksBehind: 3,
      expireSeconds: 30
    });
}

deploy(stage, env).then(() => {
  console.log(`Successfully deployed on stage ${stage.name}`);
  process.exit(0);
}).catch((err) => {
  console.log("Failed to deploy cause", err);
  process.exit(1);
})
const ScatterJS = require("@scatterjs/core").default;
const ScatterEOS = require("@scatterjs/eosjs2").default;
const { JsonRpc, Api } = require("eosjs");
const { TextEncoder, TextDecoder } = require(`util`);
require("isomorphic-fetch");

ScatterJS.plugins(new ScatterEOS());

const payerAccountName = "peeranhaacct";

const accountCredentials = {
    eosAccountName: process.argv[2],
    publicActiveKey: process.argv[3],
    publicOwnerKey: process.argv[4],
}

console.log(accountCredentials);

const ramBytes = 4096;

const env = {
    BLOCKCHAIN_NAME: 'eos',
    DEFAULT_EOS_PERMISSION: 'active',
    SCATTER_APP_NAME: 'Peeranha',
    EOS_PROTOCOL: 'https',
    EOS_HOST: 'api.telosfoundation.io',
    EOS_PORT: 443,
    EOS_CHAIN_ID: '4667b205c6838ef70ff7988f6e8257e8be0e1284a2f59699054a018f743b1d11',
}

async function createAccount(accountCredentials,
    ramBytes,
    stakeQuantity) {
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
    if (account.name != payerAccountName) {
        throw `Invalid account! Use ${payerAccountName}`;
    }

    const transactActions = [
        {
            account: "eosio",
            name: "newaccount",
            authorization: [
                {
                    actor: payerAccountName,
                    permission: "active",
                },
            ],
            data: {
                creator: payerAccountName,
                name: accountCredentials.eosAccountName,
                owner: {
                    threshold: 1,
                    keys: [
                        {
                            key: accountCredentials.publicOwnerKey,
                            weight: 1,
                        },
                    ],
                    accounts: [],
                    waits: [],
                },
                active: {
                    threshold: 1,
                    keys: [
                        {
                            key: accountCredentials.publicActiveKey,
                            weight: 1,
                        },
                    ],
                    accounts: [],
                    waits: [],
                },
            },
        },
        {
            account: "eosio",
            name: "buyrambytes",
            authorization: [
                {
                    actor: payerAccountName,
                    permission: "active",
                },
            ],
            data: {
                payer: payerAccountName,
                receiver: accountCredentials.eosAccountName,
                bytes: ramBytes,
            },
        },
    ];
    if (stakeQuantity) {
        transactActions.push(
            {
                account: "eosio",
                name: "delegatebw",
                authorization: [
                    {
                        actor: payerAccountName,
                        permission: "active",
                    },
                ],
                data: {
                    from: payerAccountName,
                    receiver: accountCredentials.eosAccountName,
                    stake_net_quantity: stakeQuantity.net,
                    stake_cpu_quantity: stakeQuantity.cpu,
                    transfer: false,
                },
            },
        );
    }
    const resp = await eos.transact(
        {
            actions: transactActions,
        },
        {
            blocksBehind: 3,
            expireSeconds: 30,
        });
    return resp;
    
}

createAccount(accountCredentials, ramBytes, null).then(() => {
    console.log(`Successfully create account ${accountCredentials.eosAccountName}`);
    process.exit(0);
}).catch((err) => {
    console.log("Failed create account", err);
    process.exit(1);
})
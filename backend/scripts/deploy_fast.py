from cgi import test
from brownie import accounts, chain
from scripts.helpers import *
from web3.auto import w3
from eth_account.messages import encode_defunct
from eth_abi.packed import encode_abi_packed
from eth_utils import keccak


is_testnet = network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
postthread, account = deploy_contracts(accounts, use_previous=False, publish=False, testnet=is_testnet)

# mint msa ids
tx = postthread.createMsaId(account.address)
msa_id = tx.return_value
print(msa_id, account.address, tx.events)
print("Msa_id match", postthread.getMsaId(account.address) == msa_id)

private_key = "0x416b8a7d9290502f5661da81f0cf43893e3d19cb9aea3c426cfb36e8186e9c09"
local = accounts.add(private_key=private_key)
hash = keccak(encode_abi_packed(['uint256'],[msa_id]))
message = encode_defunct(hexstr=hash.hex())
signed_message =  w3.eth.account.sign_message(message, private_key=private_key)

tx = postthread.isValidUser(msa_id, str(signed_message.signature.hex()), local.address)

tx = postthread.createSponsoredAccountWithDelegation(local.address, account.address, signed_message.signature.hex())
delegate_msa_id = tx.return_value
print("Msas", msa_id, delegate_msa_id)

# mint schemas
post_schema = "category STRING,title STRING,body STRING,url STRING,is_nsfw NUMERIC"
post_schemaId = postthread.registerSchema(post_schema).return_value
print("schemas match", postthread.getSchema(post_schemaId) == post_schema)

# mint message
payload = '{"category": "test", "title": "test", "body": "test", "url": "test", "is_nsfw": 0}'
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})
tx = postthread.addMessage(msa_id, delegate_msa_id, post_schemaId, payload, {"from": account})


tx = postthread.getMessages(post_schemaId, 0, {"from": account})
print(tx)
tx = postthread.getMessages(post_schemaId, 1, {"from": account})
print(tx)
tx = postthread.getMessages(post_schemaId, 2, {"from": account})
print(tx)
tx = postthread.getMessages(post_schemaId, 3, {"from": account})
print(tx)
tx = postthread.getMessages(post_schemaId, 4, {"from": account})
print(tx)
# print(tx.error())
# print(tx.return_value)

def main():
    pass

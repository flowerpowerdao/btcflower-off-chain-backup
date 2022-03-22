from turtle import back
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
import json
import time
import schedule
import sys

# params is an array, return value is encoded bytes
params = [{'type': Types.Nat, 'value': 10}]
data = encode(params)
# Identity and Client are dependencies of Agent
iden = Identity()  # creates a random keypair
client = Client()  # creates a client to talk to the IC
# creates an agent, combination of client and identity
agent = Agent(iden, client)


def main():
    backup(canister_id=sys.argv[1])
    schedule.every(interval=int(sys.argv[2])).minutes.do(backup, canister_id=sys.argv[1])

    while True:
        schedule.run_pending()
        time.sleep(1)

def backup(canister_id):
    print("backing up ...")
    print(f"backup completed at {time.ctime()}")
    # query the NFT canister
    # doesnt change after calling `shuffleAssets`
    tokens = agent.query_raw(
        canister_id, "getTokens", encode([]))[0]["value"]
    with open('tokens.json', 'w') as f:
        json.dump(tokens, f, ensure_ascii=False, indent=4)

    # changes after every transaction
    registry = agent.query_raw(
        canister_id, "getRegistry", encode([]))[0]["value"]
    with open('registry.json', 'w') as f:
        json.dump(registry, f, ensure_ascii=False, indent=4)
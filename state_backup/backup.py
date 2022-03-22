from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
import time
import schedule
import sys

# params is an array, return value is encoded bytes
# params = [{'type': Types.Nat, 'value': 10}]
# data = encode(params)

# Identity and Client are dependencies of Agent
iden = Identity()  # creates a random keypair
client = Client()  # creates a client to talk to the IC
# creates an agent, combination of client and identity
agent = Agent(iden, client)


def main():
    backup(canister_id=sys.argv[1])
    schedule.every(5).seconds.do(backup, canister_id=sys.argv[1])

    while True:
        schedule.run_pending()
        time.sleep(1)


def backup(canister_id):
    print(f"disburse completed at {time.ctime()}")
    # query the NFT canister
    # doesnt change after calling `shuffleAssets`
    result = agent.update_raw(
        canister_id, "disburse", encode([]))
        
    print(result) 

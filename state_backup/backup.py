from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
import time
import sched
import sys

# params is an array, return value is encoded bytes
# params = [{'type': Types.Nat, 'value': 10}]
# data = encode(params)

# Identity and Client are dependencies of Agent
iden = Identity()  # creates a random keypair
client = Client()  # creates a client to talk to the IC
# creates an agent, combination of client and identity
agent = Agent(iden, client)

s = sched.scheduler(time.time, time.sleep)


def backup(canister_id, interval):
    print(f"disburse completed at {time.ctime()}")
    # query the NFT canister
    # doesnt change after calling `shuffleAssets`
    try:
        result = agent.update_raw(
            canister_id, "disburse", encode([]))
        print(result)
    except TypeError:
        pass

    s.enter(int(interval), 1, backup, (canister_id, interval))


def main():
    s.enter(1, 1, backup, (sys.argv[1], sys.argv[2]))
    s.run()

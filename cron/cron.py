from ic.client import Client
import sys
import sched
import time
from ic.candid import encode
from ic.canister import Canister
from ic.agent import Agent
from ic.identity import Identity

# Identity and Client are dependencies of Agent
iden = Identity()  # creates a random keypair
client = Client()  # creates a client to talk to the IC
# creates an agent, combination of client and identity
agent = Agent(iden, client)

s = sched.scheduler(time.time, time.sleep)


def cron(canister_id, interval):
    try:
        print(f"disburse completed at {time.ctime()}")
        response = agent.query_raw(
            canister_id, '__get_candid_interface_tmp_hack', encode([]))
        canister_did = response[0]['value']  # type: ignore
        my_canister = Canister(
            agent=agent, canister_id=canister_id, candid=canister_did)
        # query the NFT canister
        # doesnt change after calling `shuffleAssets`
        my_canister.cronDisbursements()  # type: ignore
        my_canister.cronFailedSales()  # type: ignore
        my_canister.cronSalesSettlements()  # type: ignore
        my_canister.cronSettlements()  # type: ignore
    except Exception as e:
        print(e)

    s.enter(int(interval), 1, cron, (canister_id, interval))


def main():
    s.enter(1, 1, cron, (sys.argv[1], sys.argv[2]))
    s.run()

from brownie import web3, chain, interface, accounts, config, Timestamp
import time
import os


def main():
    kucoin_wallet = os.getenv("ARB_WALLET")
    accounts.add(config["wallets"]["from_key"])
    # Contracts init
    distributor = interface.TokenDistributor(
        "0x67a24CE4321aB3aF51c2D0a4801c3E111D88C9d9"
    )
    arb_token = interface.IERC20("0x912CE59144191C1204E64559FE8253a0e49E6548")
    # Block number read in loop
    cnt = 0
    state_machine_cntr = 0
    while state_machine_cntr != 3:
        try:
            if state_machine_cntr == 0:
                block_number = Timestamp[-1].getBlockNumber()
                start_block = distributor.claimPeriodStart()
                amount_to_claim = distributor.claimableTokens(accounts[0].address)
                print(
                    "Amount to claim: {} {} for address {}".format(
                        amount_to_claim, arb_token.symbol(), accounts[0]
                    )
                )
                state_machine_cntr = 1
            elif state_machine_cntr == 1:
                block_number = Timestamp[-1].getBlockNumber()
                if block_number >= start_block:
                    print(
                        "Block number ({}) exceeded start block ({})".format(
                            block_number, start_block
                        )
                    )
                    try:
                        claimed_amount = arb_token.balanceOf(accounts[0])
                        if claimed_amount == 0:
                            print("Trying to claim")
                            distributor.claim({"from": accounts[0]})
                            state_machine_cntr = 2
                        else:
                            state_machine_cntr = 2
                    except:
                        print("Something went wrong")
                        continue
                else:
                    cnt += 1
                    if cnt == 3:
                        print(
                            "Block number ({}) NOT exceeded start block ({})".format(
                                block_number, start_block
                            )
                        )
                    cnt %= 4
            elif state_machine_cntr == 2:
                claimed_amount = arb_token.balanceOf(accounts[0])
                if claimed_amount > 0:
                    try:
                        print(
                            "Trying to transfer {} {}".format(
                                int(claimed_amount / 10), arb_token.symbol()
                            )
                        )
                        arb_token.transfer(
                            kucoin_wallet,
                            int(claimed_amount / 10),
                            {"from": accounts[0]},
                        )
                        state_machine_cntr = 3
                    except:
                        print("Something went wrong")
                        continue
            time.sleep(2)
        except:
            time.sleep(1.5)
            print("Somethi")
            continue

from brownie import web3, chain, interface, accounts, config, Timestamp
import time
import os


def main():
    # Get environment variables
    kucoin_wallet = os.getenv("USDC_WALLET")
    accounts.add(config["wallets"]["from_key"])
    # Contracts init
    usdt_token = interface.IERC20("0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9")
    symbol = usdt_token.symbol()
    balance = usdt_token.balanceOf(accounts[0])
    amount_to_send = int(balance / 2)
    state_machine_cntr = 0
    start_block = 226884875
    while state_machine_cntr != 2:
        block_number = Timestamp[-1].getBlockNumber()
        if state_machine_cntr == 0:
            if block_number > start_block:
                print(
                    "Block number ({}) exceeded start block ({})".format(
                        block_number, start_block
                    )
                )
                state_machine_cntr = 1
            else:
                print(
                    "Block number ({}) NOT exceeded start block ({})".format(
                        block_number, start_block
                    )
                )
        if state_machine_cntr == 1:
            print(
                "Balance of address {} is {} {}".format(
                    accounts[0], web3.fromWei(balance, "mwei"), symbol
                )
            )
            try:
                print(
                    "Transfering {} {}".format(
                        web3.fromWei(amount_to_send, "mwei"), symbol
                    )
                )
                usdt_token.transfer(
                    kucoin_wallet, amount_to_send, {"from": accounts[0]}
                )
                state_machine_cntr = 2
            except:
                print("Something went wrong")
                continue
        time.sleep(1)

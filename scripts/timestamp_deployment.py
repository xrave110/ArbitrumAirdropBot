from brownie import Timestamp, chain, interface, accounts, config

timestamp_address = 0
timestamp = 0


def deploy_contract():
    accounts.add(config["wallets"]["from_key"])
    timestamp = Timestamp.deploy(
        {"from": accounts[0]},
    )
    print("Timestamp contract has been deployed at: {}".format(timestamp.address))
    timestamp_address = timestamp.address


def main():
    deploy_contract()

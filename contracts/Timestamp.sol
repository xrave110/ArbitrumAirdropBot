// SPDX-License-Identifier
pragma solidity ^0.8.0;

contract Timestamp {
    function getBlockNumber() external view returns (uint256) {
        return block.number;
    }
}

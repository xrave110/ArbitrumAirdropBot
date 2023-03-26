// SPDX-License-Identifier: MIT license
pragma solidity >0.8.0;

interface TokenDistributor {
    function claim() external;

    function claimableTokens(address user) external view returns (uint256);

    function claimPeriodStart() external view returns (uint256);

    function claimPeriodEnd() external view returns (uint256);
}

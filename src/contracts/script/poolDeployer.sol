pragma solidity ^0.8.0;

import {Script} from "../lib/forge-std/src/Script.sol";
import {token} from "../src/tokens.sol";
import {Pool} from "../src/pool.sol";
contract poolDeployer is Script {
    token tokenX;
    token tokenY;
    Pool pool;

    bool initializedTokens = false;
    bool initializedPool = false;

    uint256 deployerPrivateKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
    function run() external {
        if (!initializedTokens) {
            vm.startBroadcast(deployerPrivateKey);
            tokenX = new token();
            tokenX.initialize("X", "X", 8);
            tokenY = new token();
            tokenY.initialize("Y", "Y", 8);
            initializedTokens = true;

            vm.stopBroadcast();
        }

        if (!initializedPool && initializedTokens) {
            vm.startBroadcast(deployerPrivateKey);
            pool = new Pool();
            pool.setTokenPair(address(tokenX), address(tokenY));
            vm.stopBroadcast();
        }
    }
}

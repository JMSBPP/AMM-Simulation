pragma solidity ^0.8.0;

import {Script} from "../lib/forge-std/src/Script.sol";
import {MockERC20} from "../lib/forge-std/src/mocks/MockERC20.sol";

contract poolDeployer is Script {
    

    function mint()
    function run() external{
        vm.startBroadcast();
        MockERC20 tokenX = new MockERC20();
        tokenX.initialize("X", "X", 8);
        MockERC20 tokenY = new MockERC20();
        tokenX.initialize("Y", "Y", 8);
    }

}

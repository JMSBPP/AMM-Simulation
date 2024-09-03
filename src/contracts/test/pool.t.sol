pragma solidity ^0.8.0;

import {Test} from "../lib/forge-std/src/Test.sol";
import {Pool} from "../src/pool.sol";

contract TestPool is Test {
    Pool public pool;
    function setUp() public {
        pool = new Pool();
        pool.initialize(200, 100, 20);
    }

    function testInitialState() external {
        pool.getReserves();
    }
}

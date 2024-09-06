pragma solidity ^0.8.0;

import {Test} from "../lib/forge-std/src/Test.sol";
import {Pool} from "../src/pool.sol";

contract TestPool is Test {
    Pool public pool;
    function setUp() public {
        pool = new Pool();
    }

    function testInitialize() public {
        pool.initialize(400, 10, 20);
        assertEq(pool.reserveOffset(), 0);
    }

    function testAddLiquidity() public {
        pool.initialize(400, 10, 20);
        pool.addLiquidity(5, 20);
    }
}

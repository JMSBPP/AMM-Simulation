pragma solidity ^0.8.0;

import {MockERC20} from "../lib/forge-std/src/mocks/MockERC20.sol";

contract token is MockERC20 {
    function mint(address account, uint256 amount) public {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) public {
        _burn(account, amount);
    }
}

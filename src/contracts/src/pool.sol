pragma solidity ^0.8.0;

import {IERC20} from "../lib/forge-std/src/interfaces/IERC20.sol";

contract Pool {
    uint public reserveA;
    uint public reserveB;
    uint public rateChange;
    uint public maxReservesX;
    uint public maxReservesY;
    uint public priceX;
    uint public priceY;
    uint public liquidity;
    address public LPToken;

    bool initialized = false;

    modifier _initialized() {
        require(initialized == true, "POOL NOT INITIALIZED");
        _;
    }

    function initialize(
        uint _maxReserveX,
        uint initialReserveX,
        uint initialReserveY
    ) public {
        maxReservesX = _maxReserveX;
        reserveA = initialReserveX;
        reserveB = initialReserveY;
        rateChange = (maxReservesX - reserveA) / reserveB;
        maxReservesY = maxReservesX / rateChange;
        priceX = reserveA / reserveB;
        priceY = reserveB / reserveA;
        liquidity = (maxReservesX * maxReservesY) / 2;
        initialized = true;
    }

    function getReserves() public view _initialized returns (uint, uint) {
        return (reserveA, reserveB);
    }

    function _update() internal _initialized {
        rateChange = (maxReservesX - maxReservesY) / reserveB;
        maxReservesX = reserveA * rateChange * reserveB;
        maxReservesY = maxReservesX / rateChange;
        priceX = reserveA / reserveB;
        priceY = reserveB / reserveA;
        liquidity = (maxReservesX * maxReservesY) / 2;
    }
    function addLiquidity(
        uint amount0in,
        address tokenX,
        uint amount1in,
        address tokenY
    ) public _initialized {
        uint _reserve0A = reserveA;
        uint amount1inOptimal = (reserveB *
            (_reserve0A + amount0in) -
            reserveB *
            _reserve0A);
        require(amount1inOptimal >= amount1in, "NOT ENOUGH LIQUIDITY");
        IERC20(tokenY).transfer(msg.sender, amount1inOptimal - amount1in);
        uint mintable = amount0in / _reserve0A;
        // IERC20(LPToken).mint(msg.sender, mintable);
        reserveA += amount0in;
        reserveB += amount1in;
        _update();
    }
}

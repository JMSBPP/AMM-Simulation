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

    uint private constant FACTOR_SCALE = 1e8;

    enum state {
        INITIALIZED,
        NOT_INITIALIZED
    }

    state _state;
    bool initialized = false;

    event PoolInitialized(
        uint indexed _reserveX,
        uint indexed _reserveY,
        uint indexed _maxReserveX
    );

    modifier _initialized() {
        require(_state == state.INITIALIZED, "POOL NOT INITIALIZED");
        _;
    }

    constructor() {
        _state = state.NOT_INITIALIZED;
    }

    function initialize(
        uint _maxReserveX,
        uint initialReserveX,
        uint initialReserveY
    ) public {
        require(
            initialReserveX > 0 && initialReserveY > 0,
            "INITIAL SUPPLY MUST BE POSITIVE"
        );
        require(
            initialReserveX <= _maxReserveX && initialReserveY <= _maxReserveX,
            "MAX RESERVE MUST BE GRATER THAN INITIAL SUPPLY"
        );
        maxReservesX = _maxReserveX;
        reserveA = initialReserveX;
        reserveB = initialReserveY;
        _update();
        _state = state.INITIALIZED;
        emit PoolInitialized(reserveA, reserveB, maxReservesX);
    }

    function _update() internal {
        if (_state == state.INITIALIZED) {
            maxReservesX = reserveA + rateChange * reserveB;
        }
        rateChange = ((maxReservesX - reserveA) * FACTOR_SCALE) / reserveB;
        maxReservesY = (maxReservesX * FACTOR_SCALE ** 2) / rateChange;
        // priceX = reserveA / reserveB;
        // priceY = reserveB / reserveA;
        // liquidity = (maxReservesX * maxReservesY) / 2;
    }

    function calculateInvariant(
        uint maxA_,
        uint rateChange_,
        uint reserveB_
    ) internal pure returns (uint) {
        uint _maxA = maxA_ * FACTOR_SCALE ** 3;
        uint _reserveB = reserveB_ * FACTOR_SCALE ** 2;
        uint expectedReserve = (_maxA - rateChange_ * _reserveB) /
            FACTOR_SCALE ** 3;
        return expectedReserve;
    }

    function reserveOffset() public _initialized returns (uint) {
        calculateInvariant(maxReservesX, rateChange, reserveB);
        uint offset = calculateInvariant(maxReservesX, rateChange, reserveB) -
            reserveA;
        return offset;
    }

    // function addLiquidity(
    //     uint amount0in,
    //     address tokenX,
    //     uint amount1in,
    //     address tokenY
    // ) public _initialized {
    //     uint _reserve0A = reserveA;
    //     uint amount1inOptimal = (reserveB *
    //         (_reserve0A + amount0in) -
    //         reserveB *
    //         _reserve0A);
    //     require(amount1inOptimal >= amount1in, "NOT ENOUGH LIQUIDITY");
    //     IERC20(tokenY).transfer(msg.sender, amount1inOptimal - amount1in);
    //     uint mintable = amount0in / _reserve0A;
    //     // IERC20(LPToken).mint(msg.sender, mintable);
    //     reserveA += amount0in;
    //     reserveB += amount1in;
    //     _update();
    // }
}

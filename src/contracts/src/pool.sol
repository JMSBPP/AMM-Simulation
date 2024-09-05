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
    address tokenX;
    address tokenY;

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

    error InvalidInputAmount();

    modifier _initialized() {
        require(_state == state.INITIALIZED, "POOL NOT INITIALIZED");
        _;
    }

    modifier upperBoundTokenXLiquidity(uint a) {
        require(upperBoundTokenX(a) >= 0, "TOKEN X INPUT AMOUNT NOT VALID");
        _;
    }

    modifier upperBoundTokenYLiquidity(uint b) {
        require(b <= maxReservesY - reserveB, "TOKEN Y INPUT AMOUNT NOT VALID");
        _;
    }

    constructor(address _tokenX, address _tokenY) {
        tokenX = _tokenX;
        tokenY = _tokenY;
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
        IERC20(tokenX).transfer(address(this), initialReserveX);
        IERC20(tokenY).transfer(address(this), initialReserveY);
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

    function reserveOffset() public view _initialized returns (uint) {
        calculateInvariant(maxReservesX, rateChange, reserveB);
        uint offset = calculateInvariant(maxReservesX, rateChange, reserveB) -
            reserveA;
        return offset;
    }

    function upperBoundTokenX(uint a) public view returns (int) {
        //rateChange = ((maxReservesX - reserveA) * FACTOR_SCALE) / reserveB
        uint comp = (rateChange * reserveB) / FACTOR_SCALE;
        return int(comp - a);
    }

    function acceptableTokenYamount(
        uint _reserveB,
        uint _reserveA,
        uint amountA
    ) private pure returns (uint) {
        uint acceptableB = ((_reserveB * amountA) * FACTOR_SCALE) / _reserveA;
        return acceptableB;
    }

    function addLiquidity(
        uint amountA,
        uint amountB
    )
        public
        _initialized
        upperBoundTokenXLiquidity(amountA)
        upperBoundTokenYLiquidity(amountB)
    {
        uint optimalB = acceptableTokenYamount(reserveB, reserveA, amountA);
        if (optimalB >= amountB) {
            IERC20(tokenY).approve(address(this), optimalB - amountB);
            IERC20(tokenY).transferFrom(
                address(this),
                msg.sender,
                optimalB - amountB
            );
        }
        if (optimalB < amountB) {
            revert InvalidInputAmount();
        }
    }
}

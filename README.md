# AMM-Simulation

## Abstract
UniswapV2 defines a constant product formula (CPF) analogous to the indiference curve defined by the Cobb-Douglas utility function.\\

The following is a protocol implementation of an automated market maker (AMM) that follows a perfect substitute indifference curve model and studies its underlying behavior.\\

The functional relationship between the reserves of a toekn $X$ with respect to $Y$ is descrubed as:
\ \ $$A(B) = max(A) - \frac{dA}{dB}B$$


## Traders

Traders are essentially only allowed to swap between
tokens within a pool.\\

Each swap results in a endogoneous change to the liquidity function, meaning to say that the state transition only affects the prices between tokens.

## LP Providers

LP providers perform only two kind of operations that result in a transition state\\
1) **Add liquidity**
2) **Remove liquidity**.\\
It turns out that this operations result in an exogeneous move on the liquidty function but prices must remain the same, mathematically.\\

$$\frac{A}{B}=\frac{A+a}{B+b} \Rightarrow B(A+a)=A(B+b)$$



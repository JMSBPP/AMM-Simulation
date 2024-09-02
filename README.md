# AMM-Simulation

## Abstract
UniswapV2 defines a constant product formula (CPF) analogous to the indifference curve defined by the Cobb-Douglas utility function. The following is a protocol implementation of an automated market maker (AMM) that follows a perfect substitute indifference curve model and studies its underlying behavior.

The functional relationship between the reserves of a toekn $X$ with respect to $Y$ is descrubed as:
$$A(B) = max(A) - \frac{dA}{dB}B$$
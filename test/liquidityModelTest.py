import unittest as ut
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))

from liquidityModel import LiquidityModel


class LiquidityModelTest(ut.TestCase):
    def setUp(self):
        # Initialize the LiquidityModel with sample values
        self.liquidity_model = LiquidityModel(200, 100, 20)
    
    def testLiquidityRelation(self):
        # Add liquidity
        self.liquidity_model.addLiquidity(50)
        
        # Retrieve values from the model's summary
        reserveX = self.liquidity_model.summary["reserve X"]
        maxReserveX = self.liquidity_model.summary["maxReservestokenX"]
        rateChange = self.liquidity_model.summary['rateChange']
        reserveY = self.liquidity_model.summary["reserve Y"]
        
        # Calculate the expected reserve X
        expectedReserveX = maxReserveX - rateChange * reserveY
        
        # Assert that the actual reserve X is close to the expected value
        self.assertAlmostEqual(reserveX, expectedReserveX)

if __name__ == '__main__':
    ut.main()

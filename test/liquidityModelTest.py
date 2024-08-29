import unittest as ut
from ..src import liquidityModel



class LiquidityModelTest(ut.TestCase):
    def setUp(self):
        self.liquidity_model = liquidityModel.LiquidityModel(200,100,20)
    
    def testLiquidityRelation(self):
        self.liquidity_model.addLiquidity(50)
        reserveX = self.liquidity_model.summary["reserve X"]
        maxReserveX = self.liquidity_model.summary["maxReservestokenX"]
        rateChange  = self.liquidity_model.summary['rateChange']
        reserveY = self.liquidity_model.summary["reserve Y"]
        expectedReserveX = maxReserveX - rateChange*reserveY
        self.assertAlmostEqual(reserveX, expectedReserveX)


if __name__ == '__main__':
    ut.main()
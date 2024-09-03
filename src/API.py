from actors import Providers

class LiquidityModelDeployer:
    def __init__(self):
        self.liquidityPool = None
    def initiateLiquidityPool(self, maxReservestokenA, initialReservestokenA, initialReservestokenB):
        self.liquidityPool = LiquidityModel(maxReservestokenA, initialReservestokenA, initialReservestokenB)

class API:

    def __init__(self, id):
        self.providers = Providers(id)
        self.liquidityPool = LiquidityModelDeployer()
    def initiatePool(self, maxReservestokenA, initialReservestokenA, initialReservestokenB):
        self.liquidityPool.initiateLiquidityPool(maxReservestokenA, initialReservestokenA, initialReservestokenB)

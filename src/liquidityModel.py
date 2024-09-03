import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random



class LiquidityModel:

    def __init__(self, maxReservestokenA, initialReservestokenA, initialReservestokenB):
        assert maxReservestokenA >= initialReservestokenA, "MAX RESERVES MUST BE GRATER THAN INITIAL RESERVES"
        assert initialReservestokenB > 0 and initialReservestokenA > 0 , "INITIAL RESERVES MUST BE POSITIVE"
        self.maxReservestokenA = maxReservestokenA
        self.reservestokenB = initialReservestokenB
        self.reservestokenA = initialReservestokenA
        self.rateChangeAB = (self.maxReservestokenA - self.reservestokenA)/self.reservestokenB
        self.maxReservestokenB = self.maxReservestokenA/self.rateChangeAB
        self.priceX= self.reservestokenA/self.reservestokenB
        self.priceY= self.reservestokenB/self.reservestokenA
        self.liquidity = self.maxReservestokenA*self.maxReservestokenB/2
        self.summary = {"reserve X": [],
                        "reserve Y": [],
                        "rateChange": [],
                        "Price X": [],
                        "Price Y": [],
                        "liquidity": [],
                        "maxReservestokenX": [],
                        "maxReservestokenY": []}
        self.updateSummary()


    def updateSummary(self):
        #Se actualiza la tasa de cambio de reservas dA/dB
        self.rateChangeAB = (self.maxReservestokenA - self.reservestokenA)/(self.reservestokenB)
        #Se actualizan les reservas maximas max(A) = A(B=0)
        self.maxReservestokenA = self.reservestokenA + self.rateChangeAB*self.reservestokenB
        #Se actualizan las reservas maximas max(B) = A(max(B))=0
        self.maxReservestokenB = self.maxReservestokenA/self.rateChangeAB
        self.priceX = self.reservestokenA/self.reservestokenB
        self.priceY = self.reservestokenB/self.reservestokenA
        self.liquidity = self.maxReservestokenA*self.maxReservestokenB/2

        self.summary["reserve X"].append(self.reservestokenA)
        self.summary["reserve Y"].append(self.reservestokenB)
        self.summary["rateChange"].append(self.rateChangeAB)
        self.summary["Price X"].append(self.priceX)
        self.summary["Price Y"].append(self.priceY)
        self.summary["liquidity"].append(self.liquidity)
        self.summary["maxReservestokenX"].append(self.maxReservestokenA)
        self.summary["maxReservestokenY"].append(self.maxReservestokenB)


    def addLiquidity(self, amountTokenA):
        '''
        Allows to add liquidity exclusively from one token calculating the amount of thken B to provide
        '''

        assert amountTokenA > 0, "AMOUNT MUST BE POSITIVE"
        assert amountTokenA + self.reservestokenA < self.maxReservestokenA, "AMOUNT MUST BE LESS THAN MAX RESERVES"
        
        reserveA0 = self.reservestokenA
        # Se calcula la cantidad de b que toca depositar que dejen invariante el precio b
        amountTokenB = (self.reservestokenB*(reserveA0 + amountTokenA) - self.reservestokenB*reserveA0)/reserveA0
        #Se actualizan las reservas actuales A
        self.reservestokenA += amountTokenA
        #Se actualizan las reservas actuales B
        self.reservestokenB += amountTokenB
        self.updateSummary()
        # assert self.reservestokenA == self.maxReservestokenA -self.rateChangeAB*self.reservestokenB

class Providers:

    def __init__(self, id):
        self.providers = []
        self.id = id

    def addProvider(self, provider):
        provider.assignId()
        self.providers.append(provider)
class Provider:

    def __init__(self, providersGroupID):
        self.providersGroup = Providers(providersGroupID) 
        self.id = 0
        self.LPbalance = 0
        self.TokenXbalance = 0
        self.TokenYbalance = 0
    def assignId(self):
        self.providers.id = self.providers.id + 1
    def groupId(self):
        return self.providersGroup.id
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


class Simulation(LiquidityModel):
    def __init__(self, maxReservestokenA, initialReservestokenA, initialReservestokenB):
        super().__init__(maxReservestokenA, initialReservestokenA, initialReservestokenB)
        self.data = pd.DataFrame()

    def simulateAddLiquidity(self, steps):
        for _ in range(steps):
            amount = random.uniform(0.01, 0.99)
            self.addLiquidity(amount)
            # Update DataFrame with current summary
            temp_df = pd.DataFrame(self.summary)
            self.data = pd.concat([self.data, temp_df], ignore_index=True)
            self.data['Model'] = self.data['maxReservestokenY'] - self.data['rateChange']*self.data['reserve Y']
        return self.data

    def rateChangeEvolution(self):
        
        fig, ax = plt.subplots(nrows=2,ncols=3, figsize=(10,10))
        ax[0,0].plot(self.data.index, self.data['rateChange'])
        ax[0,0].set_title('Rate Change Evolution')
        ax[0,0].set_xlabel('Time')
        ax[0,0].set_ylabel('dA/dB')
        
        ax[0,1].plot(self.data.index, self.data['reserve X'])
        ax[0,1].set_title('reserve X Evolution')
        ax[0,1].set_xlabel('Time')
        ax[0,1].set_ylabel('reserve X')

        ax[0,2].plot(self.data['Model'], self.data['reserve X'])
        ax[0,2].set_title('Model vs reserve X')
        ax[0,2].set_xlabel('Model')
        ax[0,2].set_ylabel('reserve X')

        
        ax[1,0].plot(self.data.index, self.data['reserve Y'])
        ax[1,0].set_title('reserve Y Evolution')
        ax[1,0].set_xlabel('Time')
        ax[1,0].set_ylabel('reserve Y')
        
        ax[1,1].plot(self.data.index, self.data['maxReservestokenY'])
        ax[1,1].set_title('Max Reserve Y Evolution')
        ax[1,1].set_xlabel('Time')
        ax[1,1].set_ylabel('Max Reserve Y')

        ax[1,2].plot(self.data.index, self.data['liquidity'])   
        ax[1,2].set_title('liquidty Evolution')
        ax[1,2].set_xlabel('Time')
        ax[1,2].set_ylabel('liquidity')

        
        
        
        
        plt.savefig('rateChangeEvolution.png', format='png')



if __name__ == "__main__":
   s = Simulation(1000, 100, 100)
   s.simulateAddLiquidity(1000)
   s.rateChangeEvolution()

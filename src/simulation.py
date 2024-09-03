import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from liquidityModel import  LiquidityModel

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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random



class LiquidityModel:

    def __init__(self, maxReservestokenA, initialReservestokenA, initialReservestokenB):
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
        #Se actualizan las reservas maximas max(A) = A(B=0)
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

        
        reserveA0 = self.reservestokenA
        # Se calcula la cantidad de b que toca depositar que dejen invariante el precio b
        amountTokenB = (self.reservestokenB*(reserveA0 + amountTokenA) - self.reservestokenB*reserveA0)/reserveA0
        #Se actualizan las reservas actuales A
        self.reservestokenA += amountTokenA
        #Se actualizan las reservas actuales B
        self.reservestokenB += amountTokenB
        self.updateSummary()
        assert self.reservestokenA == self.maxReservestokenA -self.rateChangeAB*self.reservestokenB

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


if __name__ == "__main__":
    l = LiquidityModel(200, 100, 20)
    print("Pool before adding liquidity",l.summary)
    l.addLiquidity(50)
    print("Pool after 50 token A liquidity",l.summary)
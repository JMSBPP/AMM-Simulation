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
        self.expectedReserveX = self.maxReservestokenA - self.rateChangeAB*self.reservestokenB
        self.summary = {"reserve X": [],
                        "expected reserve X": [],
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

        self.expectedReserveX = self.maxReservestokenA - self.rateChangeAB*self.reservestokenB

        self.summary["reserve X"].append(self.reservestokenA)
        self.summary["reserve Y"].append(self.reservestokenB)
        self.summary["rateChange"].append(self.rateChangeAB)
        self.summary["Price X"].append(self.priceX)
        self.summary["Price Y"].append(self.priceY)
        self.summary["liquidity"].append(self.liquidity)
        self.summary["maxReservestokenX"].append(self.maxReservestokenA)
        self.summary["maxReservestokenY"].append(self.maxReservestokenB)
        self.summary["expected reserve X"].append(self.expectedReserveX)


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






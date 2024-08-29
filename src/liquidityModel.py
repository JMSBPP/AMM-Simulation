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
        self.summary = {"reserve X": self.reservestokenA,
                        "reserve Y": self.reservestokenB,
                        "rateChangeAB": self.rateChangeAB,
                        "maxReservestokenA": self.maxReservestokenA}


    def updateSummary(self):
        self.summary = {"reserve X": self.reservestokenA,
                        "reserve Y": self.reservestokenB,
                        "rateChangeAB": self.rateChangeAB,
                        "maxReservestokenA": self.maxReservestokenA}


    def addLiquidity(self, amountTokenA):
        reservesA0 = self.reservestokenA
        self.reservestokenA += amountTokenA
        reservesB0 = self.reservestokenB
        amountTokenB = (amountTokenA)/(self.maxReservestokenA-self.rateChangeAB)
        self.reservestokenB += amountTokenB
        self.rateChangeAB = (self.maxReservestokenA - self.reservestokenA)/(self.reservestokenB)
        self.updateSummary()

        assert self.reservestokenA == self.maxReservestokenA -self.rateChangeAB*self.reservestokenB



if __name__ == "__main__":
    l = LiquidityModel(200, 100, 20)
    print("Initial Summary:", l.summary)
    l.addLiquidity(50)
    print("After adding 100 token A:", l.summary)
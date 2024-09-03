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

#Movimientos
class Movement:
    def __init__(self,name,velLineal,velAngular,reward,enabled):
        self.name = name
        self.vel_linear = velLineal
        self.vel_angular = velAngular
        self.reward = reward
        self.enabled = enabled
        

    def __str__(self):
        print(str(self.name) + ' velocidad lineal: ' + str(self.vel_linear) + ' velocidad angular: ' +
         str(self.vel_angular) + ' recompensa: ' + str(self.reward) + ' habilitada: ' + str(self.enabled))

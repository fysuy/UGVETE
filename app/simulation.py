#Clase simulacion
import configparser
import movements as movs

#Clase
class Simulacion:
    def __init__(self,file):
        config = configparser.ConfigParser()
        config.read(file)       
        #Cargas iniciales datos generales
        self.algoritm = config['General']['Algoritm']
        self.episodes = config['General']['Episodes']
        self.timesteps = config['General']['TimeSteps']
        foward = movs.Movement('Foward',config['Foward']['VelLineal'],config['Foward']['VelAngular'],config['Foward']['Reward'],config['Foward']['Enabled'])
        left = movs.Movement('Left',config['Left']['VelLineal'],config['Left']['VelAngular'],config['Left']['Reward'],config['Left']['Enabled'])
        right = movs.Movement('Right',config['Right']['VelLineal'],config['Right']['VelAngular'],config['Right']['Reward'],config['Right']['Enabled'])
        turnleft = movs.Movement('TurnLeft',config['TurnLeft']['VelLineal'],config['TurnLeft']['VelAngular'],config['TurnLeft']['Reward'],config['TurnLeft']['Enabled'])
        turnright = movs.Movement('TurnRight',config['TurnRight']['VelLineal'],config['TurnRight']['VelAngular'],config['TurnRight']['Reward'],config['TurnRight']['Enabled'])
        stop = movs.Movement('Stop',config['Stop']['VelLineal'],config['Stop']['VelAngular'],config['Stop']['Reward'],config['Stop']['Enabled'])
        self.movements = {"Foward": foward, "Left": left, "Right": right, "TurnLeft": turnleft,"TurnRight": turnright,"Stop": stop}
    
def save_simulation(algoritm,episodes,timesteps,foward,left,right,turnleft,turnright,stop):
    config = configparser.ConfigParser()
    
    config['General'] = {'Algoritm': algoritm,
                        'Episodes': episodes,
                        'TimeSteps': timesteps}

    config['Foward'] = {'VelLineal': foward.vel_linear,
                        'VelAngular': foward.vel_angular,
                        'Reward': foward.reward,
                        'Enabled': foward.enabled}

    config['Left'] = {'VelLineal': left.vel_linear,
                        'VelAngular': left.vel_angular,
                        'Reward': left.reward,
                        'Enabled': left.enabled}

    config['Right'] = {'VelLineal': right.vel_linear,
                        'VelAngular': right.vel_angular,
                        'Reward': right.reward,
                        'Enabled': right.enabled}

    config['TurnLeft'] = {'VelLineal': '0.00',
                        'VelAngular': turnleft.vel_angular,
                        'Reward': turnleft.reward,
                        'Enabled': turnleft.enabled}

    config['TurnRight'] = {'VelLineal': '0.00',
                        'VelAngular': turnright.vel_angular,
                        'Reward': turnright.reward,
                        'Enabled': turnright.enabled}

    config['Stop'] = {'VelLineal': '0.00',
                        'VelAngular': '0.00',
                        'Reward': stop.reward,
                        'Enabled': stop.enabled}

    with open('simulation.ini', 'w') as configfile:
        config.write(configfile)

def load_simulation():
    simulation = Simulacion('simulation.ini')   
    return simulation

def get_enabled_moves(simulation):  
    movements = simulation.movements
    foward = movements["Foward"]
    left = movements["Left"]
    right = movements["Right"]
    turnleft = movements["TurnLeft"]
    turnright = movements["TurnRight"]
    stop = movements["Stop"]
    enabled_moves = []    
    
    if foward.enabled == 'True':
        enabled_moves.append(foward)        
    
    if left.enabled == 'True':         
        enabled_moves.append(left)        
    
    if right.enabled == 'True':         
        enabled_moves.append(right)
    
    if turnleft.enabled == 'True':         
        enabled_moves.append(turnleft)
    
    if turnright.enabled == 'True':         
        enabled_moves.append(turnright)
    
    if stop.enabled == 'True':         
        enabled_moves.append(stop)
    
    return enabled_moves

def get_simulation_properties(simulation):    
    episodes = simulation.episodes
    timesteps = simulation.timesteps
    return episodes,timesteps

def len_enabled_moves(enabled_moves):
    return len(enabled_moves)

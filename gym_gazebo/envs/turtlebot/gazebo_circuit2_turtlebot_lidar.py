import gym
import rospy
import roslaunch
import time
import numpy as np
import simulation as sim


from gym import utils, spaces
from gym_gazebo.envs import gazebo_env
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

from sensor_msgs.msg import LaserScan

from gym.utils import seeding

class GazeboCircuit2TurtlebotLidarEnv(gazebo_env.GazeboEnv):

    def __init__(self):
        # Launch the simulation with the given launchfile name
        gazebo_env.GazeboEnv.__init__(self, "GazeboCircuit2TurtlebotLidar_v0.launch")
        self.vel_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=5)
        self.unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
        self.pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        
        self.simulation = sim.load_simulation()
        #aux_total_episodes, aux_time_steps = sim.get_simulation_properties(simulation)  
        self.moves = sim.get_enabled_moves(self.simulation)
        #self.action_space = spaces.Discrete(3) #F,L,R
        print("Largo movs: "+ str(sim.len_enabled_moves(self.moves)))
        self.action_space = spaces.Discrete(sim.len_enabled_moves(self.moves))
        self.reward_range = (-np.inf, np.inf)

        self._seed()

    def discretize_observation(self,data,new_ranges):
        discretized_ranges = []
        min_range = 0.2
        done = False
        mod = len(data.ranges)/new_ranges
        for i, item in enumerate(data.ranges):
            if (i%mod==0):
                if data.ranges[i] == float ('Inf') or np.isinf(data.ranges[i]):
                    discretized_ranges.append(6)
                elif np.isnan(data.ranges[i]):
                    discretized_ranges.append(0)
                else:
                    discretized_ranges.append(int(data.ranges[i]))
            if (min_range > data.ranges[i] > 0):
                done = True
        return discretized_ranges,done

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            self.unpause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/unpause_physics service call failed")
        """
        moves = sim.get_enabled_moves()
        for move in moves:
            if move.name == 'Foward':               
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'Left':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'Right':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'Right':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'TurnLeft':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'TurnRight':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            elif move.name == 'Stop':
                vel_cmd = Twist()
                vel_cmd.linear.x = move.vel_linear
                vel_cmd.angular.z = move.vel_angular
                self.vel_pub.publish(vel_cmd)
            """
        
        """
        if action == 0: #FORWARD
            pos = 0          
        elif action == 1: #LEFT
            pos = 1         
        elif action == 2: #RIGHT
            pos = 2
        elif action == 3: #TURN_LEFT
            pos = 3
        elif action == 4: #TURN_RIGHT
            pos = 4
        elif action == 5: #STOP
            pos = 5
        """
        if action >= 0 and action <= 5:
            vel_cmd = Twist()
            aux_action = self.moves[action]
            vel_cmd.linear.x = float(aux_action.vel_linear)
            vel_cmd.angular.z = float(aux_action.vel_angular)
            self.vel_pub.publish(vel_cmd)
        """
        if action == 0: #FORWARD
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.3
            vel_cmd.angular.z = 0.0
        elif action == 1: #LEFT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = 0.3
            self.vel_pub.publish(vel_cmd)
        elif action == 2: #RIGHT
            vel_cmd = Twist()
            vel_cmd.linear.x = 0.05
            vel_cmd.angular.z = -0.3
            self.vel_pub.publish(vel_cmd)
        """   
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/pause_physics service call failed")

        state,done = self.discretize_observation(data,5)
        """
        if not done:
            
            for move in moves:
                if move.name == 'Foward':               
                    reward = move.reward
                elif move.name == 'Left':
                    reward = move.reward
                elif move.name == 'Right':
                    reward = move.reward
                elif move.name == 'TurnLeft':
                    reward = move.reward
                elif move.name == 'TurnRight':
                    reward = move.reward
                elif move.name == 'Stop':
                    reward = move.reward
        else:   
            reward = -200

        """
        """
        if not done:
            if action == 0:
                reward = 5
            else:
                reward = 1
        else:
            reward = -200
        """
        if not done:
            if action >= 0 and action <= 5:        
                reward = int(aux_action.reward)
        else:
            reward = -200

        return state, reward, done, {}

    def reset(self):

        # Resets the state of the environment and returns an initial observation.
        rospy.wait_for_service('/gazebo/reset_simulation')
        try:
            #reset_proxy.call()
            self.reset_proxy()
        except (rospy.ServiceException) as e:
            print ("/gazebo/reset_simulation service call failed")

        # Unpause simulation to make observation
        rospy.wait_for_service('/gazebo/unpause_physics')
        try:
            #resp_pause = pause.call()
            self.unpause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/unpause_physics service call failed")

        #read laser data
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('/scan', LaserScan, timeout=5)
            except:
                pass

        rospy.wait_for_service('/gazebo/pause_physics')
        try:
            #resp_pause = pause.call()
            self.pause()
        except (rospy.ServiceException) as e:
            print ("/gazebo/pause_physics service call failed")

        state = self.discretize_observation(data,5)

        return state
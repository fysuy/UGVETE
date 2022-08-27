import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# Gazebo
# ----------------------------------------

# Turtlebot envs
register(
    id='GazeboMazeTurtlebotLidar-v0',
    entry_point='gym_gazebo.envs.turtlebot:GazeboMazeTurtlebotLidarEnv',
    # More arguments here
)

register(
    id='GazeboCircuit2TurtlebotLidar-v0',
    entry_point='gym_gazebo.envs.turtlebot:GazeboCircuit2TurtlebotLidarEnv',
    # More arguments here
)
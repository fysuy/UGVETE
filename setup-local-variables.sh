echo -e "\nexport GAZEBO_MODEL_DATABASE_URI='http://models.gazebosim.org/'" >> ~/.bashrc
echo "alias killgazebogym='killall -9 rosout roslaunch rosmaster gzserver nodelet robot_state_publisher gzclient'" >> ~/.bashrc
echo "export GAZEBO_RESOURCE_PATH=$GAZEBO_RESOURCE_PATH:/usr/share/gazebo-9:$HOME/Libs/chaolmu-collection/worlds" >> ~/.bashrc
echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/usr/share/gazebo-9/models:$HOME/Libs/chaolmu-collection/models" >> ~/.bashrc
echo "export GYM_GAZEBO_WORLD_UGVETE=$UGVETE_HOME/gym_gazebo/envs/assets/worlds/maze.world" >> ~/.bashrc
echo "export GAZEBO_MASTER_URI=http://localhost:11312" >> ~/.bashrc
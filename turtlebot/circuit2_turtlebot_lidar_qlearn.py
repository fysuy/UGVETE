#!/usr/bin/env python
from functools import reduce
import gym
from gym import wrappers
import gym_gazebo
import time
import calendar;
import numpy
import random
import time
import pickle
import json
import os
import qlearn
import liveplot

if __name__ == '__main__':
    f = open(os.environ['UGVETE_HOME'] + '/app/config.json', 'r')
    config = json.loads(f.read())
    f.close()
    
    for i in range(len(config["worlds"])):
        currentWorld = config["worlds"][i]

        if currentWorld["selected"]:
            if currentWorld["name"] == 'oficina': 
                os.environ['GYM_GAZEBO_WORLD_UGVETE'] = os.environ['UGVETE_HOME'] + '/gym_gazebo/envs/assets/worlds/office.world'
            
            if currentWorld["name"] == 'laberinto': 
                os.environ['GYM_GAZEBO_WORLD_UGVETE'] = os.environ['UGVETE_HOME'] + '/gym_gazebo/envs/assets/worlds/maze.world'

            if currentWorld["name"] == 'circuito': 
                os.environ['GYM_GAZEBO_WORLD_UGVETE'] = os.environ['UGVETE_HOME'] + '/gym_gazebo/envs/assets/worlds/round.world'


    env = gym.make('GazeboCircuit2TurtlebotLidar-v0', config=config)

    outdir = '/tmp/gazebo_gym_experiments'
    # env = gym.wrappers.Monitor(env, outdir, force=True)
    env = gym.wrappers.RecordEpisodeStatistics(env)
    
    plotter = liveplot.LivePlot(outdir)

    last_time_steps = numpy.ndarray(0)

    qlearn = qlearn.QLearn(actions=range(env.action_space.n),
                    alpha=0.2, gamma=0.8, epsilon=0.9, config=config)

    initial_epsilon = qlearn.epsilon

    epsilon_discount = 0.9986

    start_time = time.time()
    highest_reward = 0

    aux_total_episodes = config['episodes']
    aux_time_steps = config['timesteps']
    total_episodes = int(aux_total_episodes)
    total_time_steps = int(aux_time_steps)
    
    print("Total episodes: " + str(total_episodes))
    print("Total timesteps: "+ str(total_time_steps))    
    print("progressFilePath: " + config['progressFilePath'])    

    gmt = time.gmtime()
    ts = calendar.timegm(gmt)

    for x in range(total_episodes):
        done = False
        cumulated_reward = 0 #Should going forward give more reward then L/R ?

        observation = env.reset()

        if qlearn.epsilon > 0.05:
            qlearn.epsilon *= epsilon_discount

        #render() #defined above, not env.render()

        state = ''.join(map(str, observation))

        for i in range(total_time_steps):

            # Pick an action based on the current state
            action = qlearn.chooseAction(state)

            # Execute the action and get feedback
            observation, reward, done, info = env.step(action)
            cumulated_reward += reward

            if highest_reward < cumulated_reward:
                highest_reward = cumulated_reward

            nextState = ''.join(map(str, observation))

            qlearn.learn(state, action, reward, nextState)

            # env._flush(force=True)

            if not(done):
                state = nextState
            else:
                last_time_steps = numpy.append(last_time_steps, [int(i + 1)])
                break

        if x%100==0 and qlearn.q != {}:
            # plotter.plot(env)
            with open('q-learn-' + str(ts) + '.pkl', 'wb') as file:
                pickle.dump(qlearn, file)
                file.close()

        m, s = divmod(int(time.time() - start_time), 60)
        h, m = divmod(m, 60)
        print ("EP: "+str(x+1)+" - [alpha: "+str(round(qlearn.alpha,2))+" - gamma: "+str(round(qlearn.gamma,2))+" - epsilon: "+str(round(qlearn.epsilon,2))+"] - Reward: "+str(cumulated_reward)+"     Time: %d:%02d:%02d" % (h, m, s))

    #Github table content
    print ("\n|"+str(total_episodes)+"|"+str(qlearn.alpha)+"|"+str(qlearn.gamma)+"|"+str(initial_epsilon)+"*"+str(epsilon_discount)+"|"+str(highest_reward)+"| PICTURE |")

    l = last_time_steps.tolist()
    l.sort()

    #print("Parameters: a="+str)
    print("Overall score: {:0.2f}".format(last_time_steps.mean()))
    print("Best 100 score: {:0.2f}".format(reduce(lambda x, y: x + y, l[-100:]) / len(l[-100:])))

    env.close()

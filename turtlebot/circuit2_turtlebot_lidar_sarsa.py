#!/usr/bin/env python
from functools import reduce
import pickle
import gym
from gym import wrappers
import gym_gazebo
import time
import numpy
import random
import time
import app.simulation as sim

import liveplot
import sarsa


if __name__ == '__main__':

    env = gym.make('GazeboCircuit2TurtlebotLidar-v0')

    outdir = '/tmp/gazebo_gym_experiments'
    env = gym.wrappers.Monitor(env, outdir, force=True)
    plotter = liveplot.LivePlot(outdir)

    last_time_steps = numpy.ndarray(0)

    sarsa = sarsa.Sarsa(actions=range(env.action_space.n),
                    epsilon=0.9, alpha=0.2, gamma=0.9)

    initial_epsilon = sarsa.epsilon

    epsilon_discount = 0.9986

    start_time = time.time()
    highest_reward = 0

    simulation = env.simulation
    aux_total_episodes, aux_time_steps = sim.get_simulation_properties(simulation)      
    total_episodes = int(aux_total_episodes)
    total_time_steps = int(aux_time_steps)
    print("Total episodes: " + str(total_episodes))
    print("Total timesteps: "+ str(total_time_steps))

    for x in range(total_episodes):
        done = False

        cumulated_reward = 0 #Should going forward give more reward then L/R ?

        observation = env.reset()

        if sarsa.epsilon > 0.05:
            sarsa.epsilon *= epsilon_discount

        #render() #defined above, not env.render()

        state = ''.join(map(str, observation))

        for i in range(total_time_steps):

            # Pick an action based on the current state
            action = sarsa.chooseAction(state)

            # Execute the action and get feedback
            observation, reward, done, info = env.step(action)
            cumulated_reward += reward

            if highest_reward < cumulated_reward:
                highest_reward = cumulated_reward

            nextState = ''.join(map(str, observation))
            nextAction = sarsa.chooseAction(nextState)

            #sarsa.learn(state, action, reward, nextState)
            sarsa.learn(state, action, reward, nextState, nextAction)

            env._flush(force=True)

            if not(done):
                state = nextState
            else:
                last_time_steps = numpy.append(last_time_steps, [int(i + 1)])
                break

        if x%100==0:
            plotter.plot(env)
            with open('sarsa-q.pkl', 'wb') as file:
                pickle.dump(sarsa, file)

        m, s = divmod(int(time.time() - start_time), 60)
        h, m = divmod(m, 60)
        print ("EP: "+str(x+1)+" - [alpha: "+str(round(sarsa.alpha,2))+" - gamma: "+str(round(sarsa.gamma,2))+" - epsilon: "+str(round(sarsa.epsilon,2))+"] - Reward: "+str(cumulated_reward)+"     Time: %d:%02d:%02d" % (h, m, s))

    #Github table content
    print ("\n|"+str(total_episodes)+"|"+str(sarsa.alpha)+"|"+str(sarsa.gamma)+"|"+str(initial_epsilon)+"*"+str(epsilon_discount)+"|"+str(highest_reward)+"| PICTURE |")

    l = last_time_steps.tolist()
    l.sort()

    #print("Parameters: a="+str)
    print("Overall score: {:0.2f}".format(last_time_steps.mean()))
    print("Best 100 score: {:0.2f}".format(reduce(lambda x, y: x + y, l[-100:]) / len(l[-100:])))

    env.close()
from random import random
from gym import Env
import gym
from gridworld import *


class SarsaLambdaAgent():
    def __init__(self, env: GridWorldEnv):
        self.env = env
        self.Q = {}
        self.E = {}
        self.state = None
        self.resetAgent()

    def act(self, a):
        return self.env.step(a)

    def resetAgent(self):
        self.state = self.env.reset()
        s_name = self._get_state_name(self.state)
        self._assert_state_in_Q(s_name, randomized=False)

    def _get_state_name(self, state):
        return str(state)

    def _is_state_in_Q(self, s):
        return self.Q.get(s) is not None

    def _init_state_value(self, s_name, randomized=True):
        if not self._is_state_in_Q(s_name):
            self.Q[s_name] = {}
            for action in range(self.env.action_space.n):
                default_v = random() / 10 if randomized is True else 0.0
                self.Q[s_name][action] = default_v

    def _assert_state_in_Q(self, s, randomized=True):
        if not self._is_state_in_Q(s):
            self._init_state_value(s, randomized)

    def _get_Q(self, s, a):
        self._assert_state_in_Q(s, randomized=True)
        return self.Q[s][a]

    def _set_Q(self, s, a, value):
        self._assert_state_in_Q(s)
        self.Q[s][a] = value

    def performPolicy(self, s, episode_num, use_epsilon):
        epsilon = 1.00 / (episode_num + 1)
        Q_s = self.Q[s]
        str_act = "unknown"
        rand_value = random()
        action = None
        if use_epsilon and rand_value < epsilon:
            action = self.env.action_space.sample()
        else:
            str_act = max(Q_s, key=Q_s.get)
            action = int(str_act)
        return action

    def learning(self, gamma, alpha, max_episode_num):
        total_time, time_in_episode, num_episode = 0, 0, 0
        while num_episode < max_episode_num:
            self.state = self.env.reset()
            s0 = self._get_state_name(self.state)
            self.env.render()
            a0 = self.performPolicy(s0, num_episode, use_epsilon=True)

            time_in_episode = 0
            is_done = False
            while not is_done:
                s1, r1, is_done, info = self.act(a0)
                self.env.render()
                s1 = self._get_state_name(s1)
                self._assert_state_in_Q(s1, randomized=True)

                a1 = self.performPolicy(s1, num_episode, use_epsilon=True)
                old_q = self._get_Q(s0, a0)
                q_prime = self._get_Q(s1, a1)
                td_target = r1 + gamma * q_prime
                new_q = old_q + alpha * (td_target - old_q)
                self._set_Q(s0, a0, new_q)

                if num_episode == max_episode_num:
                    print("t:{0:>2}: s:{1}, a:{2:2}, s1:{3}". \
                          format(time_in_episode, s0, a0, s1))

                s0, a0 = s1, a1
                time_in_episode += 1

            print("Episode {0} takes {1} steps.".format(
                num_episode, time_in_episode))  # 显示每一个Episode花费了多少步

            total_time += time_in_episode
            num_episode += 1
        return

    def _resetEValue(self):
        for value_dic in self.E.values():
            for action in range(self.env.action_space.n):
                value_dic[action] = 0.0

    def learning2(self, lambda_, gamma, alpha, max_episode_num):
        total_time, time_in_episode, num_episode = 0, 0, 0
        while num_episode < max_episode_num:
            self._resetEValue()
            s0 = self._get_state_name(self.env.reset())
            a0 = self.performPolicy(s0, num_episode, use_epsilon=True)

            time_in_episode = 0
            is_done = False
            while not is_done:
                s1, r1, is_done, info = self.act(a0)
                self.env.render()
                s1 = self._get_state_name(s1)

    def _assert_state_in_QE(self, s, radomized=True):
        if not self._is_state_in_Q(s):

def main():
    env = SimpleGridWorld()
    agent = Agent(env)
    print("Learning...")
    agent.learning(gamma=0.9, alpha=0.1, max_episode_num=800)

if __name__ == '__main__':
    main()




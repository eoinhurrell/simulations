#!/usr/bin/env python3
import numpy as np
import random
import sys
import math
from collections import Counter


class Player:
    def __init__(self, arm_pref=None):
        if arm_pref is None:
            self.arm_pref = {
                "A": 1.0,
                "B": 1.0,
                "C": 1.0,
            }
        else:
            self.arm_pref = arm_pref
        self.steps = []

    def hey(self):
        print("Hey", self.test)

    def avg_steps(self):
        return int(sum(self.steps) / len(self.steps))

    def get_reward(self, choice):
        # Furberg et al 2016
        steps = np.random.gamma(2.8, 3100)
        todays_steps = int(steps * self.arm_pref.get(choice, 0))
        self.steps.append(todays_steps)
        return todays_steps


class EpsilonGreedyBandit:
    def __init__(self, arms=None, epsilon=0.15):
        self.arms = Counter()
        if arms is None:
            arms = ["A", "B", "C"]
        for arm in arms:
            self.arms[arm] = 0
        self.epsilon = epsilon

    def choose_arm(self):
        # epsilon% likelihood of drawing a 1
        explore = np.random.binomial(1, self.epsilon)
        # if explore:
        if explore == 1:
            choice = np.random.choice(list(self.arms.keys()), size=1)[0]
        # if exploit:
        else:
            choice = self.arms.most_common(1)[0][0]
        return choice

    def add_reward(self, choice, reward):
        assert choice in self.arms
        self.arms[choice] += reward

    def report(self):
        print(self.arms)


def main():
    bandit = EpsilonGreedyBandit()
    arm_prefs = [
        {
            "A": 1.2,
            "B": 0.75,
            "C": 0.75,
        },
        {
            "A": 0.95,
            "B": 1.0,
            "C": 0.75,
        },
        {
            "A": 0.75,
            "B": 0.75,
            "C": 1.1,
        },
    ]
    players = []
    for _ in range(1000):
        players.append(Player(np.random.choice(arm_prefs, size=1)[0]))

    for day in range(21):  # 3 week simulation
        for player in players:
            choice = bandit.choose_arm()
            bandit.add_reward(choice, player.get_reward(choice))

        print("Day", day + 1)
        bandit.report()


if __name__ == '__main__':
    main()

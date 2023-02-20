import numpy as np

from board import Board

import json


class Agent:

  def __init__(self):
    self.df = 0.13
    self.lr = 0.35
    self.noise = 0.2

    self.Q = {}

  def act(self, state: str):
    if state not in self.Q:
      self.Q[state] = np.zeros(9)

    actions = np.copy(self.Q[state])
    for i in range(len(actions)):
      actions[i] += (np.random.random() * 2 - 1) * self.noise

    action: int = int(np.argmax(actions))

    return action, actions

  def learn(self, states: list[tuple[str, int]], reward: float) -> None:
    for i in range(1, len(states)):
      state = states[i - 1][0]
      future = states[i][0]

      action = states[i - 1][1]
      future_act = states[i][1]

      self._learn(state, future, action, future_act, i/reward)

  def _learn(self, state: str, future_state: str, action: float,
             future_action: float, reward: float) -> None:
    if future_state not in self.Q:
      self.Q[future_state] = np.zeros(9)
    self.Q[state][action] += self.lr * (
      reward + self.df * self.Q[future_state][future_action] -
      self.Q[state][action])


def train(agent: Agent, epochs: int):
  board = Board()
  epoch = 0

  while epoch < epochs:
    states1: list[tuple[str, int]] = []
    states2: list[tuple[str, int]] = []
    while not board.is_finished():
      state = board.encode(board.player)
      action = agent.act(state)
      position = action[0]

      position = board.play(position, random_choice=True)[0]

      if board.player == 'X':
        states1.append((state, position))
      if board.player == 'O':
        states2.append((state, position))

    if board.is_win('X'):
      agent.learn(states1, 7)
      agent.learn(states2, -1)
    elif board.is_win('O'):
      agent.learn(states1, -1)
      agent.learn(states2, 7)
    else:
      agent.learn(states1, 0.5)
      agent.learn(states2, 0.5)

    epoch += 1
    board.reset()

  with open('Q.json', 'w') as file:
    newQ = {}
    for state in agent.Q.keys():
      newQ[state] = list(agent.Q[state])
      
    file.write(json.dumps(newQ, indent='\t'))

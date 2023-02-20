import numpy as np

from colorama import Fore


class Board:

  def __init__(self):
    self.win_states = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                       [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    self.vector = np.array([])
    self.player = ''

    self.reset()

  def reset(self):
    self.vector = np.zeros(9)
    self.player = np.random.choice(['X', 'O'])

  def get_pretty_player(self):
    return {
      'X': Fore.RED + 'X' + Fore.RESET,
      'O': Fore.BLUE + 'O' + Fore.RESET
    }.get(self.player)

  def next(self):
    if self.player == 'X':
      return 'O'
    else:
      return 'X'

  def play(self, pos: int, random_choice=False):
    if pos < 0 or pos > 8:
      return pos, False

    if random_choice and not self.is_empty(pos):
      empty_pos = np.where(self.vector == 0)[0]
      pos = np.random.choice(empty_pos)

    if not self.is_empty(pos):
      return pos, False

    self.vector[pos] = self.player_id(self.player)
    self.player = self.next()

    return pos, True

  def encode(self, player: str):
    key = self.player_id(player)
    encoded = ''
    for child in self.vector:
      if child == 0:
        encoded += '-'
      elif child == key:
        encoded += '1'
      else:
        encoded += '0'
    return encoded

  def is_win(self, player: str):
    player_id = self.player_id(player)

    for state in self.win_states:
      if self.vector[state[0]] == player_id and\
              self.vector[state[1]] == player_id and\
              self.vector[state[2]] == player_id:
        return True

    return False

  def is_draw(self):
    return not self.is_win('X') and not self.is_win(
      'O') and 0 not in self.vector

  def is_finished(self):
    return self.is_win('X') or self.is_win('O') or self.is_draw()

  def is_empty(self, pos: int):
    return self.vector[pos] == 0

  @staticmethod
  def player_id(player: str):
    return {'X': -1, 'O': 1}.get(player)

  def __str__(self):
    pretty_vector = []

    for i in range(len(self.vector)):
      if self.vector[i] == -1:
        pretty_vector.append(Fore.RED + 'X' + Fore.RESET)
      elif self.vector[i] == 1:
        pretty_vector.append(Fore.BLUE + 'O' + Fore.RESET)
      else:
        pretty_vector.append(Fore.YELLOW + str(i) + Fore.RESET)

    print()
    print(f' {pretty_vector[0]} | {pretty_vector[1]} | {pretty_vector[2]} ')
    print(f'-----------')
    print(f' {pretty_vector[3]} | {pretty_vector[4]} | {pretty_vector[5]} ')
    print(f'-----------')
    print(f' {pretty_vector[6]} | {pretty_vector[7]} | {pretty_vector[8]} ')
    return ''

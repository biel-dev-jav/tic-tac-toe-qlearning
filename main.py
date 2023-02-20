import qlearn

from board import Board

import json

from colorama import Back, Fore


def main():
  agent = qlearn.Agent()
  agent.Q = json.load(open('Q.json', 'r'))
  qlearn.train(agent, 10_000)
  agent.noise = 0

  for key in agent.Q.keys():
    print(key + ' : ' + str(agent.Q[key]))

  board = Board()
  while not board.is_finished():
    print(board)

    state = board.encode(board.player)

    print('codificado:', state)
    print('probabilidades: ', end='')
    ideal, props = agent.act(state)
    for i in range(len(props)):
      if i == ideal:
        print(f'{Back.GREEN + Fore.WHITE}{i}:{props[i]:0.2f}{Back.RESET}', end=' ')
        continue
      print(f'{Back.YELLOW + Fore.WHITE}{i}:{props[i]:0.2f}{Back.RESET}', end=' ')

    print()

    pos = int(
      input(
        f'Agora é a vez do {board.get_pretty_player()}! Digite uma posição: '))

    board.play(pos)

  print()

  if board.is_win('X'):
    print('Parabéns! o X ganhou!')
  elif board.is_win('O'):
    print('Parabéns! o O ganhou!')
  else:
    print('Opps! Houve empate!')


if __name__ == '__main__':
  main()

import qlearn

from board import Board


def main():
  agent = qlearn.Agent()
  qlearn.train(agent, 10_000)
  agent.noise = 0

  for key in agent.Q.keys():
    print(key + ' : ' + str(agent.Q[key]))

  board = Board()
  while not board.is_finished():
    print(board)

    state = board.encode(board.player)

    print('codificado:', state)
    print('probabilidades:', agent.act(state))

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

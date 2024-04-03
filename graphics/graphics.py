class Graphics:
  def display_logo(self):
    print('=====================')
    print('-----FAMILY FEUD-----')
    print('=====================\n')

  def display_game_board(self, question_status):
    question_length = len(question_status['question'])
    current_total = str(question_status['current_total'])
    print(question_status)
    print('\n', question_status['question'])
    print('\n', '=' * question_length)
    print((int(question_length / 2) - len(current_total) - 1) * ' ', current_total, '\n')

    longest_answer_length = len(max(question_status['answers'], key=lambda x: len(x['answer']))['answer'])
    question_count = len(question_status['answers'])
    for answer_index in range(4 if question_count >= 4 else question_count):
      answer = question_status['answers'][answer_index]
      continue_line = True if question_count > 4 + answer_index else False
      next_answer = None

      if continue_line:
        next_answer = question_status['answers'][4 + answer_index]

      vertical_border_str = '—' * (longest_answer_length + 8)

      print('', vertical_border_str, end='' if continue_line else None)
      if continue_line:
        print(' ' * 2, vertical_border_str)

      if answer['hide']:
        print('|', ' ' * (longest_answer_length + 6), '|', end='' if continue_line else None)
      else:
        print(f'| {answer["answer"]}', end='')
        print(' ' * (longest_answer_length - len(answer["answer"]) + 1), f'| {answer["score"]} |', end='' if continue_line else None)

      if next_answer is not None:
        if next_answer['hide']:
          print(' |', ' ' * (longest_answer_length + 6), '|')
        else:
          print(f' | {next_answer["answer"]}', end='')
          print(' ' * (longest_answer_length - len(next_answer["answer"]) + 2), f'| {next_answer["score"]} |')

      print('', vertical_border_str, end='' if continue_line else None)
      if continue_line:
        print('  ', vertical_border_str)
      print()

  def display_guess_message(self, guess_message):
    if guess_message is not None:
      print(guess_message, '\n')

  def display_player_scores(self, players):
    for player in players:
      print(f'{player["name"]}: {player["score"]}')
    print()

  def display_main_menu(self):
    self.display_logo()
    print('AVAILABLE COMMANDS:')
    print('------------------')
    print('create server')
    print('join server')
    print('quit')
    print('------------------\n')

  def display_create_server_menu(self, host_info):
    self.display_logo()

    print('++++++++++++++++++')
    print('HOST: ', host_info['hostname'])
    print('IP: ', host_info['ip_address'])
    print('PORT: ', 58008)
    print('++++++++++++++++++\n')
    print('SET A PASSWORD FOR THE SERVER:')

  def display_join_server_menu(self, server_fields):
    self.display_logo()

    for key, val in server_fields.items():
      if val is not None:
        print(f'{key}: {val}')
      else:
        print(f'\nENTER {key}:')
        break

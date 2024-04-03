import socket
import os
import json
from enum import Enum

# from menu.menu import Menu
from graphics.graphics import Graphics
from game.game import GameState

class ClientState(Enum):
  MENU = 0
  PLAY = 1

class Client:
  def __init__(self) -> None:
    self.graphics = Graphics()

    #self.client_state = ClientState.MENU
    self.client_state = ClientState.PLAY
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.player_id = None

    self.quit = False
    self.client_message = '-1'
    print('\033[38;2;0;255;0m')

  def run(self):
    if not self.join_server():
      self.quit = True

    while not self.quit:
      self.update()

    self.client_socket.close()
    print('\033[0m')

  def update(self):
    try:
      self.client_socket.send(str.encode(self.client_message))
      data = json.loads(self.client_socket.recv(2048).decode())
      self.client_message = '-1'

      if data['game_state'] == 'SET_NAME':
        if not any(p['id'] == self.player_id and p['name'] != '' for p in data['players']):
          print('TELL STEVE HARVEY YOUR NAME: ')
          self.prompt_client()
      elif data['trigger_rerender']:
        self.clear_screen()
        self.graphics.display_game_board(data['question_status'])
        self.graphics.display_guess_message(data['guess_message'])
        self.graphics.display_player_scores(data['players'])
        self.client_message = 'ACK_RERENDER'
      elif data['question_status']['player_answering']['id'] == self.player_id:
        print('TYPE YOUR ANSWER: ')
        self.prompt_client()

    except KeyboardInterrupt:
      self.quit = True

  def join_server(self):
    server_address = ('192.168.1.86', 58008)

    try:
      self.client_socket.connect(server_address)
      self.player_id = int(self.client_socket.recv(2048).decode())
    except socket.error as e:
      print(e)
      return False

    return True

  def prompt_client(self):
    print('>$', end='')
    self.client_message = input()

  def clear_screen(self):
    os.system('cls' if os.name == 'nt' else 'clear')
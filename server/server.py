import socket
from _thread import *
import json

from game.game import Game

class Server:
  def __init__(self) -> None:
    self.game = Game()
    self.client_list = []

    self.rerender_flag = False
    self.rerender_ack = {}

  def start_server(self):
    host_info = self.get_host_info()
    ###################################
    print(host_info)
    server_addr = (host_info['ip_address'], 58008)

    self.server_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind(server_addr)
    self.server_socket.listen(2)

    print('SERVER STARTIED - WAITING FOR CONNECTIONS...')

    player_count = 0
    while True:
      try:
        client_socket, client_address = self.server_socket.accept()
        print(f'CLIENT {client_address} CONNECTED')

        self.game.register_user(player_count, client_address[0], client_address[1], client_socket)
        start_new_thread(self.service_client, (client_socket, player_count))

        player_count += 1
      except KeyboardInterrupt:
        print('SHUTTING DOWN...')
        self.server_socket.close()
        break

  def service_client(self, client_socket, player_id):
    client_socket.send(str.encode(str(player_id)))
    self.client_list.append(client_socket)
    reply = ''

    while True:
      try:
        data = client_socket.recv(2048).decode()
        if data != '-1':
          if not self.game.is_game_ready():
            if self.game.is_player_name_missing(player_id):
              self.game.set_player_name(player_id, data)
              if self.game.is_game_ready():
                self.rerender_flag = True
          elif data == 'ACK_RERENDER':
            self.rerender_ack[str(player_id)] = True
          else:
            self.game.process_game_command(player_id, data)
            self.rerender_flag = True
            self.rerender_ack = {}

        reply = self.game.generate_response(self.rerender_flag and str(player_id) not in self.rerender_ack)
        client_socket.sendall(reply)
        if self.rerender_flag:
          if len(self.rerender_ack) == len(self.client_list):
            self.rerender_flag = False
      except socket.error as e:
        print(e)
        break

  def get_host_info(self):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return { 'hostname': hostname, 'ip_address': ip_address }

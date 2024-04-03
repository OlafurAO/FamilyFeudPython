import socket
from _thread import *
import json
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = '192.168.43.228'
port = 5555

player_id = None

try:
  client.connect((server, port))
  player_id = int(client.recv(2048).decode())
  print(f'PLAYER ID: {player_id}')
except:
  print('NOOOOOOOOOOOOOOO')

command = '-1'

while True:
  client.send(str.encode(command))
  command = '-1'
  res = json.loads(client.recv(2048).decode())

  if res['trigger_rerender']:
    client.send(str.encode('ACK_RERENDER'))
    client.recv(2048)
    os.system('cls')
    print('WORD LIST:')
    for i in res['word_list']:
      print(i)

  if int(res['player_turn']) == player_id:
    print('$', end='')
    command = input()

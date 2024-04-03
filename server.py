import socket
from _thread import *
import json

server = '192.168.43.228'
port = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  sock.bind((server, port))
except socket.error as e:
  print(e)

sock.listen(2)
print('SERVER STARTIED - WAITING FOR CONNECTIONS...')

client_list = []

word_list = []
player_turn = 0
rerender_flag = False

rerender_ack = {}

def threaded_client(conn: socket, curr_player):
  global player_turn
  global rerender_flag
  global rerender_ack

  conn.send(str.encode(str(curr_player)))
  client_list.append(conn)
  reply = ''

  while True:
    try:
      data = conn.recv(2048).decode()
      if data == 'ACK_RERENDER':
        rerender_ack[curr_player] = True
      elif data != '-1':
        if player_turn == 1:
          player_turn = 0
        else:
          player_turn = 1
        word_list.append(data)
        rerender_flag = True
        rerender_ack = {}

      reply = { 'word_list': word_list, 'trigger_rerender': rerender_flag, 'player_turn': player_turn }
      conn.sendall(str.encode(json.dumps(reply)))
      if rerender_flag:
        if len(rerender_ack) == len(client_list):
          rerender_flag = False
    except socket.error as e:
      print(e)
      break

  print('LOST CONNECTION...')
  conn.close()

curr_player = 0
while True:
  try:
    conn, addr = sock.accept()
    print('CONNECTED TO: ', addr)

    start_new_thread(threaded_client, (conn, curr_player))
    curr_player += 1
  except:
    sock.quit()
    break
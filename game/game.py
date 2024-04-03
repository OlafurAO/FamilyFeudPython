import random
import json
from enum import Enum

from question_repo.question_repo import QuestionRepo

MAX_PLAYERS = 2

class GameState(Enum):
  SET_NAME = 0
  PLAY = 1

class Game:
  def __init__(self) -> None:
    self.question_repo = QuestionRepo()
    self.game_state = GameState.SET_NAME
    self.players = []
    self.question_status = None
    self.guess_message = None

  def process_game_command(self, player_id, command: str):
    if self.game_state == GameState.PLAY:
      self.guess_message = self.question_status.guess_answer(player_id, command)

  def register_user(self, player_id, ip_address, port, socket):
    self.players.append(Player(player_id, ip_address, port, socket))

  def generate_response(self, trigger_rerender: bool = False):
    return self.get_json_obj(message='', trigger_rerender=trigger_rerender)

  def set_player_name(self, player_id, name):
    player = self.get_player_by_id(player_id)
    if player is not None:
      player.set_name(name)
      if self.is_game_ready():
        self.init_new_question()
        self.game_state = GameState.PLAY

  def init_new_question(self, random_player = False):
    self.question_status = QuestionStatus(self.question_repo.get_new_question())
    if self.question_status.player_answering == None:
      self.question_status.set_player_answering(random.choice(self.players))

  def get_json_obj(self, message: str = None, trigger_rerender: bool = False):
    return json.dumps({
      'game_state': self.game_state.name,
      'players': [player.__dict__() for player in self.players],
      'question_status': self.question_status.__dict__() 
        if self.question_status is not None else None,
      'message': message,
      'guess_message': self.guess_message,
      'trigger_rerender': trigger_rerender
    }).encode()

  def get_player_by_id(self, player_id):
    for p in self.players:
      if p.player_id == player_id:
        return p

  def is_game_ready(self):
    return len(self.players) == MAX_PLAYERS and all(player.name is not None and player.name != '' for player in self.players)
    #return True

  def is_selecting_name(self):
    return self.game_state == GameState.SET_NAME

  def is_player_name_missing(self, player_id):
    player = self.get_player_by_id(player_id)
    if player is not None:
        return player.name == ''
    return False


class Player:
  def __init__(self, player_id, ip_address, port, socket) -> None:
    self.player_id = player_id
    self.ip_address = ip_address
    self.port = port
    self.socket = socket
    self.name = ''
    self.score = 0

  def set_name(self, name):
    self.name = name

  def set_score(self, score):
    self.score = score

  def __dict__(self):
    return {
      'id': self.player_id,
      'ip_address': self.ip_address,
      'port': self.port,
      'name': self.name,
      'score': self.score
    }

class QuestionStatus:
  def __init__(self, question_obj) -> None:
    self.question = question_obj['question']
    self.answers = [
      {'answer': answer, 'score': score, 'hide': True}
      for answer, score in question_obj['answers'].items()
    ]
    self.current_total = 0
    self.player_answering = None
    self.strikes = 0

  def set_player_answering(self, player):
    self.player_answering = player
    self.strikes = 0

  def guess_answer(self, player_id, answer: str):
    correct_guess = False
    guess_message = answer
    for a in self.answers:
      if self.check_similarity(a['answer'], answer) and a['hide'] == True:
        self.current_total += a['score']
        a['hide'] = False
        correct_guess = True

    if correct_guess:
      guess_message += ' IS ON THE BOARD!'
    else:
      guess_message += ' IS NOT ON THE BOARD! TRY AGAIN DUMBASS'

    return guess_message
  
  # Returns true if the answer is 'good enough'
  def check_similarity(self, correct_answer, player_answer):
    stop_words = {'a', 'the', 'on', 'in', 'at', 'to'}

    correct_words = set(correct_answer.lower().strip().split())
    player_words = set(player_answer.lower().strip().split())

    filtered_correct = correct_words - stop_words
    filtered_player = player_words - stop_words

    return filtered_player.issubset(filtered_correct)

  def __dict__(self):
    return {
      'question': self.question,
      'answers': self.answers,
      'current_total': self.current_total,
      'player_answering': self.player_answering.__dict__(),
      'strikes': self.strikes,
    }

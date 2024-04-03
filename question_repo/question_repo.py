import json
import msgpack
import random

class QuestionRepo:
	def __init__(self) -> None:
		with open("res/index_file.json", "r") as index_file:
				self.question_indexes = json.load(index_file)

		self.binary_file_path = "res/questions.bin"
		self.answered_questions = []
		self.question_count = len(self.question_indexes)

	def get_new_question(self):
		byte_offset = self.get_new_byte_offset()
		with open(self.binary_file_path, "rb") as binary_file:
			binary_file.seek(byte_offset)
			unpacker = msgpack.Unpacker(binary_file)
			for unpacked in unpacker:
				return unpacked

	def get_new_byte_offset(self) -> int:
		index = random.randint(0, self.question_count - 1)
		return self.question_indexes[str(index)]

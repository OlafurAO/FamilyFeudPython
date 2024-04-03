import json
import msgpack

with open("../res/questions.json") as file:
    json_data = json.load(file)

index_data = {}
curr_index_offset = 0

with open("../res/questions.bin", "wb") as binary_file:
    for index, data in enumerate(json_data):
        index_data[index] = curr_index_offset
        packed_data = msgpack.packb(data)

        binary_file.write(packed_data)
        curr_index_offset += len(packed_data)

with open("../res/index_file.json", "w") as index_file:
    json.dump(index_data, index_file)

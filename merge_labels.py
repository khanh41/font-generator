import os

all_data = []
for path in os.listdir("labels"):
    path = "labels/" + path
    data = open(path, 'r').read()
    # data = data.replace("[{'transcription':", "  [{'transcription':")
    all_data.append(data)

with open("all_data.txt", 'w') as f:
    f.write('\n'.join(all_data))

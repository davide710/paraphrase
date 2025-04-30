import pandas as pd
from google import genai
import time


df = pd.read_csv('todo.txt', sep='\t')
pieces = df['sub_sentence'].tolist()

prompt = """Translate the piece of text in PIECE to modern and simpler English, easily understandable also for non-native speakers, keeping the meaning intact. 
If it is just a part of a sentence, just translate it, do not try to guess what's before or after.
If the text is already modern and simple, return it as is. Do not add any introduction, extra text or explanation, just answer with the translation. Do not add new lines.

### PIECE:
{}

### TRANSLATION:
"""

client = genai.Client(api_key="AIzaSyDL-tR5qzjRvqIkcOz2GetiLe24skE43uA") # "AIzaSyCKVVWt1_KGxsI_bnQvcMpyPEG0NkwGEH0"

with open('dataset_light.txt', 'a') as output_file:
    output_file.write("ORIGINAL\tTRANSLATED\n")

    for i, piece in enumerate(pieces):
        if i % 50 == 0:
            print(f"Translated {i} of {len(pieces)} lines.")
        if (i+1) % 15 == 0:
            time.sleep(61)
        
        inp = prompt.format(piece)
        translation = client.models.generate_content(
            model="gemini-2.0-flash", contents=inp, # "gemini-2.0-flash-lite"
        ).text
        output_file.write(piece + "\t" + "\t" + translation + "\n")
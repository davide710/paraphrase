import pandas as pd
from google import genai
import time


df = pd.read_csv('todo.txt', sep='\t')
pieces = df['sub_sentence'].tolist()
contexts = df['context'].tolist()

prompt = """Translate the piece of text in PIECE to modern and simpler English, keeping the meaning intact. Use the CONTEXT to help you understand the piece of text.
If the text is already modern and simple, return it as is. Do not add any introduction, extra text or explanation, just answer with the translation. Do not add new lines.

### CONTEXT:
{}

### PIECE:
{}
"""

client = genai.Client(api_key="AIzaSyDL-tR5qzjRvqIkcOz2GetiLe24skE43uA") # "AIzaSyCKVVWt1_KGxsI_bnQvcMpyPEG0NkwGEH0"

with open('dataset.txt', 'a') as output_file:
    #output_file.write("ORIGINAL\tCONTEXT\tTRANSLATED\n")

    for i, (piece, context) in enumerate(zip(pieces, contexts)):
        if i % 50 == 0:
            print(f"Translated {i} of {len(pieces)} lines.")
        if (i+1) % 15 == 0:
            time.sleep(61)
        
        inp = prompt.format(context, piece)
        translation = client.models.generate_content(
            model="gemini-2.0-flash", contents=inp,
        ).text
        output_file.write(piece + "\t" + context + "\t" + translation + "\n")
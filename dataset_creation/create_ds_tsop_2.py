from google import genai
import time


prompt = """I will give you a line from "This side of paradise" by E. Hemingway. Please translate it to modern and simpler English, keeping the meaning intact.
Target slang words and phrases, complex sentence structures, difficult vocabulary, and make it more accessible to a an audience of contemporaries and non-native speakers. 
Target archaic words and phrases, and make it more accessible to a an audience of contemporaries and non-native speakers.
Do not add any introduction, extra text or explanation.
LINE:
{}
"""

client = genai.Client(api_key="api_key")

with open('dataset_tsop.txt', 'w') as output_file:
    output_file.write("ORIGINAL\tTRANSLATED\n")

    with open('data.txt', 'r') as f:
        lines = f.readlines()
        for i, orig in enumerate(lines):
            if i % 50 == 0:
                print(f"Translated {i + 1} of {len(lines)} lines.")
            if (i+1) % 15 == 0:
                time.sleep(60)
            orig = orig[:-1] # remove newline
            inp = prompt.format(orig.strip())
            translation = client.models.generate_content(
                model="gemini-2.0-flash", contents=inp,
            ).text
            output_file.write(orig + "\t" + translation + "\n")

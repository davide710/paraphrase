with open("formatted_hamlet.txt", "r") as file:
    lines = file.readlines()
    quote = ""
    data = []
    for i, line in enumerate(lines):
        if (line.startswith("ACT") and "SCENE" in line) or (line.startswith("(") and line.endswith(")\n")):
            continue
        
        line = line.strip()
        line = line.replace("\n", "")
        if ":" in line and line.split(":")[0].isupper():
            data.append(quote)
            quote = ":".join(line.split(":")[1:]).strip()
        else:
            quote += " " + line

data = data[1:]

prompt = """I will give you a line from the Hamlet by William Shakespeare. Please translate it to modern and simpler English, keeping the meaning intact.
Target archaic words and phrases, and make it more accessible to a an audience of contemporaries and non-native speakers.
Do not add any extra text or explanation.
LINE:
{}
"""
import time
from google import genai

client = genai.Client(api_key="AIzaSyCKVVWt1_KGxsI_bnQvcMpyPEG0NkwGEH0")
with open("dataset_hamlet.txt", "w") as output_file:
    output_file.write("ORIGINAL\tTRANSLATED\n")
    for i, line in enumerate(data):
        if i % 50 == 0:
            print(f"Translated {i + 1} of {len(data)} lines.")
        if (i+1) % 15 == 0:
            time.sleep(60)

        inp = prompt.format(line.strip())
        translation = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt.format(line),
        ).text
        output_file.write(line + "\t" + translation + "\n")
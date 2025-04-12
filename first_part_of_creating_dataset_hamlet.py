from google import genai
import os

client = genai.Client(api_key="AIzaSyCKVVWt1_KGxsI_bnQvcMpyPEG0NkwGEH0")

#prompt = """I will give you a line from a .txt of the Hamlet I want to reformat, and you will have to reformat it according to the following rules:
#1. If it is the start of a character line, put it in the format: CHARACTER: line
#2. If it is a stage direction, put it in the format: (stage direction)
#3. If it is the continuation of a character line, just remove initial spaces and put it in the format: line
#4. If there is a stage direction in the middle of a character line, put it in the format: part of the line before (stage direction) part of the line after
#5. If it is the line saying the act / scene, put it in the format: ACT N / SCENE N
#6. Do not add any extra text or explanation.
#LINE:
#{}"""
prompt = """I will give you a chunk of a .txt of the Hamlet I want to reformat, and you will have to reformat it according to the following rules:
1. For each character line, gather all of it and put it all in a single line in the format: CHARACTER: line
2. When there is a stage direction, put it in the format: (stage direction)
3. When there is a stage direction in the middle of a character line, put it in the format: part of the line before (stage direction) part of the line after
4. When there is the start of a new scene or act, put it in the format: ACT act_number_in_roman_numerals, SCENE scene_number_in_roman_numerals
5. Do not add any extra text or explanation.
BOOK CHUNK:
{}"""

#with open("hamlet.txt", "r") as file:
#    lines = file.readlines()
#    formatted_lines = []
#    for i, line in enumerate(lines):
#        if i > 30: break
#        if i % 500 == 0:
#            print(f"Processed {i + 1} of {len(lines)} lines.") 
#        if line.strip():
#            inp = prompt.format(line.strip())
#            text = client.models.generate_content(
#                        model="gemini-2.0-flash", contents=prompt.format(line), 
#                        ).text
#            formatted_lines.append(text)
#
#with open("formatted_hamlet.txt", "w") as output_file:
#    for formatted_line in formatted_lines:
#        output_file.write(formatted_line + "\n")
#

with open("formatted_hamlet.txt", "w") as output_file:
    for file in sorted(os.listdir("hamlet")):
        with open(os.path.join("hamlet", file), "r") as file:
            chunk = file.read()
            print(f"Processing {file}...")
            formatted = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt.format(chunk),
            ).text
            output_file.write(formatted)
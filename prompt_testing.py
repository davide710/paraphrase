from google import genai

client = genai.Client(api_key="AIzaSyCKVVWt1_KGxsI_bnQvcMpyPEG0NkwGEH0")
prompt = """I will give you a line from a .txt of the Hamlet I want to reformat, and you will have to reformat it according to the following rules:
1. If it is the start of a character line, put it in the format: CHARACTER: line
2. If it is a stage direction, put it in the format: (stage direction)
3. If it is the continuation of a character line, just remove initial spaces and put it in the format: line
4. If there is a stage direction in the middle of a character line, put it in the format: part of the line before (stage direction) part of the line after
5. If it is the line saying the act / scene, put it in the format: ACT N / SCENE N
6. Do not add any extra text or explanation.
LINE:
{}"""
line = "						 							 Bernardo 							 Who’s there?"
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=prompt.format(line), 
)
print(response.text)

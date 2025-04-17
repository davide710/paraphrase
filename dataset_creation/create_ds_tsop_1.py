import random


with open("This-side-of-paradise.txt", "r") as file:
    lines = file.readlines()
    formatted_lines = []
    for i, line in enumerate(lines):
        if line.strip():
            formatted_lines.append(line.strip())

paragraphs = []
p = ''
for i, l in enumerate(formatted_lines):
    if l == '||-+-||':
        paragraphs.append(p)
        p = ''
    else:
        p += l + ' '

originals = []
with open("data.txt", "w") as file:
    for p in paragraphs:
        sentences = p.split('.')
        #sentences = [s for s in sentences if len(s) > 1]
        n_sentences = len(sentences)
        i = 0
        while i < n_sentences:
            n = random.randint(2, 4)
            if i + n > n_sentences:
                n = n_sentences - i
            sentence = '.'.join(sentences[i:i + n])
            i += n
            s = sentence.strip()
            if s == '' or len(s) < 4:
                continue
            if s[:2] == '” ' or s[:2] == "’ " or s[:2] == ') ':
                s = s[2:]
            originals.append(s)
            file.write(s + '\n')
#print(originals[14:16])
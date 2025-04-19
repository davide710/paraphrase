from get_pieces import create_simplified_translation_dataset
from get_complexity import keep
import pandas as pd


def get_chunks_macbeth():
    with open('simplified_macbeth', 'r') as f:
        text = f.read()
    lines = text.split('\n\n')
    without_name = [':'.join(l.split(':')[1:])[1:] for l in lines]
    originals = [l.split('[[')[0][:-1] for l in without_name]
    return originals

def get_chunks_hamlet():
    df = pd.read_csv('../dataset_creation/dataset_hamlet.txt', sep='\t')
    return list(df['ORIGINAL'].values)

def get_chunks_tsop():
    with open('This-side-of-paradise.txt', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        text = ' '.join(lines)
        chapters = text.split('||-+-||')
        return chapters

def create_originals():
    chunks = get_chunks_macbeth() + get_chunks_hamlet() + get_chunks_tsop()
    print(f"Loaded {len(chunks)} chunks")
    datasets = []
    for i, c in enumerate(chunks):
        if i % 300 == 0:
            print(f"Processed {i} chunks")
        datasets.append(create_simplified_translation_dataset(c))
    print(f"Created {len(datasets)} datasets")
    d = pd.concat(datasets)
    print(f"Concatenated datasets to {len(d)} rows")
    d = d[d.apply(lambda row: keep(row['sub_sentence'], row['target_sentence']), axis=1)]
    print(f"Filtered dataset to {len(d)} rows")
    d.to_csv('dataset_newapproach.csv', index=False, sep='\t')
    print(f"Dataset created with {len(d)} rows")

create_originals()
import pandas as pd
import json
import re
import jieba
import pypinyin

SUBTLEX_FILE = 'data\SUBTLEX-CH-WF.xlsx'
CEDICT_FILE = 'data\cedict_ts.u8'
ZH_TATOEBA = 'data\cmn.txt'
EN_TATOEBA = 'data\EN.txt'
DICT_SIZE = 10_000

OUTPUT_FILE = 'mandarin_dictionary.json'

subtlex_df = pd.read_excel(SUBTLEX_FILE, header=2)

top_n_words = subtlex_df.sort_values(by='WCount', ascending=False).head(DICT_SIZE)['Word'].tolist()
top_n_set = set(top_n_words)

cedict = {}
with open(CEDICT_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        # skip comments
        if line.startswith('#'):
            continue
        match = re.match(r'(\S+) (\S+) \[(.+)\] /(.+)', line.strip())
        if match:
            traditional, simplified, pinyin, definition = match.groups()
            if simplified not in cedict:
                cedict[simplified] = {
                    'pinyin': pinyin, 
                    'definition': definition, 
                    'traditional': traditional
                }
                
def get_hanzi_meanings(word, cedict):
    meanings = []
    for char in word:
        if char in cedict:
            full_definition = cedict[char]['definition']
            first_meaning = full_definition.split('/')[0]
            meanings.append(f'{char}: {first_meaning}')
        else:
            meanings.append(f'{char}: ')
    return '; '.join(meanings)

examples = {}
with open(ZH_TATOEBA, 'r', encoding='utf-8') as zh_file, \
     open(EN_TATOEBA, 'r', encoding='utf-8') as en_file:
    for zh_line, en_line in zip(zh_file, en_file):
        zh_sentence = zh_line.strip()
        en_sentence = en_line.strip()
        seg_list = set(jieba.cut(zh_sentence))
        for word in seg_list:
            if word in top_n_set and word not in examples:
                examples[word] = (zh_sentence, en_sentence)
                if len(examples) == DICT_SIZE:
                    break
        if len(examples) == DICT_SIZE:
            break


dictionary = []
for i, word in enumerate(top_n_words):
    zh_example, en_example = examples.get(word, ('', ''))
    if zh_example:
        pinyin_example = pypinyin.lazy_pinyin(zh_example, style=pypinyin.Style.TONE2)
        example = {
            'chinese': zh_example,
            'pinyin': ' '.join(pinyin_example),
            'english': en_example
        }
    else:
        example = {}
    entry = {
        'pinyin': '', 
        'definition': '',
        'example': example, 
        'traditional': '',
        'simplified': '',
        'rank': i+1,
        'hanzi_meaning': get_hanzi_meanings(word, cedict)
    }
    if word in cedict:
        entry['pinyin'] = cedict[word]['pinyin']
        entry['definition'] = cedict[word]['definition']
        entry['traditional'] = cedict[word]['traditional']
        entry['simplified'] = word

    dictionary.append(entry)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)

print(f'Dictionary generated with {len(dictionary)} entries and saved to {OUTPUT_FILE}')
# Mandarin Chinese Dictionary Generator

This script generates a JSON dictionary of the 10000 most common Mandarin Chinese words using SUBTLEX-CH-WF, CC-CEDICT, and Tatoeba datasets.

## Requirements

### Python Libraries
- `pandas`
- `openpyxl`
- `jieba`
- `pypinyin`

To install all the required libraries at once, run the following command in your terminal:
```bash
pip install -r requirements.txt
```

### Datasets
- SUBTLEX-CH-WF: A frequency list of Chinese words from subtitles. Download the dataset (e.g., SUBTLEX-CH-WF.xlsx) and place it in your project data/ directory.

- CC-CEDICT: A Chinese-English dictionary. Download the cedict_ts.u8 file from CC-CEDICT and place it in your project data/ directory.

- Tatoeba: This is a collection of translated sentences from Tatoeba. Download the Chinese-English translations from OPUS, extract the text files (e.g., zh.txt and en.txt), and place them in your project data/ directory.

### Usage

1. Update file paths in the script.

2. Run:
```bash
python generate_dictionary.py
```

### Output Format
Each entry in the JSON array has:
- "pinyin": Pinyin of the word.
- "definition": English definition.
- "example": An object with:
  - "chinese": Chinese example sentence.
  - "pinyin": Pinyin of the sentence.
  - "english": English translation.
- "traditional": Tradional writing.
- "simplified": Simplified writing,
- "rank": Word frequency rank.
- "hanzi_meaning": Meaning of the characters.


#### Example Entry
```json
{
    "pinyin": "yi1 ge5",
    "definition": "a; an; one/the whole (afternoon, summer vacation etc)/",
    "example": {
        "chinese": "要变得完美，她就是少了一个缺点。",
        "pinyin": "ya4o bia4n de2 wa2n me3i ， ta1 jiu4 shi4 sha3o le yi2 ge4 que1 dia3n 。",
        "english": "That's because you're a girl."
    },
    "traditional": "一個",
    "simplified": "一个",
    "rank": 44,
    "hanzi_meaning": "一: one; 个: used in 自個兒|自个儿[zi4 ge3 r5]"
}
```





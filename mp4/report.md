# MP4 Report

- **Team Members:** Zhirong Chen (zhirong4), Xiaoyang Chu (xzhu58), Jiajun Hu (jiajunh5),  Yanbing Yang (yanbing7)
- **Date:** 5/14/2024

---

## Section I: Baseline Tagger
Our baseline tagger resulted in the following statistics:

|Metrics|Values|
|--|--|
|Accuracy|93.93%|
|Multitags Accuracy|90.29%|
|Unseen words Accuracy|69.70%|
|Top K Wrong Word-Tag Predictions|[('to', {'IN': 2258, 'X': 2}), ('that', {'DET': 429, 'PRON': 304, 'ADV': 15}), ('as', {'IN': 28, 'ADV': 203}), ('more', {'ADJ': 177, 'NOUN': 13})]|
|Top K Correct Word-Tag Predictions| [('the', {'DET': 13917}), (',', {'PERIOD': 11453}), ('.', {'PERIOD': 10100}), ('of', {'IN': 7056})]|

The result matches the key statistics as required by the description.

---
## Section II: Viterbi Tagger I
|Accuracy|94.32%|
|--|--|
|Multitags Accuracy|93.13%|
|Unseen words Accuracy|48.16%|
|Top K Wrong Word-Tag Predictions| [('that', {'CONJ': 197, 'DET': 187, 'PRON': 251, 'ADV': 15}), ('to', {'TO': 491, 'IN': 42, 'X': 2}), ('as', {'IN': 28, 'ADV': 194, 'CONJ': 12}), ('out', {'PART': 123, 'IN': 68})]|
|Top K Correct Word-Tag Predictions|[('the', {'DET': 13917}), (',', {'PERIOD': 11453}), ('.', {'PERIOD': 10100}), ('of', {'IN': 7056})]|

We find that Viterbi I has a higher multitags accuracy than that of the baseline tagger, whereas the unseen words accuracy is lower than the Baseline tagger.

---
## Section III: Viterbi Tagger II

|Accuracy|95.66%|
|--|--|
|Multitags Accuracy|94.30%|
|Unseen words Accuracy|66.74%|
|Top K Wrong Word-Tag Predictions| [('that',{'CONJ': 155,'DET': 237, 'PRON': 249,'ADV': 15}),('to',{'TO': 150,'IN': 134,'X': 2}),('as',{'IN':28,'ADV':195,'CONJ':13}),('more',{'ADJ':100,'ADV':54，'NOUN':13})]
|Top K Correct Word-Tag Predictions| [('the", {'DET': 13917}),(’,’,{'PERIOD': 11453}),('.",{'PERIOD': 10188}), ('of', {'IN': 7856})]|
---
## Extra Credit


---

## Statement of Contribution
- Zhirong Chen: Finish the baseline, viterbi_1, viterbi_2
- Jiajun Hu: Finish part2, Bag of words task
- Xiaoyang Chu: viterbi_1
- Yanbing Yang: Extra Credit





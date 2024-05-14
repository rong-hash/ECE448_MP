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



---
## Section III: Viterbi Tagger II


---
## Extra Credit
**Accuracy at different $\lambda_{mix}$**

  |$\lambda_{mix}$|<0.5|0.6~0.7|0.8|0.9|
  |:----:|:----:|:----:|:----:|:----:|
  |Accuracy|0.8116|0.8095|0.8012|0.7619|
  
**Conclusion of Bigram mixed model**

The Bigram model is incorporated into the original model with a fusion ratio of 𝜆 in this section. The Bigram model considers the interaction between words within the same inference group, specifically their conditional probability. Through experimentation, it was found that the optimal accuracy is achieved when the hyper-parameter 𝜆 equals 0.6. However, this may not always be advantageous due to limited training data resulting in numerous binary word groups being absent from the model. This discrepancy is further amplified by Laplace smoothing, causing significant deviation in results when relying solely on the Bigram model.  
The actural prediction accuracy did not varies as expect as the increasing 𝜆, which is monotone with the mixing weight. The mixing of model did not make a difference until the 𝜆 is higher than 0.6. We found the detailed accuracy for each classification is slightly diffrerent while the overall stastics analysis shows no variation when adjusting 𝜆 within a narrow range.

---

## Statement of Contribution
- Zhirong Chen: Finish the part 3, logistic regression
- Jiajun Hu: Finish part2, Bag of words task
- Xiaoyang Chu: Image Classification
- Yanbing Yang: Extra Credit





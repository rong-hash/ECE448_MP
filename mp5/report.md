# MP5 Report

- **Team Members:** Zhirong Chen (zhirong4), Xiaoyang Chu (xzhu58), Jiajun Hu (jiajunh5),  Yanbing Yang (yanbing7)
- **Date:** 5/25/2024

---

## Part 1

##### Snake Agent
During the train phase, the snake agent will calculate the reward of the current state and then update the quality value of the previous state-action pair. Then it will determine the action with the greatest quality value and select that action.

Durint the evaluation phase, the snake will only find the action with the greatest quality given the current state and then execute it.

##### Result

The following parameters are found to lead to good result.

|$N_e$|$C$|$\gamma$|
|--|--|--|
|20|20|0.7|

With the set of parameters, the model converges after around 15000 episodes of training.

The average point on 1000 test games is 24.777.

##### Modification

The major modification made to the state is a new "recommended action" state, which is the recommended action evalutated by the state information from the game board. The state has four possible values, which correspond to four possible actions. The "recommended action" is evalutaed based on the position of the head and adjoining body segments, if any. By adding the new state variable, the minimum points gained in the testing episodes is increased. The model is trained for 20000 episodes with following parameters.

|$N_e$|$C$|$\gamma$|
|--|--|--|
|20|20|0.7|

---

## Part 2

Accuracy: 0.858

F1-Score: 0.880511612251767

Precision: 0.8837837837837837

Recall: 0.8772635814889336

Loss vs Epoch
![loss](./part2/loss.png)

**Observation**

Initial Rapid Decrease: At the beginning of training, there's a rapid decrease in loss, which is typical as the model initially makes significant improvements from its starting parameters.

Gradual Stabilization: Following the sharp initial drop, the loss gradually stabilizes and continues to decrease slowly. This is expected behavior as the model begins to converge and makes smaller adjustments to the parameters.

Sudden Spike at the End: The most notable and unusual feature of the plot is the sharp spike in loss towards the end of the training. This kind of spike is not typical and suggests some issues with the training process.

**Explanation for Spike**

Overfitting: If the training data does not generalize well or if the model is too complex relative to the amount of training data, overfitting could occur. However, overfitting typically leads to a gradual increase in loss, particularly on a validation set, rather than a sudden spike.

Learning Rate Issues: An improperly configured learning rate can cause divergence in training at later stages, especially if it's too high. However, such issues would usually cause fluctuation or gradual increase in loss much earlier than observed here.

Data Issues: If there is an issue with how data batches are prepared or if a corrupted batch of data is fed into the training process near the end, it might cause a sudden spike in loss.

Model/Training Instability: Some inherent instability in the model or the training process, possibly due to issues with numerical stability (e.g., very large or very small gradients leading to exploding or vanishing gradients), might also cause this. This could be exacerbated by specific activation functions or the lack of normalization layers in the network.



---

## Statement of Contribution
- Zhirong Chen: Finish part 2
- Jiajun Hu: 
- Xiaoyang Chu: 
- Yanbing Yang: 





# 机器学习 Machine Learning
## 贝叶斯 
### 贝叶斯公式 Bayesian Rule  
$$
P(A|B) = \frac{P(B|A)P(A)}{P(B)}
$$
-  P(A|B)  是在事件 B 发生的条件下事件 A 发生的概率，也称为**后验概率 Posteriori**
-  P(B|A)  是在事件 A 发生的条件下事件 B 发生的概率。
-  P(A)    是事件 A 的概率，也称为 **先验概率 Prior**
-  P(B)    是事件 B 的概率

### 贝叶斯推理 Bayesian Inference  
E = Evidence  
Y = Query variable / Class variable of the category  

$$
Y \in \{\text{spam}, \text{not spam}\}, \quad E = \text{email message}
$$

**最大后验概率估计决策 Maximum a Posteriori (MAP) decision**





### 贝叶斯学习 Bayesian Learning




### 未分类

|$X_1$|$X_2$|$Y$|
|---|---|---|
|0|0|0|
|0|1|1|
|1|2|1|
|0|0|1|
|2|2|0|
|1|1|0|
|0|2|1|
|2|0|0|
|2|1|0|
|1|0|0|

- 朴素贝叶斯 假设每个变量 X 相互独立  
  
计算条件概率：
$$ P(Y = 0 \mid X = (0, 2)) \quad \text{AND} \quad P(Y = 1 \mid X = (0, 2)) $$

计算过程：
  $$ P(Y=0)=\frac{6}{10} $$
  $$ P(Y=1)=\frac{4}{10} $$  
  $$ \quad $$

  $$ P(X=(0,2)|Y=0) = \color{red}{0} $$
  $$ P(X=(0,2)|Y=1) = \color{red}{\frac{1}{4}} $$  
  $$ \quad $$

  $$ P(Y = 0 \mid X = (0, 2))  = \color{red}{\frac{P(X=(0,2)|Y=0) \cdot P(Y=0)}{P(X=(0,2)} = 0}$$ 
  $$ P(Y = 1 \mid X = (0, 2))  = \color{red}{\frac{P(X=(0,2)|Y=1) \cdot P(Y=1)}{P(X=(0,2)} = ?}$$ 
  $$ \quad $$

  $$ P(X=(0,2)|Y=0) = \color{green}{P(X_1 = 0|Y=0) \cdot P(X_2 = 2| Y = 0)} = \frac{3}{4} \cdot \frac{2}{4}$$
  $$ P(X=(0,2)|Y=1) = \color{green}{P(X_1 = 0|Y=1) \cdot P(X_2 = 2| Y = 1)} = \frac{1}{6} \cdot \frac{1}{6}$$  




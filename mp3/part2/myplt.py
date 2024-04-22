import math
from collections import Counter, defaultdict, OrderedDict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def confusion_matrix_plot(true_labels, predicted_labels):
    # 创建混淆矩阵
    confusion_matrix = [[0 for _ in range(14)] for _ in range(14)]
    for true_label, predicted_label in zip(true_labels, predicted_labels):
        confusion_matrix[true_label - 1][predicted_label - 1] += 1
    
    # 计算百分比
    for i in range(14):
        total = sum(confusion_matrix[i])
        for j in range(14):
            confusion_matrix[i][j] = round(confusion_matrix[i][j] / total, 2)

    # 使用matplotlib绘制混淆矩阵
    fig, ax = plt.subplots(figsize=(10, 8))  # 设置画布大小
    cax = ax.matshow(confusion_matrix, cmap='viridis')  # 选择颜色映射
    plt.title('Confusion Matrix', pad=20)  # 增加标题上方的空间
    fig.colorbar(cax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_xticks(np.arange(14))
    ax.set_yticks(np.arange(14))
    ax.set_xticklabels(range(1, 15))
    ax.set_yticklabels(range(1, 15))
    ax.xaxis.set_label_position('top')  # 将x轴标签放到顶部
    ax.xaxis.tick_top()  # 将x轴刻度标签也放到顶部

    # 在每个单元格中加入数值
    for (i, j), val in np.ndenumerate(confusion_matrix):
        ax.text(j, i, f'{val}', ha='center', va='center', color='white')

    plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
    plt.savefig('D:\DeskTop\Embedded\ECE448\ece448_mp\mp3\img\part2_confusion_matrix.png', bbox_inches='tight')  
    plt.show()  # 显示图形
    
    return confusion_matrix


def data_plot(precision, recall, f1_scores):
    # 创建一个DataFrame来存储结果
    results_df = pd.DataFrame({
        'Class': list(range(1, len(precision)+1)),
        'Precision': [f"{p:.2f}" for p in precision],  # 格式化为两位小数
        'Recall': [f"{r:.2f}" for r in recall],        # 格式化为两位小数
        'F1 Score': [f"{f:.2f}" for f in f1_scores]    # 格式化为两位小数
    })
    
    # 绘图设置
    fig, ax = plt.subplots(figsize=(10, 6))  # 根据需要调整大小
    ax.axis('tight')
    ax.axis('off')

    colWidths = [0.1, 0.2, 0.2, 0.2]  # 这些值可以根据实际需要调整

    table = ax.table(cellText=results_df.values,
                     colLabels=results_df.columns,
                     cellLoc='center',
                     loc='center',
                     colColours=["palegreen"] * len(results_df.columns),
                     colWidths=colWidths)

    table.auto_set_font_size(False)  # 禁止自动设置字体大小
    table.set_fontsize(12)  # 设置字体大小
    table.scale(1.2, 1.2)  # 调整表格比例

    # 调整绘图区域边距
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)  # 减少白边

    # 保存图像
    plt.savefig(r"D:\DeskTop\Embedded\ECE448\ece448_mp\mp3\img\part2_results_table.png", bbox_inches='tight')
    plt.show()  # 显示图表以便直接查看


def top20(word_count_in_label):
    # 创建一个字典，用于存储每个标签的前20个单词
    top20_words = {}
    for label,word_count in word_count_in_label.items():
        # 按单词出现次数降序排序
        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        top20_words[label] = [word for word, count in sorted_word_count[:20]]
    return top20_words


def plot_top_words(tag_words_dict):
    # 构建一个DataFrame来存储每个标签的词
    data = {'Tag': [], 'Words': []}
    for tag, words in tag_words_dict.items():
        data['Tag'].append(tag)
        data['Words'].append(', '.join(words))  # 将词列表转换为字符串

    results_df = pd.DataFrame(data)
    
    # 绘图设置，计算表格需要的大小
    n_rows = len(results_df)
    cell_height = 0.3
    fig_height = cell_height * n_rows + 1  # 留出空间给标题

    fig, ax = plt.subplots(figsize=(12, fig_height))  # 根据行数调整高度
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=results_df.values,
                     colLabels=results_df.columns,
                     cellLoc='center',
                     loc='center',
                     colWidths=[0.1, 0.9])  # 第一列窄，第二列宽

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)  # 调整表格的行高

    plt.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

    # 保存和显示图像
    plt.savefig("top_words_table.png", bbox_inches='tight')
    plt.show()



def save_top_words_to_csv(tag_words_dict, file_path):
    # 构建一个DataFrame来存储每个标签的词
    data = {'Tag': [], 'Words': []}
    for tag, words in tag_words_dict.items():
        # 直接将词列表转换为逗号分隔的字符串
        data['Tag'].append(tag)
        data['Words'].append(', '.join(words))

    results_df = pd.DataFrame(data)
    
    # 保存为CSV文件
    results_df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

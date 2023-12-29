import pandas as pd
import matplotlib.pyplot as plt

def count_string_lengths(file_path):
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 统计每一行的字符串长度
    lengths = [len(line.strip()) for line in lines]

    # 创建DataFrame并统计不同长度的出现次数
    df = pd.DataFrame(lengths, columns=['Length'])
    counts = df['Length'].value_counts().sort_index()

    # 绘制柱形统计图
    plt.bar(counts.index, counts.values, color='skyblue')
    plt.xlabel('length')
    plt.xlim(0,140)
    plt.ylabel('count')
    plt.ylim(0,10500)
    plt.title('DNA length statistics')
    plt.show()

# 输入文件路径
file_path = '50-SF.txt'
count_string_lengths(file_path)

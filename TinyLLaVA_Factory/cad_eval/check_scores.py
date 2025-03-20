import os
import csv
import argparse

def count_functions(file_path):
    """统计指定文件中各个函数的数量"""
    counts = {'add_line': 0, 'add_arc': 0, 'add_circle': 0, 'add_loop': 0}
    with open(file_path, 'r') as f:
        for line in f:
            for key in counts.keys():
                counts[key] += line.count(key)
    return counts

def calculate_scores(generated_counts, answer_counts):
    """计算 Curve_acc 和 Loop_acc 分数"""
    L1, A1, C1, P1 = generated_counts['add_line'], generated_counts['add_arc'], generated_counts['add_circle'], generated_counts['add_loop']
    L, A, C, P = answer_counts['add_line'], answer_counts['add_arc'], answer_counts['add_circle'], answer_counts['add_loop']

    # 计算 Curve_acc
    curve_acc = (L + A + C - min(abs(L - L1), L) - min(abs(A - A1), A) - min(abs(C - C1), C)) / (L + A + C) * 100

    # 计算 Loop_acc
    loop_acc = (P - min(abs(P - P1), P)) / P * 100 if P > 0 else 0

    return curve_acc, loop_acc

def main(generated_folder, answer_folder, output_csv):
    results = []

    # 遍历标准答案文件夹
    for filename in os.listdir(answer_folder):
        if filename.endswith('.py'):
            answer_file_path = os.path.join(answer_folder, filename)
            generated_file_path = os.path.join(generated_folder, filename)

            # 统计标准答案文件中的函数数量
            answer_counts = count_functions(answer_file_path)

            # 检查生成文件是否存在
            if os.path.exists(generated_file_path):
                # 统计生成文件中的函数数量
                generated_counts = count_functions(generated_file_path)

                # 计算分数
                curve_acc, loop_acc = calculate_scores(generated_counts, answer_counts)
            else:
                # 如果生成文件不存在，记为 0 分
                curve_acc, loop_acc = 0.0, 0.0
                #print(f"生成文件不存在: {generated_file_path}，记为 0 分。")

            # 将结果添加到列表中
            results.append([filename.split('.')[0], curve_acc, loop_acc])

    # 输出结果到 CSV 文件
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Curve_acc', 'Loop_acc'])  # 写入表头
        csv_writer.writerows(results)  # 写入数据

    print(f"结果已输出到 {output_csv}")

    # 计算平均分
    if results:
        avg_curve_acc = sum(result[1] for result in results) / len(results)
        avg_loop_acc = sum(result[2] for result in results) / len(results)
        print(f"平均 Curve_acc: {avg_curve_acc:.2f}%")
        print(f"平均 Loop_acc: {avg_loop_acc:.2f}%")
    else:
        print("没有有效的结果可供计算平均分。")

if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description='检查生成的 Python 文件与标准答案的差异并计算分数')
    parser.add_argument('--gen', type=str, help='生成的 Python 文件夹路径')
    parser.add_argument('--ans', type=str, help='标准答案文件夹路径')
    parser.add_argument('--output', type=str, default='output_scores.csv', help='输出 CSV 文件的路径')

    args = parser.parse_args()

    main(args.gen, args.ans, args.output)

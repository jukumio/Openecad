import os
import csv
import argparse

def count_functions(file_path):
    """统计指定文件中各个函数的数量"""
    counts = {'add_line': 0, 'add_arc': 0, 'add_circle': 0, 'add_loop': 0, 'add_sketchplane': 0}
    with open(file_path, 'r') as f:
        for line in f:
            for key in counts.keys():
                counts[key] += line.count(key)
    return counts

def extract_loops(file_path):
    """从文件中提取所有的环"""
    loops = []
    current_loop = []
    with open(file_path, 'r') as f:
        for line in f:
            if 'add_loop' in line:
                if current_loop:
                    loops.append(current_loop)
                    current_loop = []
            elif any(func in line for func in ['add_line', 'add_arc', 'add_circle']):
                current_loop.append(line.strip())
    if (current_loop):
        loops.append(current_loop)
    return loops

def is_same_loop(loop1, loop2):
    """判断两个环是否完全一致（包括正序和倒序）"""
    if len(loop1) != len(loop2):
        return False
    for i in range(len(loop1)):
        if loop1 == loop2[i:] + loop2[:i] or loop1 == loop2[i:][::-1] + loop2[:i][::-1]:
            return True
    return False

def calculate_curve_acc(loop1, loop2):
    """计算两个环的 Curve_acc 分数"""
    counts1 = {'add_line': 0, 'add_arc': 0, 'add_circle': 0}
    counts2 = {'add_line': 0, 'add_arc': 0, 'add_circle': 0}
    for line in loop1:
        for key in counts1.keys():
            counts1[key] += line.count(key)
    for line in loop2:
        for key in counts2.keys():
            counts2[key] += line.count(key)
    L1, A1, C1 = counts1['add_line'], counts1['add_arc'], counts1['add_circle']
    L, A, C = counts2['add_line'], counts2['add_arc'], counts2['add_circle']
    curve_acc = (L + A + C - min(abs(L - L1), L) - min(abs(A - A1), A) - min(abs(C - C1), C)) / (L + A + C) * 90
    return curve_acc

def calculate_file_score(generated_loops, answer_loops):
    """计算文件的最终得分"""
    total_score = 0
    total_weight = 0
    used_generated_loops = set()
    
    for answer_loop in answer_loops:
        best_score = 0
        best_match = None
        for i, generated_loop in enumerate(generated_loops):
            if i in used_generated_loops:
                continue
            if is_same_loop(answer_loop, generated_loop):
                best_score = 100
                best_match = i
                break
            else:
                score = calculate_curve_acc(answer_loop, generated_loop)
                if score > best_score:
                    best_score = score
                    best_match = i
        if best_match is not None:
            used_generated_loops.add(best_match)
        
        # 计算权重
        num_curves = len(answer_loop)
        weight = 1 + 0.05 * (num_curves - 1)
        total_score += best_score * weight
        total_weight += weight

    average_score = total_score / total_weight if total_weight > 0 else 0

    # 计算环数差异的影响
    P = len(answer_loops)
    P1 = len(generated_loops)
    if P1 < P:
        loop_acc = 0
    else:
        loop_acc = (P - min(abs(P - P1), P)) / P * 100

    # 最终得分是环的平均分和环数差异得分的加权平均
    final_score = (average_score * 0.9 + loop_acc * 0.1)
    return final_score, len(answer_loops)

def main(generated_folder, answer_folder, output_csv):
    results = []
    total_weighted_score = 0
    total_weight = 0

    # 遍历标准答案文件夹
    for filename in os.listdir(answer_folder):
        if filename.endswith('.py'):
            answer_file_path = os.path.join(answer_folder, filename)
            generated_file_path = os.path.join(generated_folder, filename)

            # 提取标准答案文件和生成文件中的环
            answer_loops = extract_loops(answer_file_path)
            if os.path.exists(generated_file_path):
                generated_loops = extract_loops(generated_file_path)
            else:
                generated_loops = []
                #print(f"生成文件不存在: {generated_file_path}，记为 0 分。")

            # 计算文件的最终得分
            file_score, num_loops = calculate_file_score(generated_loops, answer_loops)

            # 计算权重
            weight = 1 + 0.1 * (num_loops - 1)
            total_weighted_score += file_score * weight
            total_weight += weight

            # 统计 add_sketchplane 数量
            function_counts = count_functions(answer_file_path)
            add_sketchplane_count = function_counts['add_sketchplane']

            # 将结果添加到列表中
            results.append([filename, file_score, add_sketchplane_count])

    # 输出结果到 CSV 文件
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Score', 'Add_Sketchplane_Count'])  # 写入表头
        csv_writer.writerows(results)  # 写入数据

    # 计算加权平均分
    if total_weight > 0:
        weighted_avg_score = total_weighted_score / total_weight
        print(f"加权平均分: {weighted_avg_score:.2f}%")
    else:
        print("没有有效的结果可供计算加权平均分。")



if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description='检查生成的 Python 文件与标准答案的差异并计算分数')
    parser.add_argument('--gen', type=str, help='生成的 Python 文件夹路径')
    parser.add_argument('--ans', type=str, help='标准答案文件夹路径')
    parser.add_argument('--output', type=str, default='output_scores.csv', help='输出 CSV 文件的路径')

    args = parser.parse_args()

    main(args.gen, args.ans, args.output)

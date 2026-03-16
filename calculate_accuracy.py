import json
import os

# 读取验证文件，获取正确答案
def load_ground_truth(file_path):
    ground_truth = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line.strip())
            task_id = data['task_id']
            ground_truth[task_id] = data['Final answer'].strip().lower()
    return ground_truth

# 读取输出文件夹，获取预测答案
def load_predictions(folder_path):
    predictions = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            task_id = filename.split('.')[0]
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip().lower()
                predictions[task_id] = content
    return predictions

# 计算准确率
def calculate_accuracy(ground_truth, predictions):
    correct = 0
    total = 0
    
    for task_id, true_answer in ground_truth.items():
        if task_id in predictions:
            pred_answer = predictions[task_id]
            if pred_answer == true_answer:
                correct += 1
            total += 1
    
    if total == 0:
        return 0.0
    return correct / total

# 主函数
def main():
    validate_file = 'd:\\gaia\\gaia_validate_level1.jsonl'
    output_folder = 'd:\\gaia\\gaia_level1'
    
    ground_truth = load_ground_truth(validate_file)
    predictions = load_predictions(output_folder)
    
    accuracy = calculate_accuracy(ground_truth, predictions)
    
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Correct: {sum(1 for task_id, true_answer in ground_truth.items() if task_id in predictions and predictions[task_id] == true_answer)}")
    print(f"Total: {sum(1 for task_id in ground_truth if task_id in predictions)}")

if __name__ == "__main__":
    main()

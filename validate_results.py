import json
import os

# 配置
GAIA_VALIDATE_LEVEL1 = 'gaia_validate_level1.jsonl'
GAIA_VALIDATE_LEVEL2 = 'gaia_validate_level2.jsonl'
GAIA_VALIDATE_LEVEL3 = 'gaia_validate_level3.jsonl'
OUTPUT_DIR = 'outputs'

class GaiaValidator:
    def __init__(self):
        self.tasks = {}
        self.load_gaia_tasks()
        
    def load_gaia_tasks(self):
        """加载 GAIA 任务及正确答案"""
        # 加载 Level 1
        with open(GAIA_VALIDATE_LEVEL1, 'r', encoding='utf-8') as f:
            for line in f:
                task = json.loads(line)
                self.tasks[task['task_id']] = {
                    'final_answer': task['Final answer'],
                    'level': task['Level'],
                    'question': task['Question']
                }
        
        # 加载 Level 2
        with open(GAIA_VALIDATE_LEVEL2, 'r', encoding='utf-8') as f:
            for line in f:
                task = json.loads(line)
                self.tasks[task['task_id']] = {
                    'final_answer': task['Final answer'],
                    'level': task['Level'],
                    'question': task['Question']
                }
        
        # 加载 Level 3
        with open(GAIA_VALIDATE_LEVEL3, 'r', encoding='utf-8') as f:
            for line in f:
                task = json.loads(line)
                self.tasks[task['task_id']] = {
                    'final_answer': task['Final answer'],
                    'level': task['Level'],
                    'question': task['Question']
                }
        
    def load_generated_results(self):
        """加载生成的结果"""
        generated_results = {}
        
        for file in os.listdir(OUTPUT_DIR):
            if file.endswith('.txt') and file != 'index.json':
                task_id = file.replace('.txt', '')
                file_path = os.path.join(OUTPUT_DIR, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    generated_answer = f.read().strip()
                generated_results[task_id] = generated_answer
        
        return generated_results
    
    def validate(self):
        """验证结果"""
        generated_results = self.load_generated_results()
        
        # 初始化统计数据
        total_tasks = len(generated_results)
        correct_tasks = 0
        level_stats = {
            1: {'total': 0, 'correct': 0},
            2: {'total': 0, 'correct': 0},
            3: {'total': 0, 'correct': 0}
        }
        detailed_results = []
        
        # 验证每个任务
        for task_id, generated_answer in generated_results.items():
            if task_id in self.tasks:
                task_info = self.tasks[task_id]
                correct_answer = task_info['final_answer']
                level = task_info['level']
                
                # 标准化答案格式
                generated_answer_norm = self.normalize_answer(generated_answer)
                correct_answer_norm = self.normalize_answer(correct_answer)
                
                # 判断是否正确
                is_correct = generated_answer_norm == correct_answer_norm
                
                # 更新统计数据
                level_stats[level]['total'] += 1
                if is_correct:
                    correct_tasks += 1
                    level_stats[level]['correct'] += 1
                
                # 记录详细结果
                detailed_results.append({
                    'task_id': task_id,
                    'level': level,
                    'generated_answer': generated_answer,
                    'correct_answer': correct_answer,
                    'is_correct': is_correct
                })
            else:
                print(f"Warning: Task {task_id} not found in GAIA data")
        
        # 计算准确率
        if total_tasks > 0:
            overall_accuracy = correct_tasks / total_tasks * 100
        else:
            overall_accuracy = 0
        
        # 生成报告
        self.generate_report(overall_accuracy, level_stats, detailed_results, total_tasks, correct_tasks)
        
        return overall_accuracy, level_stats, detailed_results
    
    def normalize_answer(self, answer):
        """标准化答案格式"""
        # 去除前后空格
        answer = answer.strip()
        # 转换为小写
        answer = answer.lower()
        # 去除标点符号
        import string
        answer = answer.translate(str.maketrans('', '', string.punctuation))
        # 去除多余的空格
        answer = ' '.join(answer.split())
        return answer
    
    def generate_report(self, overall_accuracy, level_stats, detailed_results, total_tasks, correct_tasks):
        """生成验证报告"""
        report = f"""# GAIA 评测验证报告

## 总体统计
- 总任务数: {total_tasks}
- 正确任务数: {correct_tasks}
- 准确率: {overall_accuracy:.2f}%

## 按难度级别统计
"""
        
        # 添加级别统计
        for level in [1, 2, 3]:
            stats = level_stats[level]
            if stats['total'] > 0:
                accuracy = stats['correct'] / stats['total'] * 100
            else:
                accuracy = 0
            report += f"- Level {level}: {stats['correct']}/{stats['total']} ({accuracy:.2f}%)\n"
        
        # 添加详细结果
        report += "\n## 详细结果\n"
        report += "| 任务ID | 级别 | 生成答案 | 正确答案 | 结果 |\n"
        report += "|--------|------|----------|----------|------|\n"
        
        for result in detailed_results:
            status = "✅ 正确" if result['is_correct'] else "❌ 错误"
            report += f"| {result['task_id']} | {result['level']} | {result['generated_answer']} | {result['correct_answer']} | {status} |\n"
        
        # 保存报告
        report_file = os.path.join(OUTPUT_DIR, 'validation_report.md')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("验证报告已生成: outputs/validation_report.md")
        print(f"总体准确率: {overall_accuracy:.2f}%")

def main():
    """主函数"""
    print("开始验证 GAIA 评测结果...")
    
    validator = GaiaValidator()
    overall_accuracy, level_stats, detailed_results = validator.validate()
    
    print("验证完成!")

if __name__ == "__main__":
    main()

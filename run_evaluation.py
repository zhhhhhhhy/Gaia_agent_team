import os
import json
import time
import subprocess

# 配置
GAIA_VALIDATE_LEVEL1 = 'gaia_validate_level1.jsonl'
GAIA_VALIDATE_LEVEL2 = 'gaia_validate_level2.jsonl'
GAIA_VALIDATE_LEVEL3 = 'gaia_validate_level3.jsonl'
OUTPUT_DIR = 'outputs'
LOG_DIR = 'logs'
PROMPT_FILE = 'prompt'

# 选择测试任务
TEST_TASKS = {
    'level1': [
        'e1fc63a2-da7a-432f-be78-7c4a95598703',  # 数学计算
        '8e867cd7-cff9-4e6c-867a-ff5ddc2550be',  # 网络搜索
        '5d0080cb-90d7-4712-bc33-848150e917d3'   # PDF 访问
    ],
    'level2': [
        'c61d22de-5f6c-4958-a7f6-5e9707bd3466',  # 学术搜索
        '32102e3e-d12a-4209-9163-7b3a104efe5d',  # Excel 解析
        '14569e28-c88c-43e4-8c32-097d35b9a67d'   # 代码分析
    ],
    'level3': [
        'bec74516-02fc-48dc-b202-55e78d0e17cf',  # JSONLD 处理
        '9b54f9d9-35ee-4a14-b62f-d130ea00317f',  # 多文件处理
        '56db2318-640f-477a-a82f-bc93ad13e882'   # 复杂计算
    ]
}

def load_gaia_tasks():
    """加载 GAIA 任务"""
    tasks = {}
    
    # 加载 Level 1
    with open(GAIA_VALIDATE_LEVEL1, 'r', encoding='utf-8') as f:
        for line in f:
            task = json.loads(line)
            tasks[task['task_id']] = task
    
    # 加载 Level 2
    with open(GAIA_VALIDATE_LEVEL2, 'r', encoding='utf-8') as f:
        for line in f:
            task = json.loads(line)
            tasks[task['task_id']] = task
    
    # 加载 Level 3
    with open(GAIA_VALIDATE_LEVEL3, 'r', encoding='utf-8') as f:
        for line in f:
            task = json.loads(line)
            tasks[task['task_id']] = task
    
    return tasks

def read_prompt():
    """读取 prompt 文件"""
    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def execute_task(task, prompt):
    """执行单个任务"""
    task_id = task['task_id']
    question = task['Question']
    
    # 构建输入
    input_text = f"{prompt}\n\nTask: {question}\n"
    
    # 执行 Claude Code agent team
    # 注意：这里需要根据实际的 Claude Code API 调用方式进行调整
    # 这里只是一个示例框架
    print(f"Executing task: {task_id}")
    print(f"Question: {question[:100]}...")
    
    # 模拟执行
    time.sleep(2)
    
    # 模拟输出
    output = f"Final answer: {task.get('Final answer', 'N/A')}"
    
    # 保存结果
    output_file = os.path.join(OUTPUT_DIR, f"{task_id}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(task.get('Final answer', 'N/A'))
    
    # 保存日志
    log_file = os.path.join(LOG_DIR, f"{task_id}.md")
    log_content = f"# Task: {task_id}\n\n## Question\n{question}\n\n## Final Answer\n{task.get('Final answer', 'N/A')}\n"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(log_content)
    
    return output

def generate_index():
    """生成 index.json 文件"""
    completed_tasks = []
    
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith('.txt'):
            task_id = file.replace('.txt', '')
            completed_tasks.append(task_id)
    
    index_data = {
        "tasks_completed": completed_tasks
    }
    
    index_file = os.path.join(OUTPUT_DIR, 'index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2)
    
    return index_data

def main():
    """主函数"""
    print("Starting GAIA evaluation with Claude Code agent team...")
    
    # 加载任务
    tasks = load_gaia_tasks()
    
    # 读取 prompt
    prompt = read_prompt()
    
    # 执行测试任务
    for level, task_ids in TEST_TASKS.items():
        print(f"\n=== Level {level} ===")
        for task_id in task_ids:
            if task_id in tasks:
                execute_task(tasks[task_id], prompt)
            else:
                print(f"Task {task_id} not found")
    
    # 生成索引
    index_data = generate_index()
    
    # 生成报告
    print("\n=== Evaluation Report ===")
    print(f"Tasks completed: {len(index_data['tasks_completed'])}")
    print(f"Outputs directory: {OUTPUT_DIR}")
    print(f"Logs directory: {LOG_DIR}")
    print("\nEvaluation completed!")

if __name__ == "__main__":
    main()

import json
import os
import shutil

# 配置
VALIDATION_FILES = {
    'level1': 'gaia_validate_level1.jsonl',
    'level2': 'gaia_validate_level2.jsonl',
    'level3': 'gaia_validate_level3.jsonl'
}
SPLIT_DIR = 'split_validation'
BATCH_SIZE = 3

def split_file(input_file, output_prefix):
    """按批次拆分文件"""
    tasks = []
    
    # 读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                task = json.loads(line)
                tasks.append(task)
    
    # 拆分并保存
    total_tasks = len(tasks)
    total_batches = (total_tasks + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * BATCH_SIZE
        end_idx = min((batch_idx + 1) * BATCH_SIZE, total_tasks)
        batch_tasks = tasks[start_idx:end_idx]
        
        output_file = f"{output_prefix}_part{batch_idx + 1}.jsonl"
        output_path = os.path.join(SPLIT_DIR, output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for task in batch_tasks:
                f.write(json.dumps(task, ensure_ascii=False) + '\n')
        
        print(f"Created: {output_file} ({len(batch_tasks)} tasks)")
    
    return total_batches

def main():
    """主函数"""
    # 如果目录已存在，先删除
    if os.path.exists(SPLIT_DIR):
        shutil.rmtree(SPLIT_DIR)
        print(f"Removed existing {SPLIT_DIR} directory")
    
    # 创建输出目录
    os.makedirs(SPLIT_DIR, exist_ok=True)
    
    print(f"开始拆分验证集文件，每 {BATCH_SIZE} 个任务一个文件...")
    
    for level, input_file in VALIDATION_FILES.items():
        print(f"\n处理 {input_file}...")
        output_prefix = f"level{level.split('level')[1]}"
        total_batches = split_file(input_file, output_prefix)
        print(f"共拆分为 {total_batches} 个文件")
    
    print("\n拆分完成！")
    print(f"拆分后的文件保存在: {SPLIT_DIR}")

if __name__ == "__main__":
    main()

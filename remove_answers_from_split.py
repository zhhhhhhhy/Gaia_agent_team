import json
import os

# 配置
SPLIT_DIR = 'split_validation'

def remove_answers():
    """删除拆分文件中的答案部分"""
    # 获取所有拆分文件
    split_files = []
    for file in os.listdir(SPLIT_DIR):
        if file.endswith('.jsonl'):
            split_files.append(file)
    
    print(f"找到 {len(split_files)} 个拆分文件")
    
    for file in split_files:
        file_path = os.path.join(SPLIT_DIR, file)
        tasks = []
        
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    task = json.loads(line)
                    # 删除 Final answer 字段
                    if 'Final answer' in task:
                        del task['Final answer']
                    tasks.append(task)
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            for task in tasks:
                f.write(json.dumps(task, ensure_ascii=False) + '\n')
        
        print(f"处理完成: {file}")
    
    print("\n所有拆分文件的答案已删除！")

def main():
    """主函数"""
    print("开始删除拆分文件中的答案部分...")
    remove_answers()

if __name__ == "__main__":
    main()

import os

def print_directory_structure(start_path, indent=0):
    """
    遞迴遍歷並打印指定目錄的結構，排除 .mypy_cache、.git 資料夾和 .csv 文件。

    Args:
        start_path (str): 起始的目錄路徑。
        indent (int): 用於控制縮進層級的參數。
    """
    for item in sorted(os.listdir(start_path)):  # 使用排序讓結果有序
        item_path = os.path.join(start_path, item)
        
        # 排除條件：忽略 .mypy_cache、.git 資料夾和 .csv 文件
        if item in {".mypy_cache", ".git"} or item.endswith('.csv'):
            continue
        
        if os.path.isdir(item_path):
            print('  ' * indent + f'📂 {item}')  # 資料夾顯示
            print_directory_structure(item_path, indent + 1)
        else:
            print('  ' * indent + f'📄 {item}')  # 檔案顯示

if __name__ == "__main__":
    # 替換為您的專案根目錄
    project_root = "D:\\AI_course\\Finance_data_visualization"
    print(f"Project Directory Structure ({project_root}):\n")
    print_directory_structure(project_root)

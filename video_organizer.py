#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频文件整理器
功能：将指定目录下的所有视频文件从其子文件夹移动到一级目录，然后删除空文件夹
"""

import os
import shutil
import sys
from pathlib import Path
import time

try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

# 常见视频文件扩展名
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv', '.ts', '.mts', '.m2ts',
    '.rm', '.rmvb', '.asf', '.divx', '.vob', '.dat', '.f4v', '.swf'
}

def is_video_file(filename):
    """检查文件是否为视频文件"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in VIDEO_EXTENSIONS

def find_video_files(directory):
    """递归查找目录中的所有视频文件"""
    video_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if is_video_file(file):
                video_files.append((root, file))
    return video_files

def move_video_to_root(directory, root_path):
    """将视频文件移动到一级目录"""
    root = root_path[0]  # 文件所在的原始子目录
    file = root_path[1]
    source_path = os.path.join(root, file)
    target_path = os.path.join(directory, file)
    
    # 如果目标文件已存在，添加数字后缀
    counter = 1
    original_name, ext = os.path.splitext(file)
    while os.path.exists(target_path):
        new_name = f"{original_name}_{counter}{ext}"
        target_path = os.path.join(directory, new_name)
        counter += 1
    
    try:
        shutil.move(source_path, target_path)
        return True, target_path
    except Exception as e:
        return False, str(e)

def is_folder_empty(folder_path):
    """检查文件夹是否为空（不包含任何文件或子文件夹）"""
    if not os.path.exists(folder_path):
        return True
    
    # 检查文件夹中是否有任何内容
    with os.scandir(folder_path) as it:
        for entry in it:
            return False  # 如果找到任何条目，文件夹非空
    return True

def safe_delete_folder(folder_path, original_directory):
    """安全删除文件夹（检查是否为空且不是原始目录）"""
    if folder_path == original_directory:
        return False, "不能删除原始目录"
    
    if not os.path.exists(folder_path):
        return False, "文件夹不存在"
    
    if not is_folder_empty(folder_path):
        return False, "文件夹非空"
    
    try:
        os.rmdir(folder_path)
        return True, "删除成功"
    except Exception as e:
        return False, str(e)

def get_unique_folders(video_files):
    """从视频文件路径中提取唯一的文件夹"""
    folders = set()
    for root, file in video_files:
        folders.add(root)
    return sorted(folders, key=len, reverse=True)  # 从最深层的文件夹开始

def process_directory(directory):
    """处理指定目录"""
    print(f"\n正在处理目录: {directory}")
    print("=" * 50)
    
    # 步骤1：查找所有视频文件
    print("正在搜索视频文件...")
    video_files = find_video_files(directory)
    
    if not video_files:
        print("未找到视频文件！")
        return
    
    total_videos = len(video_files)
    print(f"找到 {total_videos} 个视频文件")
    
    # 步骤2：移动视频文件到一级目录
    print("\n正在移动视频文件...")
    moved_count = 0
    failed_moves = []
    
    for i, (root, file) in enumerate(video_files, 1):
        print(f"处理中: {file} ({i}/{total_videos})")
        success, result = move_video_to_root(directory, (root, file))
        
        if success:
            print(f"  ✓ 已移动到: {os.path.basename(result)}")
            moved_count += 1
        else:
            print(f"  ✗ 移动失败: {result}")
            failed_moves.append((file, result))
    
    # 步骤3：删除空文件夹
    print("\n正在删除空文件夹...")
    deleted_folders = []
    failed_deletes = []
    
    # 获取所有可能的父文件夹
    all_folders = get_unique_folders(video_files)
    
    for folder in all_folders:
        if folder == directory:
            continue  # 跳过原始目录
            
        success, message = safe_delete_folder(folder, directory)
        if success:
            print(f"  ✓ 删除文件夹: {os.path.relpath(folder, directory)}")
            deleted_folders.append(folder)
        else:
            if message != "文件夹非空":
                print(f"  ✗ 删除失败 ({os.path.relpath(folder, directory)}): {message}")
                failed_deletes.append((folder, message))
    
    # 步骤4：显示结果摘要
    print("\n" + "=" * 50)
    print("处理完成！")
    print(f"视频文件总数: {total_videos}")
    print(f"成功移动: {moved_count}")
    print(f"移动失败: {len(failed_moves)}")
    print(f"删除空文件夹: {len(deleted_folders)}")
    
    if failed_moves:
        print("\n移动失败的文件:")
        for file, error in failed_moves:
            print(f"  - {file}: {error}")
    
    if failed_deletes:
        print("\n删除失败的文件夹:")
        for folder, error in failed_deletes:
            print(f"  - {os.path.relpath(folder, directory)}: {error}")

def browse_directory_dialog():
    """使用 tkinter 弹出系统文件夹选择框"""
    root = tk.Tk()
    root.withdraw()           # 隐藏主窗口
    root.attributes('-topmost', True)  # 确保对话框在最前面
    folder = filedialog.askdirectory(title="选择要整理的视频目录")
    root.destroy()
    return folder if folder else None


def get_directory_from_user():
    """获取用户输入的目录"""
    print("\n" + "=" * 50)
    print("视频文件整理器")
    print("=" * 50)
    print("功能说明:")
    print("1. 递归查找指定目录下的所有视频文件")
    print("2. 将视频文件移动到一级目录")
    print("3. 删除空文件夹（仅当文件夹中无任何文件时）")
    print("=" * 50)
    
    while True:
        try:
            if HAS_TKINTER:
                print("\n正在打开文件夹选择窗口...")
                path = browse_directory_dialog()
                if path is None:
                    cont = input("未选择目录，输入 'exit' 退出，或按 Enter 重新选择: ").strip().lower()
                    if cont == 'exit':
                        return None
                    continue
            else:
                # 降级：手动输入
                print("\n请输入目录路径（或拖拽文件夹到终端窗口）:")
                path = input("目录: ").strip()
                
                if path.lower() == 'exit':
                    return None
                
                # 处理拖拽路径（可能包含引号）
                path = path.strip('"\'')
                
                if not path:
                    print("请输入有效的目录路径！")
                    continue
            
            if not os.path.exists(path):
                print(f"目录不存在: {path}")
                continue
                
            if not os.path.isdir(path):
                print(f"路径不是目录: {path}")
                continue
                
            return os.path.abspath(path)
            
        except KeyboardInterrupt:
            print("\n\n已取消操作")
            return None
        except Exception as e:
            print(f"发生错误: {e}")
            continue

def main():
    """主函数"""
    print("视频文件整理器 v1.0")
    print("按 Ctrl+C 退出程序\n")
    
    try:
        while True:
            directory = get_directory_from_user()
            
            if directory is None:
                print("\n感谢使用，再见！")
                break
                
            # 确认操作
            print(f"\n你选择的目录是: {directory}")
            confirm = input("确认开始整理？(y/n): ").strip().lower()
            
            if confirm != 'y':
                print("操作已取消")
                continue
                
            # 处理目录
            process_directory(directory)
            
            # 询问是否继续
            print("\n" + "=" * 50)
            cont = input("是否处理其他目录？(y/n): ").strip().lower()
            if cont != 'y':
                print("\n感谢使用，再见！")
                break
                
    except KeyboardInterrupt:
        print("\n\n程序已终止")
    except Exception as e:
        print(f"\n程序发生错误: {e}")
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()
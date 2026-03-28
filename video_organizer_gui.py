#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频文件整理器（GUI版本）
功能：将指定目录下的所有视频文件从其子文件夹移动到一级目录，然后删除空文件夹
"""

import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
import time

# 常见视频文件扩展名
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.m4v', '.mpg', '.mpeg', '.3gp', '.ogv', '.ts', '.mts', '.m2ts',
    '.rm', '.rmvb', '.asf', '.divx', '.vob', '.dat', '.f4v', '.swf'
}

class VideoOrganizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("视频文件整理器 v1.0")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        self.setup_ui()
        self.processing = False
        
    def setup_ui(self):
        # 标题
        title_label = tk.Label(
            self.root, 
            text="视频文件整理器", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # 说明标签
        desc_text = """功能说明：
1. 递归查找指定目录下的所有视频文件
2. 将视频文件移动到一级目录
3. 删除空文件夹（仅当文件夹中无任何文件时）"""
        
        desc_label = tk.Label(
            self.root, 
            text=desc_text, 
            font=("Arial", 10),
            justify=tk.LEFT,
            bg="#f8f9fa",
            padx=10,
            pady=10,
            relief=tk.GROOVE
        )
        desc_label.pack(pady=10, padx=20, fill=tk.X)
        
        # 目录选择区域
        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(dir_frame, text="选择目录:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.dir_var = tk.StringVar()
        dir_entry = tk.Entry(
            dir_frame, 
            textvariable=self.dir_var, 
            font=("Arial", 10),
            state='readonly'
        )
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            dir_frame,
            text="浏览...",
            command=self.browse_directory,
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            relief=tk.RAISED
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10, padx=20, fill=tk.X)
        
        # 状态文本
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        status_label.pack(pady=5)
        
        # 日志文本框
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(log_frame, text="处理日志:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.log_text = tk.Text(
            log_frame,
            height=10,
            font=("Consolas", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(
            button_frame,
            text="开始整理",
            command=self.start_processing,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=5,
            state='disabled'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="清空日志",
            command=self.clear_log,
            font=("Arial", 11),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=5
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(
            button_frame,
            text="退出",
            command=self.root.quit,
            font=("Arial", 11),
            bg="#95a5a6",
            fg="white",
            padx=20,
            pady=5
        )
        exit_btn.pack(side=tk.LEFT, padx=5)
        
    def browse_directory(self):
        directory = filedialog.askdirectory(title="选择要整理的目录")
        if directory:
            self.dir_var.set(directory)
            self.start_btn.config(state='normal')
            self.log_message(f"选择的目录: {directory}")
    
    def log_message(self, message):
        self.log_text.config(state='normal')
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def clear_log(self):
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        self.status_var.set("就绪")
        self.progress_var.set(0)
    
    def is_video_file(self, filename):
        """检查文件是否为视频文件"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in VIDEO_EXTENSIONS
    
    def find_video_files(self, directory):
        """递归查找目录中的所有视频文件"""
        video_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if self.is_video_file(file):
                    video_files.append((root, file))
        return video_files
    
    def is_folder_empty(self, folder_path):
        """检查文件夹是否为空（不包含任何文件或子文件夹）"""
        if not os.path.exists(folder_path):
            return True
        
        with os.scandir(folder_path) as it:
            for entry in it:
                return False
        return True
    
    def process_directory(self):
        """处理指定目录"""
        directory = self.dir_var.get()
        
        if not directory or not os.path.exists(directory):
            messagebox.showerror("错误", "请选择有效的目录！")
            return
        
        try:
            self.processing = True
            self.start_btn.config(state='disabled', text="处理中...")
            
            self.log_message(f"开始处理目录: {directory}")
            self.status_var.set("正在搜索视频文件...")
            
            # 步骤1：查找所有视频文件
            video_files = self.find_video_files(directory)
            
            if not video_files:
                self.log_message("未找到视频文件！")
                messagebox.showinfo("提示", "未找到视频文件！")
                return
            
            total_videos = len(video_files)
            self.log_message(f"找到 {total_videos} 个视频文件")
            
            # 步骤2：移动视频文件到一级目录
            self.status_var.set("正在移动视频文件...")
            moved_count = 0
            failed_moves = []
            
            for i, (root, file) in enumerate(video_files, 1):
                # 更新进度
                progress = (i / total_videos) * 50
                self.progress_var.set(progress)
                
                self.log_message(f"处理: {file}")
                
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
                    self.log_message(f"  ✓ 移动到: {os.path.basename(target_path)}")
                    moved_count += 1
                except Exception as e:
                    error_msg = str(e)
                    self.log_message(f"  ✗ 移动失败: {error_msg}")
                    failed_moves.append((file, error_msg))
            
            # 步骤3：删除空文件夹
            self.status_var.set("正在删除空文件夹...")
            deleted_folders = []
            failed_deletes = []
            
            # 获取所有可能的父文件夹
            folders = set()
            for root, file in video_files:
                folders.add(root)
            
            folders = sorted(folders, key=len, reverse=True)
            
            for j, folder in enumerate(folders):
                if folder == directory:
                    continue
                
                # 更新进度
                progress = 50 + (j / len(folders)) * 50
                self.progress_var.set(progress)
                
                if not self.is_folder_empty(folder):
                    continue
                
                try:
                    os.rmdir(folder)
                    self.log_message(f"  ✓ 删除空文件夹: {os.path.relpath(folder, directory)}")
                    deleted_folders.append(folder)
                except Exception as e:
                    error_msg = str(e)
                    self.log_message(f"  ✗ 删除失败 ({os.path.relpath(folder, directory)}): {error_msg}")
                    failed_deletes.append((folder, error_msg))
            
            # 完成
            self.progress_var.set(100)
            self.status_var.set("处理完成")
            
            # 显示结果
            result_msg = f"""处理完成！
            
视频文件总数: {total_videos}
成功移动: {moved_count}
移动失败: {len(failed_moves)}
删除空文件夹: {len(deleted_folders)}
            
请查看日志了解详细信息。"""
            
            self.log_message("=" * 50)
            self.log_message("处理完成！")
            self.log_message(f"视频文件总数: {total_videos}")
            self.log_message(f"成功移动: {moved_count}")
            self.log_message(f"移动失败: {len(failed_moves)}")
            self.log_message(f"删除空文件夹: {len(deleted_folders)}")
            
            messagebox.showinfo("完成", result_msg)
            
        except Exception as e:
            self.log_message(f"处理过程中发生错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")
        finally:
            self.processing = False
            self.start_btn.config(state='normal', text="开始整理")
            self.status_var.set("就绪")
    
    def start_processing(self):
        """在单独的线程中开始处理"""
        if self.processing:
            return
        
        # 确认操作
        confirm = messagebox.askyesno(
            "确认", 
            "开始整理视频文件吗？\n\n注意：此操作会移动文件和删除空文件夹。"
        )
        
        if not confirm:
            return
        
        # 在后台线程中运行处理
        thread = threading.Thread(target=self.process_directory)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = VideoOrganizerGUI(root)
    
    # 居中显示窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
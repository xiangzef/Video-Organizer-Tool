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
3. 删除空文件夹（仅当文件夹中无任何文件时）
4. 批量删除不含视频文件的文件夹
5. 整理单片文件夹（仅含1个视频且无子文件夹的一级目录）"""
        
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
        
        self.delete_empty_btn = tk.Button(
            button_frame,
            text="删除无视频文件夹",
            command=self.start_delete_empty_folders,
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            padx=20,
            pady=5,
            state='disabled'
        )
        self.delete_empty_btn.pack(side=tk.LEFT, padx=5)

        self.single_video_btn = tk.Button(
            button_frame,
            text="整理单片文件夹",
            command=self.start_move_single_video_folders,
            font=("Arial", 11, "bold"),
            bg="#8e44ad",
            fg="white",
            padx=20,
            pady=5,
            state='disabled'
        )
        self.single_video_btn.pack(side=tk.LEFT, padx=5)
        
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
            self.delete_empty_btn.config(state='normal')
            self.single_video_btn.config(state='normal')
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
    
    def folder_contains_video(self, folder_path):
        """检查文件夹（含子文件夹）中是否包含视频文件"""
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if self.is_video_file(file):
                    return True
        return False

    def find_folders_without_videos(self, directory):
        """查找指定目录下所有不含视频文件的子文件夹"""
        result = []
        for root, dirs, files in os.walk(directory, topdown=False):
            if root == directory:
                continue
            has_video = any(self.is_video_file(f) for f in files)
            if not has_video:
                result.append(root)
        return sorted(result, key=len, reverse=True)

    def process_delete_empty_folders(self):
        """删除不含视频文件的文件夹（在线程中执行）"""
        directory = self.dir_var.get()

        if not directory or not os.path.exists(directory):
            messagebox.showerror("错误", "请选择有效的目录！")
            return

        try:
            self.processing = True
            self.delete_empty_btn.config(state='disabled', text="处理中...")
            self.start_btn.config(state='disabled')

            self.log_message(f"开始扫描目录: {directory}")
            self.status_var.set("正在扫描无视频文件夹...")

            candidates = self.find_folders_without_videos(directory)

            if not candidates:
                self.log_message("未找到不含视频文件的文件夹。")
                messagebox.showinfo("提示", "未找到不含视频文件的文件夹！")
                return

            total = len(candidates)
            self.log_message(f"找到 {total} 个不含视频文件的文件夹")
            for folder in candidates:
                self.log_message(f"  - {os.path.relpath(folder, directory)}")

            # 弹确认框（在主线程中需通过 after 调用，这里直接用 messagebox）
            confirm = messagebox.askyesno(
                "确认删除",
                f"即将删除 {total} 个不含视频文件的文件夹（包含其中所有内容）。\n\n此操作不可恢复，确认继续？"
            )
            if not confirm:
                self.log_message("操作已取消。")
                return

            self.status_var.set("正在删除...")
            deleted, failed = [], []

            for i, folder in enumerate(candidates, 1):
                self.progress_var.set(i / total * 100)
                if not os.path.exists(folder):
                    continue
                if folder == directory:
                    continue
                try:
                    shutil.rmtree(folder)
                    rel = os.path.relpath(folder, directory)
                    self.log_message(f"  ✓ 已删除: {rel}")
                    deleted.append(folder)
                except Exception as e:
                    rel = os.path.relpath(folder, directory)
                    self.log_message(f"  ✗ 删除失败 ({rel}): {e}")
                    failed.append((folder, str(e)))

            self.progress_var.set(100)
            self.status_var.set("处理完成")
            self.log_message("=" * 50)
            self.log_message(f"删除完成！成功: {len(deleted)}，失败: {len(failed)}")
            messagebox.showinfo("完成", f"删除完成！\n\n成功删除: {len(deleted)} 个文件夹\n失败: {len(failed)} 个")

        except Exception as e:
            self.log_message(f"处理过程中发生错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")
        finally:
            self.processing = False
            self.delete_empty_btn.config(state='normal', text="删除无视频文件夹")
            self.start_btn.config(state='normal')
            self.status_var.set("就绪")

    def start_delete_empty_folders(self):
        """在独立线程中启动删除操作"""
        if self.processing:
            return
        thread = threading.Thread(target=self.process_delete_empty_folders)
        thread.daemon = True
        thread.start()

    def analyze_single_video_folders(self, directory):
        """
        分析根目录下的一级子文件夹，找出「仅含1个视频文件且无子文件夹」的文件夹。
        返回列表，每项为 (folder_path, video_filename)
        """
        results = []
        try:
            entries = list(os.scandir(directory))
        except Exception:
            return results

        for entry in entries:
            if not entry.is_dir():
                continue
            folder_path = entry.path
            try:
                children = list(os.scandir(folder_path))
            except Exception:
                continue

            # 有子文件夹 → 跳过
            if any(c.is_dir() for c in children):
                continue

            # 统计视频文件
            videos = [c.name for c in children if c.is_file() and self.is_video_file(c.name)]

            if len(videos) == 1:
                results.append((folder_path, videos[0]))

        return results

    def process_move_single_video_folders(self):
        """整理单片文件夹（在线程中执行）"""
        directory = self.dir_var.get()

        if not directory or not os.path.exists(directory):
            messagebox.showerror("错误", "请选择有效的目录！")
            return

        try:
            self.processing = True
            self.single_video_btn.config(state='disabled', text="处理中...")
            self.start_btn.config(state='disabled')
            self.delete_empty_btn.config(state='disabled')

            self.log_message(f"开始扫描目录: {directory}")
            self.status_var.set("正在扫描单片文件夹...")

            candidates = self.analyze_single_video_folders(directory)

            if not candidates:
                self.log_message("未找到符合条件的文件夹（一级子文件夹仅含1个视频且无子文件夹）。")
                messagebox.showinfo("提示", "未找到符合条件的单片文件夹！")
                return

            total = len(candidates)
            self.log_message(f"找到 {total} 个符合条件的文件夹：")
            for folder, video in candidates:
                rel = os.path.relpath(folder, directory)
                self.log_message(f"  {rel}  →  {video}")

            confirm = messagebox.askyesno(
                "确认整理",
                f"即将把 {total} 个文件夹中的视频移到根目录，并删除对应文件夹。\n\n此操作不可恢复，确认继续？"
            )
            if not confirm:
                self.log_message("操作已取消。")
                return

            self.status_var.set("正在移动...")
            moved, failed = [], []

            for i, (folder, video) in enumerate(candidates, 1):
                self.progress_var.set(i / total * 100)

                src = os.path.join(folder, video)
                dst = os.path.join(directory, video)

                # 目标重名处理
                if os.path.exists(dst):
                    base, ext = os.path.splitext(video)
                    counter = 1
                    while os.path.exists(dst):
                        dst = os.path.join(directory, f"{base}_{counter}{ext}")
                        counter += 1

                rel_folder = os.path.relpath(folder, directory)
                try:
                    shutil.move(src, dst)
                    self.log_message(f"  ✓ 移动: {video}  (从 {rel_folder})")
                    # 删除现在应为空的文件夹
                    if not os.listdir(folder):
                        os.rmdir(folder)
                        self.log_message(f"  ✓ 删除: {rel_folder}")
                    moved.append(video)
                except Exception as e:
                    self.log_message(f"  ✗ 失败 ({video}): {e}")
                    failed.append((video, str(e)))

            self.progress_var.set(100)
            self.status_var.set("处理完成")
            self.log_message("=" * 50)
            self.log_message(f"整理完成！成功: {len(moved)}，失败: {len(failed)}")
            messagebox.showinfo("完成", f"整理完成！\n\n成功移动: {len(moved)} 个视频\n失败: {len(failed)} 个")

        except Exception as e:
            self.log_message(f"处理过程中发生错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")
        finally:
            self.processing = False
            self.single_video_btn.config(state='normal', text="整理单片文件夹")
            self.start_btn.config(state='normal')
            self.delete_empty_btn.config(state='normal')
            self.status_var.set("就绪")

    def start_move_single_video_folders(self):
        """在独立线程中启动整理单片文件夹操作"""
        if self.processing:
            return
        thread = threading.Thread(target=self.process_move_single_video_folders)
        thread.daemon = True
        thread.start()

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
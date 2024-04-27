import tkinter as tk
from tkinter import ttk

from ttkbootstrap import Style

'''
GitHub: https://github.com/hehe11MC/Python
'''


# 创建一个名为Calculator的类
class Calculator:
    # 初始化Calculator类的实例
    def __init__(self):
        # 创建一个Tkinter根窗口
        self.root = tk.Tk()
        self.root.title("Calculator")  # 设置窗口标题为"Calculator"
        self.root.geometry("400x320")  # 设置窗口大小为400x320
        self.style = Style(theme='flatly')  # 创建一个样式实例
        self.expression = ""  # 初始化表达式为空字符串
        self.result_var = tk.StringVar()  # 创建一个Tkinter字符串变量
        # 创建一个文本框，用于显示表达式和计算结果
        self.display = ttk.Entry(self.root, textvariable=self.result_var, font=('Arial', 20), justify="right")
        self.display.pack(fill="x", padx=10, pady=10)  # 将文本框放置在窗口中
        self.button_frame = ttk.Frame(self.root)  # 创建一个框架，用于放置按钮
        self.button_frame.pack(padx=10, pady=10, side="bottom")  # 将框架放置在窗口底部
        # 定义按钮的文本和位置
        buttons = [
            ("C", 0, 0), ("⌫", 0, 1), ("x²", 0, 2), ("√", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3)
        ]
        # 创建按钮并放置在框架中
        for (text, row, col) in buttons:
            button = ttk.Button(self.button_frame, text=text, style='Primary.TButton',
                                command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        # 配置框架的行和列权重，使按钮在窗口大小变化时能够等比放大缩小
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
            self.button_frame.grid_columnconfigure(i, weight=1)
        # 绑定窗口大小变化事件到对应的方法
        self.root.bind("<Configure>", self.on_window_resize)

    # 处理按钮点击事件的方法
    def on_button_click(self, text):
        pass  # 点击按钮的具体处理逻辑待实现

    # 处理窗口大小变化事件的方法
    def on_window_resize(self, event):
        # 计算每个按钮的新宽度
        new_button_width = event.width // 4
        # 设置每个按钮的宽度为新宽度
        for child in self.button_frame.winfo_children():
            child.config(width=new_button_width)


# 若作为独立脚本运行，则创建Calculator实例并显示窗口
if __name__ == "__main__":
    calculator = Calculator()
    calculator.root.mainloop()

from tkinter import *
import time

'''
GitHub: https://github.com/hehe11MC/Python
'''

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title('Clock')
        self.root.configure(bg='black')

        self.localtime = StringVar()

        self.time_label = Label(self.root, textvariable=self.localtime, fg='white', bg='black', font=('Arial',80))
        self.time_label.pack()

        self.get_time()

        self.root.mainloop()

    def get_time(self):
        self.localtime.set(time.strftime("%H:%M:%S"))   # 获取当前时间并更新到界面上
        self.root.after(1000, self.get_time)    # 每隔一秒调用一次get_time方法更新时间


if __name__ == '__main__':
    Main()

import tkinter as tk
from PIL import Image, ImageTk
import cv2

'''
GitHub: https://github.com/hehe11MC/Python
'''


class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.resizable(0, 0)

        # 打开默认摄像头
        self.cap = cv2.VideoCapture(0)

        # 检查摄像头是否成功打开
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        # 获取摄像头属性
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 创建一个画布来显示视频帧
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        # 捕获视频帧并在Tkinter窗口中显示它们
        self.update()

        # 将关闭事件绑定到释放摄像头并关闭窗口
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update(self):
        # 逐帧捕获
        ret, frame = self.cap.read()

        if ret:
            # 将帧转换为RGB格式
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 将帧转换为ImageTk格式
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # 用新帧更新画布
            self.canvas.img = img_tk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

        # 在10毫秒后调度下一次更新
        self.window.after(10, self.update)

    def on_close(self):
        # 释放摄像头并关闭窗口
        self.cap.release()
        self.window.destroy()

def main():
    # 创建一个Tkinter窗口
    root = tk.Tk()

    # 创建CameraApp类的一个实例
    app = CameraApp(root, "Tkinter & OpenCV")

    # 运行Tkinter事件循环
    root.mainloop()

if __name__ == "__main__":
    main()

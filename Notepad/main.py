import os
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import webbrowser


class Notepad:
    def __init__(self):
        self.root = Tk()
        self.root.title('TkNotepad - Untitled')
        self.root.geometry('700x500')

        self.file_text = ""

        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File菜单
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='New File', accelerator='Ctrl+N', command=self.new_file)
        file_menu.add_command(label='Open...', accelerator='Ctrl+O', command=self.open_file)
        self.recent_files_menu = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label='Recent Files', menu=self.recent_files_menu)
        file_menu.add_separator()
        file_menu.add_command(label='Save', accelerator='Ctrl+S', command=self.save_file)
        file_menu.add_command(label='Save As...', accelerator='Ctrl+Shift+S', command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='Close Window', accelerator='Alt+F4')
        file_menu.add_command(label='Exit', command=self.exit_app)
        menubar.add_cascade(label='File', menu=file_menu)

        # Edit菜单
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo)
        edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut)
        edit_menu.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy)
        edit_menu.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label='Select All', accelerator='Ctrl+A', command=self.select_all)
        edit_menu.add_command(label='Select Line', accelerator='Ctrl+L', command=self.select_line)
        edit_menu.add_separator()
        edit_menu.add_command(label='Go to Line', accelerator='Ctrl+G', command=self.go_to_line)
        menubar.add_cascade(label='Edit', menu=edit_menu)

        # Help菜单
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Github', command=lambda: webbrowser.open('https://github.com/hehe11MC/Python'))
        help_menu.add_command(label='About', command=self.about)
        menubar.add_cascade(label='Help', menu=help_menu)

        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)

        # 文本区域
        self.text_area = Text(main_frame, font=('Arial', 11), undo=True)
        self.text_area.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(main_frame, command=self.text_area.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        status_bar = Label(self.root, text='Ln: 1, Col: 0', bd=1, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)

        # 更新状态栏
        def update_status_bar(event=None):
            line, column = self.text_area.index('insert').split('.')
            status_bar.config(text=f'Ln: {line}, Col: {column}')

        self.text_area.bind('<KeyRelease>', update_status_bar)
        self.text_area.bind('<ButtonRelease>', update_status_bar)

        self.recent_files_path = "./tknotepad/recent_files.txt"
        self.recent_files = []

        # 加载Recent Files
        self.load_recent_files()

        self.update_recent_files_submenu()

        # 绑定快捷键
        self.root.bind_all('<Control-n>', lambda event: self.new_file())
        self.root.bind_all('<Control-o>', lambda event: self.open_file())
        self.root.bind_all('<Control-s>', lambda event: self.save_file())
        self.root.bind_all('<Control-Shift-S>', lambda event: self.save_as_file())
        self.root.bind_all('<Control-a>', lambda event: self.select_all())
        self.root.bind_all('<Control-l>', lambda event: self.select_line())
        self.root.bind_all('<Control-g>', lambda event: self.go_to_line())

        self.root.mainloop()

    def exit_app(self):
        if self.check_save_changes():
            self.root.destroy()

    def check_save_changes(self):
        if self.root.title() == 'TkNotepad - Untitled' and self.text_area.get(1.0, END).strip() != "":
            save_changes = messagebox.askyesnocancel('Save Changes', 'Do you want to save the changes?')
            if save_changes is None:
                return False
            elif save_changes:
                self.save_file()
        elif self.root.title() != 'TkNotepad - Untitled' and self.text_area.get(1.0, END) != self.file_text:
            save_changes = messagebox.askyesnocancel('Save Changes', 'Do you want to save the changes?')
            if save_changes is None:
                return False
            elif save_changes:
                self.save_file()
        return True

    def new_file(self):
        if self.check_save_changes():
            self.text_area.delete(1.0, END)
            self.root.title('TkNotepad - Untitled')

    def open_file(self):
        if self.check_save_changes():
            file_path = filedialog.askopenfilename(title='Open',
                                                   filetypes=[('All Files', '*.*'), ('Text Files', '*.txt'),
                                                              ('Python Files', '*.py')])
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.delete(1.0, END)
                    self.text_area.insert(1.0, file.read())
                    self.file_text = self.text_area.get(1.0, END)
                self.root.title(f'TkNotepad - {file_path}')
                self.update_recent_files(file_path)

    def load_recent_files(self):
        if os.path.exists(self.recent_files_path):
            with open(self.recent_files_path, 'r') as file:
                self.recent_files = [line.strip() for line in file.readlines()]

    def save_recent_files(self):
        with open(self.recent_files_path, 'w') as file:
            for recent_file in self.recent_files:
                file.write(recent_file + "\n")

    def update_recent_files_submenu(self):
        for idx, file_path in enumerate(self.recent_files[:15], start=1):
            self.recent_files_menu.add_command(label=f"{idx}. {file_path}",
                                               command=lambda path=file_path: self.open_recent_file(path))

    def update_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:15]
        self.save_recent_files()
        self.recent_files_menu.delete(0, 'end')
        self.update_recent_files_submenu()

    def open_recent_file(self, file_path):
        if self.check_save_changes():
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text_area.delete(1.0, END)
                self.text_area.insert(1.0, file.read())
                self.file_text = self.text_area.get(1.0, END)  # Update file_text
            self.root.title(f'TkNotepad - {file_path}')

    def save_file(self):
        if self.root.title() == 'TkNotepad - Untitled':
            self.save_as_file()
        else:
            file_path = self.root.title().replace('TkNotepad - ', '')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, END))
            self.file_text = self.text_area.get(1.0, END)  # Update file_text

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(title='Save As', defaultextension='.txt',
                                                 filetypes=[('All Files', '*.*'), ('Text Files', '*.txt'),
                                                            ('Python Files', '*.py')])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, END))
            self.root.title(f'TkNotepad - {file_path}')
            self.file_text = self.text_area.get(1.0, END)

    def undo(self):
        self.text_area.event_generate('<<Undo>>')

    def redo(self):
        self.text_area.event_generate('<<Redo>>')

    def cut(self):
        self.text_area.event_generate('<<Cut>>')

    def copy(self):
        self.text_area.event_generate('<<Copy>>')

    def paste(self):
        self.text_area.event_generate('<<Paste>>')

    def select_all(self):
        self.text_area.event_generate('<<SelectAll>>')

    def select_line(self):
        self.text_area.tag_add('sel', 'insert linestart', 'insert lineend+1c')

    def go_to_line(self):
        max_line = int(self.text_area.index('end-1c').split('.')[0])
        line_num = simpledialog.askinteger("Go to Line", "Enter line number:", parent=self.root, minvalue=1,
                                           maxvalue=max_line)
        if line_num is not None:
            self.text_area.mark_set("insert", f"{line_num}.0")
            self.text_area.see(f"{line_num}.0")
            self.text_area.focus_set()

    def about(self):
        messagebox.showinfo('About', 'TkNotepad\n\nA simple text editor written in Python using the tkinter library.\nVersion 1.0\nCreated by Xiaoqing')


if __name__ == '__main__':
    Notepad()

import tkinter as tk
import re


def highlight_syntax(event=None):
    text.tag_remove("keyword", "1.0", "end")
    text.tag_remove("comment", "1.0", "end")
    text.tag_remove("string", "1.0", "end")
    keywords = ["if", "else", "for", "while", "def", "class", "import", "from", "as", "return", "True", "False"]
    for keyword in keywords:
        match_indices = [(match.start(), match.end()) for match in
                         re.finditer(r"\b{}\b".format(keyword), text.get("1.0", "end"))]
        for start, end in match_indices:
            text.tag_add("keyword", "1.0+{}c".format(start), "1.0+{}c".format(end))

    comment_indices = [(match.start(), match.end()) for match in
                       re.finditer(r"#.*$", text.get("1.0", "end"), re.MULTILINE)]
    for start, end in comment_indices:
        text.tag_add("comment", "1.0+{}c".format(start), "1.0+{}c".format(end))

    string_indices = [(match.start(), match.end()) for match in re.finditer(r"(['\"])(.*?)\1", text.get("1.0", "end"))]
    for start, end in string_indices:
        text.tag_add("string", "1.0+{}c".format(start), "1.0+{}c".format(end))


root = tk.Tk()
root.title("Syntax Highlighter")

text = tk.Text(root, wrap="word", font=("Arial", 12), undo=True)
text.pack(fill="both", expand=True)

text.bind("<KeyRelease>", highlight_syntax)

text.tag_configure("keyword", foreground="blue")
text.tag_configure("comment", foreground="gray")
text.tag_configure("string", foreground="green")

root.mainloop()

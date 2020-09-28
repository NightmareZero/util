from tkinter import *
from typing import Optional


class AppRun:
    def __init__(self):
        pass

    pass


class AppGui:
    def __init__(self):
        self.window = self.gen_window()
        self.txt_server: Optional[Entry] = None
        self.txt_interval: Optional[Entry] = None
        self.txt_log: Optional[Text] = None

    def start(self):
        self.gen_content()
        self.window.mainloop()

    @staticmethod
    def gen_window() -> Tk:
        """
        生成主窗体
        :return:
        """
        gui: Tk = Tk()
        gui.wm_title("测试")
        gui.wm_geometry("800x600")
        gui.grid_anchor("center")
        return gui

    def gen_content(self):
        # ========== line 1 ===============
        line1 = Frame(self.window, height=200)
        line1.pack(fill="both")
        self.gen_conf(line1)
        self.gen_ctrl(line1)
        # ========== line 2 ===============
        line2 = Frame(self.window, height=200)
        line2.pack(fill="both", expand="yes")
        self.gen_log(line2)

    def gen_conf(self, parent) -> Widget:
        """
        生成左侧操作框
        :param parent:
        :return:
        """
        root = LabelFrame(parent, text="配置信息")
        root.pack(in_=parent, fill="both", side="left", anchor="ne",
                  expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
        # ====== line 1
        line1 = Frame(root)
        line1.pack(in_=root, fill="x", padx="10")
        label1 = Label(master=line1, text="地址")
        label1.pack(in_=line1, side="left", anchor="nw")
        self.txt_server = Entry(master=line1, width=60)
        self.txt_server.pack(in_=line1, side="right", anchor="ne")
        # ====== line 2
        line2 = Frame(root)
        line2.pack(in_=root, fill="x", padx="10")
        label2 = Label(master=line2, text="设置1")
        label2.pack(in_=line2, side="left", anchor="nw")
        self.txt_interval = Entry(master=line2, text="30", width=60)
        self.txt_interval.pack(in_=line2, side="right", anchor="ne")
        # ====== line 3
        line3 = Frame(root)
        line3.pack(in_=root, fill="x", padx=10)
        label3 = Label(master=line3, text="设置2")
        label3.pack(in_=line3, side="left", anchor="nw")
        text3 = Entry(master=line3, text="30", width=60)
        text3.pack(in_=line3, side="right", anchor="ne")
        return root

    @staticmethod
    def gen_ctrl(parent) -> Widget:
        root = LabelFrame(parent, text="操作", width=200, height=200)
        root.pack(in_=parent, fill="y", side="right", anchor="nw",
                  padx=5, pady=5, ipadx=5, ipady=5)
        # line1
        line1 = Frame()
        line1.pack(in_=root, fill="x", padx=10)
        btn11 = Button(line1, text="按钮1")
        btn11.pack(in_=line1, side="left", anchor="nw",padx=5)
        btn12 = Button(line1, text="按钮2")
        btn12.pack(in_=line1, side="left", anchor="n",padx=5)
        return root

    def gen_log(self, parent) -> Widget:
        root = LabelFrame(self.window, text="日志输出")
        root.pack(in_=parent, fill="both", anchor="se", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
        self.txt_log = Text(root)
        self.txt_log.place(in_=root, relwidth=0.99, relheight=0.99)
        return root


if __name__ == '__main__':
    AppGui().start()

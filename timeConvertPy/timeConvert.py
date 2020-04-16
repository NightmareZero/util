#!/usr/bin/env python
import sys
import time
# noinspection PyProtectedMember
from argparse import ArgumentParser, Namespace, _SubParsersAction
from time import struct_time

description = "trans time and str"


class TransInvoker:
    TIME_TO_STR = 1
    STR_TO_TIME = 2

    def __init__(self, **kw):
        self.date: str = kw.get('date')  # 输入日期
        self.time: str = kw.get('time')  # 输入时间
        self.cmd: str = kw.get('cmd')  # 执行命令
        self.time_num: int = kw.get('time_num')  # 数字格式时间
        self.use_second: bool = kw.get('second')  # 使用毫秒作为时间
        self.date_only: bool = kw.get('date_only')  # 仅包含日期
        self.run_method: int = \
            TransInvoker.STR_TO_TIME if self.cmd == "s" else TransInvoker.TIME_TO_STR  # 运行模式

    def do_run(self):
        """
        开始执行.

        :return: None
        """
        if self.run_method == self.TIME_TO_STR:
            self._do_time_to_str()
        elif self.run_method == self.STR_TO_TIME:
            self._do_str_to_time()

    def _do_time_to_str(self):
        """
        生成字符串格式日期
        """
        it_time = float(self.time_num) \
            if self.use_second is True \
            else float(self.time_num) / 1000.0
        localtime: struct_time = time.localtime(it_time)
        if self.date_only is False:
            showtime: str = time.strftime("%Y-%m-%d %H:%M:%S", localtime)
            print(showtime)
        else:
            showtime: str = time.strftime("%Y-%m-%d", localtime)
            print(showtime)

    def _do_str_to_time(self):
        """
        生成long数字类型日期
        """
        localtime: struct_time
        if self.date_only is True:
            localtime = time.strptime(self.date, "%Y-%m-%d")
        else:
            localtime = time.strptime(self.date + " " + self.time, "%Y-%m-%d %H:%M:%S")
        if self.use_second is True:
            print(int(time.mktime(localtime)))
        else:
            print(int(time.mktime(localtime) * 1000))


def genParser() -> ArgumentParser:
    """
    生成程序需要的代码分析器

    :return: 生成的分析器
    """
    pp = ArgumentParser(description=description, usage=description)
    setOptionArg(pp)  # 设置主程序参数
    subparsers: _SubParsersAction = pp.add_subparsers(title="sub command", dest="cmd", description="子命令")
    injStrToTimeParser(subparsers)  # 注入子分析器 (字符串转时间)
    injTimeToStrParser(subparsers)  # 注入子分析器 (时间转字符串)

    return pp


def setOptionArg(pp: ArgumentParser):
    pp.add_argument("-d", dest="day_only", action="store_true")
    pp.add_argument("-s", dest="use_second", action="store_true")
    pass


def injTimeToStrParser(p: _SubParsersAction):
    """
    添加子命令 (时间转字符串)

    :param p:
    """
    pp: ArgumentParser = p.add_parser(name="t")
    pp.description = "time to str"
    pp.add_argument("time_num", help="long type number")


def injStrToTimeParser(p: _SubParsersAction):
    """
    添加子命令 (字符串转时间)

    :param p:
    """
    pp: ArgumentParser = p.add_parser("s")
    pp.description = "str to time"
    pp.add_argument("date", action="store", type=str, help="date %%Y-%%m-%%d")
    pp.add_argument("time", nargs="?", action="store", default="", help="time %%H:%%M:%%S")


def parseInput(nn: Namespace) -> TransInvoker:
    """
    分析用户入参

    :param nn: 入参容器
    :return: 分析过的入参容器
    """
    if nn.cmd == 's':
        return TransInvoker(date=nn.date, time=nn.time, cmd=nn.cmd,
                            date_only=nn.day_only, second=nn.use_second)
    elif nn.cmd == 't':
        return TransInvoker(date_only=nn.day_only, second=nn.use_second, cmd=nn.cmd,
                            time_num=nn.time_num)


if __name__ == '__main__':
    parser: ArgumentParser = genParser()  # 生成分析器
    parse_input: TransInvoker = parseInput(parser.parse_args(sys.argv[1:]))
    if not parse_input:
        print("error, use " + sys.argv[0] + " -h to get help")
        exit(1)
    parse_input.do_run()
    pass

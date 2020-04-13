import sys
# noinspection PyProtectedMember
from argparse import ArgumentParser, Namespace, _SubParsersAction

description = "trans time and str"


def genParser() -> ArgumentParser:
    """
    生成程序需要的代码分析器

    :return: 生成的分析器
    """
    pp = ArgumentParser(description=description, usage=description)
    subparsers: _SubParsersAction = pp.add_subparsers(title="sub command", dest="son", description="子命令")
    injStrToTimeParser(subparsers)  # 注入子分析器 (字符串转时间)
    injTimeToStrParser(subparsers)  # 注入子分析器 (时间转字符串)

    return pp


def setOptionArg(pp: ArgumentParser):
    pass


def injTimeToStrParser(p: _SubParsersAction):
    """
    添加子命令 (时间转字符串)

    :param p:
    """
    pp: ArgumentParser = p.add_parser(name="t")
    pp.description = "time to str"


def injStrToTimeParser(p: _SubParsersAction):
    """
    添加子命令 (字符串转时间)

    :param p:
    """
    # p.add_subparsers(dest="s", description="字符串转时间")
    pp: ArgumentParser = p.add_parser("s")
    pp.allow_abbrev = True
    pp.description = "str to time"
    pp.add_argument("date", action="store", type=str, help="date %%Y-%%m-%%d")
    pp.add_argument("time", nargs="?", action="store", default="", help="time %%H:%%M:%%S")


if __name__ == '__main__':
    parser: ArgumentParser = genParser()
    nn: Namespace = parser.parse_args(sys.argv[1:])

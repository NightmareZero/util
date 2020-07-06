from typing import List, Dict, Type


class DictType:
    def __init__(self,
                 cls: Type,
                 is_list=True):
        self.is_list = is_list
        self.cls = cls


class ToDict:
    __dict_ignore__: List[str] = []

    __dict_mapping__: Dict[str, str] = []

    __dict_typing__: Dict[str, DictType] = {}

    def to_dict(self, ignore_none=False) -> dict:
        """
        将 obj 转换为 dict
        :param ignore_none: 忽略 none 字段
        :return: dict
        """
        return ToDict._to_dict(self, ignore_none)

    def from_dict(self, it_dict: dict) -> dict:
        """
        将 dict 转换为 obj
        :param it_dict: 字典数据
        :return: 未使用的字段
        """
        self._gen_reverse_mapping()
        return ToDict._from_dict(self, it_dict)

    def _gen_reverse_mapping(self) -> None:
        """
        生成逆映射列表
        :return: None
        """
        if not hasattr(self.__class__, '__reverse_dict_mapping__') and \
                len(self.__class__.__dict_mapping__) > 0:
            self.__class__.__reverse_dict_mapping__ = {}
            for (k, v) in self.__class__.__dict_mapping__:
                self.__class__.__reverse_dict_mapping__[v] = k

    @staticmethod
    def _can_to_dict(obj) -> bool:
        """
        验证是否是子类
        :param obj: .
        :return: .
        """
        return issubclass(obj, ToDict)

    @staticmethod
    def _from_dict(obj, it_dict: dict) -> dict:
        """
        dict 转 obj，实现
        :param obj: 实体
        :param it_dict: 字典
        :return: 未使用的字段
        """
        # 不继承本类, 不能转换
        if not ToDict._can_to_dict(obj):
            return obj
        unused = {}  # 未使用的字段
        for (key, value) in it_dict.items():
            # 忽略的字段
            if key in ToDict.__dict_ignore__:
                continue
            # 仅在 it_dict 存在的字段
            if not hasattr(obj, key):
                unused[key] = value
                continue
            # === 转换流程 ===
            attr: ToDict = getattr(obj, key)
            if ToDict._can_to_dict(attr):  # obj
                setattr(obj, key, attr.from_dict(value))
            elif isinstance(value, list):  # list
                if key not in ToDict.__dict_typing__:
                    unused[key] = value
                    continue
                setattr(obj, key, [])
                for v in value:
                    new_obj: Type = ToDict.__dict_typing__[key].cls()
                    obj[key].append(ToDict._from_dict(new_obj, v))
            else:  # 普通字段
                setattr(obj, key, value)
            pass

        return unused

    @staticmethod
    def _to_dict(i_obj, ignore_none=False, ignore_private=True):
        """
        obj 转 dict, 实现
        :param i_obj: 实体
        :param ignore_none: 忽略空字段?
        :param ignore_private:  忽略私有字段?
        :return:
        """
        # 不继承本类, 不能转换
        if not ToDict._can_to_dict(i_obj):
            return i_obj
        ret = {}  # 结果收集
        fields = i_obj.__dict__
        for (key, value) in fields.items():
            # 跳过私有字段
            if key.startswith('_') and ignore_private:
                continue
            # 跳过忽略字段
            if key in ToDict.__dict_ignore__:
                continue
            # 跳过空字段
            if ignore_none and value is None:
                continue
            # === 转换流程 === (分为 obj list 和 普通字段 )
            if ToDict._can_to_dict(value):  # obj
                ret[key] = value.to_dict()
            elif isinstance(value, list):  # list
                lst = []
                for i in value:
                    lst.append(ToDict._to_dict(i))
                ret[key] = lst
            else:  # 普通字段
                ret[key] = value
            # 字段重命名
            if key in ToDict.__dict_mapping__:
                ret[ToDict.__dict_mapping__[key]] = ret.pop(key)
        return ret

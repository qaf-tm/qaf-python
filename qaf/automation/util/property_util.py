import json
import os
import random
import re
import string


class PropretyUtil(dict):
    def __init__(self, name=None):
        self.name = name
        super(PropretyUtil, self).__init__()

    def load(self, file):
        extension = os.path.splitext(file)[1]
        if extension in ('.properties', '.loc', '.wsc', '.ini'):
            with open(file, 'r', encoding='UTF-8') as file:
                while line := file.readline():
                    kv = line.strip()
                    if kv and not kv.startswith("#"):
                        while kv.endswith("\\"):
                            kv = kv[:-1]
                            part = file.readline().strip()
                            if part and not part.startswith("#"):
                                kv = kv + part

                        kv = kv.split("=", 1)
                        if len(kv) == 2:
                            self.set_property(key=kv[0].strip(), value=kv[1].strip())
        elif extension in ('.wscj', '.locj'):
            with open(file, 'r', encoding='UTF-8') as json_file:
                data = json.load(json_file)
                for key, value in data.items():
                    self.set_property(key=key, value=json.dumps(value))

    def get_string(self, key):
        return ""

    def set_property(self, key, value):
        self.__dict__.__setitem__(key, value)

    def get_property(self, key, default):
        return self.get(self, key, default)

    def __getitem__(self, key):
        # We allow fall-through here, so values default to None
        return self.__dict__.get(key, None)

    def get(self, key, default=None):
        value = self.getRawValue(key)
        if value is None:
            return default
        else:
            return self.resolve(value)

    def getRawValue(self, key, default=None):
        return self.__dict__.get(key, default)

    def interpolate(self, rest, prefix, suffix, pattern, ext_dict={}):
        accum = []
        while rest:
            p = rest.find(prefix[0])
            if p < 0:
                accum.append(rest)
                return ''.join(accum)
            if p >= 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == prefix[0]:
                accum.append(prefix[0])
                rest = rest[2:]
            elif c == prefix[1]:
                m = pattern.match(rest)
                if m is None:
                    raise Exception(
                        "bad interpolation variable reference %r" % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                try:
                    if len(path) == 1:
                        opt = path[0]
                        v = ext_dict.get(opt, self.get(opt, prefix + opt + suffix))
                    elif len(path) == 2:
                        sect = path[0]
                        opt = path[1]
                        if sect == 'expr':
                            v = str(self._evalexpr(opt, ext_dict))
                        elif sect == 'rnd':
                            v = self._rnd(opt)
                        else:
                            v = ext_dict.get(opt, self.get(opt, prefix + opt + suffix))
                    accum.append(v)
                except Exception as e:
                    raise e
            else:
                accum.append(rest)

        return ''.join(accum)

    def resolve(self, value, disc={}):
        if isinstance(value, str):
            pattern = re.compile(r"<%([^>]+)%>")
            value = self.interpolate(value, "<%", "%>", pattern, disc)
            pattern = re.compile(r"\$\{([^}]+)\}")
            value = self.interpolate(value, "${", "}", pattern, disc)
            return value
        return value

    def _rnd(self, r_format):
        res_string = ""
        for char in r_format:
            res = char
            if char.isdigit():
                res = random.choice(string.digits)
            elif char.isalpha():
                res = random.choice(string.ascii_lowercase) if char.islower() else random.choice(string.ascii_uppercase)

            res_string += res
        return res_string

    def _evalexpr(self, expr, vars):
        try:
            return eval(str(expr), self.__dict__, vars)
        except NameError as ne:
            arg_index = expr.index('(')
            if not expr.startswith('__import') and arg_index > 0:
                qualified_name = expr[:arg_index]
                arg = expr[arg_index:]
                m_index = qualified_name.rindex('.')
                class_name = qualified_name[:m_index]
                method_name = qualified_name[m_index:]
                m_expr = "__import__('{0}'){1}{2}".format(class_name, method_name, arg)
                try:
                    return eval(m_expr, self.__dict__, vars)
                except Exception as ex:
                    raise ne

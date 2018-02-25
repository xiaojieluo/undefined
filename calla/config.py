import sys, os
import re
from redbaron import RedBaron
from unipath import Path
import tempfile
import importlib
import pprint
import json
import toml
from calla.model import Setting
import types

here = os.path.abspath(os.path.dirname(__file__))

class Config(dict):
    ''' config 类
    attribute only read , cannot modified
    '''
    config_file = None

    def get(self, key, default = None):
        if key in self:
            data = self[key]
            # 当 self[key] 是字典的时候， 返回本类实例
            if isinstance(data, dict):
                data = self.__class__(data)
            return data
        return default

    def __getattr__(self, key):
        return self.get(key)

    def set(self, key, value):
        self.update({key: value})

    def __setattr__(self, key, value):
        self.set(key, value)

    def save(self):
        ''' 保存配置到 self._path '''
        with open(self._path, 'w') as fp:
            toml.dump(self, fp)
        return True

    def delete(self, key):
        '''
        删除配置
        Args:
            key: 要删除的 key
        '''
        if key in self:
            del self[key]

    @classmethod
    def load(cls, path):
        ''' 静态变量， 从 toml 文件中加载配置并注入 Config 类中。 '''
        config = toml.load(path, cls)
        instance = cls()
        instance.update(config)
        instance.__dict__['_path'] = path
        return instance

    @classmethod
    def monkey_patch(cls, path):
        cls.config_file = path

    def __delattr__(self, key):
        return self.__delitem__(key)

    def __delitem__(self, key):
        if key in self:
            self.pop(key)

def make_config(path = None):
    ''' 根据配置文件组装 config
    并且用用户自定义配置覆盖默认配置
    '''
    if path is None:
        path = os.path.join(os.getcwd(), 'calla.toml')
    _config = Config.load(path)
    config = _config
    # workname = os.path.dirname(config._path)
    # config.path = os.path.join(workname, config.path)
    return config

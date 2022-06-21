# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

""" 
@Author : Fanmo
@time : 2019/1/10 17:31 
@File : setup.py
code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from setuptools import setup

setup(name='excel_db',
    version='1.0',
    packages=["excel_db"],
    include_package_data=True,
    author = 'fanmo',
    author_email = 'fanmolh@163.com',
    license = 'GPL',
    url = 'https://github.com/fanmolh/excel_db.git',
    install_requires = [
        "numpy==1.22.0",
        "pandas==0.23.4",
        "PyMySQL==0.9.3",
        "SQLAlchemy==1.2.15",
        "xlrd==1.2.0",
        "openpyxl"
    ]
)
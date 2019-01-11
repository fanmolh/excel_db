# -*- coding: UTF-8 -*-
from __future__ import unicode_literals,absolute_import

""" 
@Author : Fanmo
@time : 2019/1/9 12:08 
@File : run.py
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
from pandas import read_excel
from sqlalchemy import create_engine
from . import sql

def run(table_name,url,excel_file,config):
    """
    :param table_name:
    :param url:
    :param excel_file:
    :param config:
    :return:
    """
    conn = create_engine(url)
    data = read_excel(excel_file,sheet_name=None)

    for sheet_name in data.keys():
        mt_id = config.get(sheet_name,{}).get('mt_id')
        pkcs = config.get(sheet_name,{}).get('pkcs')
        if not mt_id:
            continue
        d = data.get(sheet_name)
        dr_names = d.columns.difference(config.get(sheet_name,{}).get('col_map',{}).keys())#去掉文件多余列
        dr_d = d.drop(dr_names,axis=1)
        dr_d.rename(columns=config.get(sheet_name,{}).get('col_map',{}),inplace = True)
        for co_new in config.get(sheet_name,{}).get('add_rs',{}).keys():
            dr_d[co_new] = config.get(sheet_name, {}).get('add_rs').get(co_new)
        sql.to_sql(dr_d,table_name, conn, if_exists='append', index=False, pkcs=pkcs)



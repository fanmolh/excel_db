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
        需要导入的表名
    :param url:
        数据库url 例如："mysql+pymysql://root:root@127.0.0.1:3306/dbname"
    :param excel_file:
        excel文件的全路径
    :param config:
        键为sheet name
        值为当前sheet的导入规则
            键：
                mt_id .....
                pkcs 数据库中表的某字段名（一个或多个）作为判断唯一性的标准，使其导入不存在的数据。
                col_map:
                    键为excel列名
                    值为数据库字段名
                add_rs:填充列
                    键为表字段名
                    值为当前字段下需要填充的值

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



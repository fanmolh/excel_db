# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

""" 
@Author : Fanmo
@time : 2019/1/10 18:09 
@File : test.py
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
from excel_db.run import run
from excel_db.run import run
config = {
        'HMC':
            {
                'mt_id': '30',
                'pkcs': ['ip'],
                'col_map':
                    {
                        'SN': 'sn',
                        'IP': 'ip',
                        'ACCOUNT': 'account',
                        'PASSWD': 'password',
                        'LOCATION': 'location'
                    },
                'add_rs': {'mt_id': '30', 'available_flag': '1', 'platform': 'HMC'}
            },
        'VIOS|IVM':
            {
                'mt_id': '31',
                'pkcs': ['ip'],
                'col_map':
                    {
                        'SN': 'sn',
                        'HOSTNAME': 'hostname',
                        'PLATFORM': 'platform',
                        'IP': 'ip',
                        'ACCOUNT': 'account',
                        'PASSWD': 'password',
                        'LOCATION': 'location'
                    },
                'add_rs': {'mt_id': '31', 'available_flag': '1'}
            },
        'SVC':
                    {
                        'mt_id': '19',
                        'pkcs': ['sn'],
                        'col_map':
                            {
                                'sn_machine': 'sn',
                                'IP': 'ip',
                                'ACCOUNT': 'account',
                                'PASSWD': 'password',
                                'location': 'location'
                            },
                        'add_rs': {'mt_id': '19', 'available_flag': '1','platform':u'SVC存储'}
                    }

    }
run("t_ip_info","mysql+pymysql://root:root@127.0.0.1:3306/dbname","tmp.xlsx",config)
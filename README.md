# excel_db
excel文件导入数据库中
def run(table_name,url,excel_file,config)
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
实例：
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
                }
            }
    run("t_ip_info","mysql+pymysql://root:root@127.0.0.1:3306/dbname","tmp.xlsx",config)






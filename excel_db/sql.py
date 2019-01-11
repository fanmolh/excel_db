# -*- coding: UTF-8 -*-
from __future__ import unicode_literals,absolute_import

""" 
@Author : Fanmo
@time : 2019/1/10 16:29 
@File : sql.py
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
from pandas.io.sql import SQLTable, SQLDatabase, _engine_builder, _is_sqlalchemy_connectable
from pandas import DataFrame, Series
from pandas.core.dtypes.common import is_dict_like
from pandas.compat import string_types
import warnings

class SQLTable_extend(SQLTable):
    def __init__(self, name, pandas_sql_engine, frame=None, index=True,
                 if_exists='fail', prefix='pandas', index_label=None,
                 schema=None, keys=None, dtype=None,pkcs=None):
        self.pkcs = pkcs
        super(SQLTable_extend,self).__init__(name, pandas_sql_engine, frame, index,
                             if_exists, prefix, index_label, schema,
                             keys, dtype)

    def _execute_insert(self, conn, keys, data_iter):
        data = [{k: v for k, v in zip(keys, row)} for row in data_iter]
        t_d = DataFrame(data)
        old_data = self.read()
        t_d = t_d.append(old_data,sort=False)
        t_d = t_d.append(old_data,sort=False)
        e_d = t_d.drop_duplicates(subset=self.pkcs,keep=False)
        if e_d.size >0:
            conn.execute(self.insert_statement(), [{k: v for k, v in zip(e_d.columns, row)} for row in e_d.values])
    def insert(self, chunksize=None):
        keys, data_list = self.insert_data()
        nrows = len(self.frame)
        if nrows == 0:
            return
        if chunksize is None:
            chunksize = nrows
        elif chunksize == 0:
            raise ValueError('chunksize argument should be non-zero')
        chunks = int(nrows / chunksize) + 1
        with self.pd_sql.run_transaction() as conn:
            for i in range(chunks):
                start_i = i * chunksize
                end_i = min((i + 1) * chunksize, nrows)
                if start_i >= end_i:
                    break

                chunk_iter = zip(*[arr[start_i:end_i] for arr in data_list])
                self._execute_insert(conn, keys, chunk_iter)

class SQLDatabase_extend(SQLDatabase):
    def to_sql(self, frame, name, if_exists='fail', index=True,
               index_label=None, schema=None, chunksize=None, dtype=None, pkcs=None):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        frame : DataFrame
        name : string
            Name of SQL table.
        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        index : boolean, default True
            Write DataFrame index as a column.
        index_label : string or sequence, default None
            Column label for index column(s). If None is given (default) and
            `index` is True, then the index names are used.
            A sequence should be given if the DataFrame uses MultiIndex.
        schema : string, default None
            Name of SQL schema in database to write to (if database flavor
            supports this). If specified, this overwrites the default
            schema of the SQLDatabase object.
        chunksize : int, default None
            If not None, then rows will be written in batches of this size at a
            time.  If None, all rows will be written at once.
        dtype : single type or dict of column name to SQL type, default None
            Optional specifying the datatype for columns. The SQL type should
            be a SQLAlchemy type. If all columns are of the same type, one
            single value can be used.

        """
        if dtype and not is_dict_like(dtype):
            dtype = {col_name: dtype for col_name in frame}

        if dtype is not None:
            from sqlalchemy.types import to_instance, TypeEngine
            for col, my_type in dtype.items():
                if not isinstance(to_instance(my_type), TypeEngine):
                    raise ValueError('The type of %s is not a SQLAlchemy '
                                     'type ' % col)

        table = SQLTable_extend(name, self, frame=frame, index=index,
                         if_exists=if_exists, index_label=index_label,
                         schema=schema, dtype=dtype,pkcs=pkcs)
        table.create()
        table.insert(chunksize)
        if (not name.isdigit() and not name.islower()):
            # check for potentially case sensitivity issues (GH7815)
            # Only check when name is not a number and name is not lower case
            engine = self.connectable.engine
            with self.connectable.connect() as conn:
                table_names = engine.table_names(
                    schema=schema or self.meta.schema,
                    connection=conn,
                )
            if name not in table_names:
                msg = (
                    "The provided table name '{0}' is not found exactly as "
                    "such in the database after writing the table, possibly "
                    "due to case sensitivity issues. Consider using lower "
                    "case table names."
                ).format(name)
                warnings.warn(msg, UserWarning)


def pandasSQL_builder(con, schema=None, meta=None,
                      is_cursor=False):
    """
    Convenience function to return the correct PandasSQL subclass based on the
    provided parameters.
    """
    # When support for DBAPI connections is removed,
    # is_cursor should not be necessary.
    con = _engine_builder(con)
    if _is_sqlalchemy_connectable(con):
        return SQLDatabase_extend(con, schema=schema, meta=meta)
    elif isinstance(con, string_types):
        raise ImportError("Using URI string without sqlalchemy installed.")
    else:
        raise ImportError("xxxx")
def to_sql(frame, name, con, schema=None, if_exists='fail', index=True,
           index_label=None, chunksize=None, dtype=None,pkcs=None):
    """
    Write records stored in a DataFrame to a SQL database.

    Parameters
    ----------
    frame : DataFrame, Series
    name : string
        Name of SQL table.
    con : SQLAlchemy connectable(engine/connection) or database string URI
        or sqlite3 DBAPI2 connection
        Using SQLAlchemy makes it possible to use any DB supported by that
        library.
        If a DBAPI2 object, only sqlite3 is supported.
    schema : string, default None
        Name of SQL schema in database to write to (if database flavor
        supports this). If None, use default schema (default).
    if_exists : {'fail', 'replace', 'append'}, default 'fail'
        - fail: If table exists, do nothing.
        - replace: If table exists, drop it, recreate it, and insert data.
        - append: If table exists, insert data. Create if does not exist.
    index : boolean, default True
        Write DataFrame index as a column.
    index_label : string or sequence, default None
        Column label for index column(s). If None is given (default) and
        `index` is True, then the index names are used.
        A sequence should be given if the DataFrame uses MultiIndex.
    chunksize : int, default None
        If not None, then rows will be written in batches of this size at a
        time.  If None, all rows will be written at once.
    dtype : single SQLtype or dict of column name to SQL type, default None
        Optional specifying the datatype for columns. The SQL type should
        be a SQLAlchemy type, or a string for sqlite3 fallback connection.
        If all columns are of the same type, one single value can be used.
    pkcs : list，default None
        column label or sequence of labels, optional
        Only consider certain columns for identifying duplicates
        Default does not take effect

    """
    if if_exists not in ('fail', 'replace', 'append'):
        raise ValueError("'{0}' is not valid for if_exists".format(if_exists))

    pandas_sql = pandasSQL_builder(con, schema=schema)

    if isinstance(frame, Series):
        frame = frame.to_frame()
    elif not isinstance(frame, DataFrame):
        raise NotImplementedError("'frame' argument should be either a "
                                  "Series or a DataFrame")

    pandas_sql.to_sql(frame, name, if_exists=if_exists, index=index,
                      index_label=index_label, schema=schema,
                      chunksize=chunksize, dtype=dtype, pkcs=pkcs)
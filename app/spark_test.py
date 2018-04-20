# -*- coding: utf-8 -*-
import sys
import json
from setup import *
from pyspark import SparkContext, SparkConf


def create_spark():
    """ Method to create Spark Context

        Returns:
        -----
        sc : pyspark.SparkContext
    """
    conf = SparkConf()\
        .setAppName("Flaspark")\
        .set("spark.executor.memory","3g")\
        .set("spark.executor.extraClassPath",
            '/srv/spark/jars/postgresql-42.1.1.jar')\
        .set('spark.driver.extraClassPath',
            '/srv/spark/jars/postgresql-42.1.1.jar')\
        .set('spark.jars', 'file:/srv/spark/jars/postgresql-42.1.1.jar')\
        .setMaster(SPARK_MASTER)
    sc = SparkContext(conf=conf)
    return sc

def create_sqlctx(sc):
    """ SQL Spark Context

        Params:
        -----
        sc : pyspark.SparkContext

        Returns:
        -----
        sqlctx : pyspark.sql.SQLContext
    """
    return SQLContext(sc)

def create_session(sqlctx):
    """ Spark Session

        Params:
        -----
        sqlctx : pyspark.sql.SQLContext

        Returns:
        spark : pyspark.sql.SparkSession
    """
    return SparkSession\
                .builder\
                .getOrCreate()

def query_psql(spark,
                jdbc_uri='postgres',
                host="localhost",
                port=5432,
                db="postgres",
                table="template0",
                props={"user":"postgres",
                    "password":"postgres"}):
    """ Query to a JDBC connected SQL Database

        Params:
        -----
        spark : pyspark.sql.SparkSession
            Spark Session
        jdbc_uri : str
            JDBC URI (e.g. postgresql)
        host : str
            DB Host
        port : int
            DB Port
        db : str
            DB name
        table : str
            DB Table to query from
        props : dict
            User, password and additional properties

        Returns:
        -----
        df : pyspark.DataFrame
            DB Table loaded dataframe
    """
    return spark.read\
            .jdbc("jdbc:{}://{}:{}/{}"\
                .format(jdbc_uri, host, port, db),
                    table=table,
                    properties={
                        "user": props['user'],
                        "password": props['password']
                    })


if __name__ == '__main__':
    # Retrieve task id
    _task_id = sys.argv[1]
    print('Executing Task:', _task_id)

    # Create Task State File and Update value
    with open('states/{}'.format(_task_id), 'w') as _f:
        _f.write(str(0))

    # Create Spark context
    sc = create_spark()
    print('Spark Context ON...')
    _testing_list = []
    for i in range(1, 11):
        print('Computing {}...'.format(i))
        # Compute Test Operation
        _rdd = sc.parallelize(range(1000000))
        _testing_list.append(_rdd.stats()\
                                .asDict())
        # Save into state file
        with open('states/{}'.format(_task_id), 'w') as _f:
            _f.write(str(i*10))
    # Write Result into dump file
    with open('dumps/{}'.format(_task_id), 'w') as _f:
        _f.write(json.dumps(_testing_list))
    sc.stop()
    print('Finished {} Test Task computation '.format(_task_id))
    
        

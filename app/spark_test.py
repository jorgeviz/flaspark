# -*- coding: utf-8 -*-
import sys
import json
from pyspark import SparkContext, SparkConf


def create_spark():
    """ Method to create Spark Context
    """
    conf = SparkConf().setAppName("Flaspark")
    sc = SparkContext(conf=conf)
    return sc


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
        _rdd = sc.parallelize(range(i*100))
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
    
        

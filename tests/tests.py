# -*- coding: utf-8  -*-
import unittest
import requests
import setup
import time

class flasparkTestCase(unittest.TestCase):
    """ Class to test Flask Spark endpoints
    """

    def test_async_test(self):
        """ Test to verify correctness in submitting an async task
        """
        print('[TEST] Testing basic async task...')
        # Submit Task
        _r = requests.post('http://{}:{}/sparktask'
                            .format(setup.APP_HOST,
                                    setup.APP_PORT))
        # Post assetion
        self.assertEqual(_r.status_code, 202)
        _t_id = _r.json()['task_id']   
        time.sleep(5)     
        while True:
            _r = requests.get('http://{}:{}/status/{}'
                                .format(setup.APP_HOST,
                                        setup.APP_PORT,
                                        _t_id))
            # Feed back about the progress
            _prog = _r.json()['progress']
            print(''.join(['>>' for i in range(0, int(_prog/10))]))
            if _prog == 100:
                break
            time.sleep(3)
        # Fetch response
        _r = requests.get('http://{}:{}/fetch/{}'
                                .format(setup.APP_HOST,
                                        setup.APP_PORT,
                                        _t_id))
        print(_r.json())
        self.assertTrue(isinstance(_r.json(), dict))

if __name__ == '__main__':
    unittest.main()
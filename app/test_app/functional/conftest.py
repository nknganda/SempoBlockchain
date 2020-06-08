import pytest
import os
import sys
import time
import logging

from helpers.utils import will_func_test_blockchain
from helpers.mocks import MockBlockchainTasker, mock_class

env_loglevel = os.environ.get('LOGLEVEL', 'DEBUG')
logging.basicConfig(level=env_loglevel)
logg = logging.getLogger(__name__)

def celery_worker_is_running():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if d:
            logg.info('running workers found')
            return True
        else:
            logg.info('no running workers found')
            return False
    except IOError as e:
        logg.info('error connecting to the backend')
        # Error connecting to the backend
        return False
    except ImportError as e:
        logg.info('import error')
        return False
    return False

@pytest.fixture(scope='module', autouse=True)
def mock_blockchain_tasks(monkeymodule):
    from server import bt
    if will_func_test_blockchain():
        print('~~~NOT Mocking Blockchain Endpoints, Eth Worker will be tested~~~')

        time_to_wait = 100
        counter = 0
        interval = 10

        while(not celery_worker_is_running()):
            logg.info('Waiting for workers to start... ' + str(counter))
            time.sleep(interval)
            counter += interval
            if (counter > time_to_wait):
                raise NameError('Workers never started')
    else:
        print('~~~Mocking Blockchain Endpoints, Eth Worker will NOT be tested~~~')
        mock_class(bt, MockBlockchainTasker, monkeymodule)

@pytest.fixture(scope='module')
def load_account():
    from web3 import (
        Web3,
        HTTPProvider
    )
    import config

    def inner(address):
        if will_func_test_blockchain():
            w3 = Web3(HTTPProvider(config.ETH_HTTP_PROVIDER))

            tx_hash = w3.eth.sendTransaction(
                {'to': address, 'from': w3.eth.accounts[0], 'value': 5 * 10 ** 18})
            hash = w3.eth.waitForTransactionReceipt(tx_hash)
            # print(f' Load account result {hash}')
            return hash
    return inner

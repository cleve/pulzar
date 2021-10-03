import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from pulzarutils.utils import Constants
from pulzarutils.utils import Utils
from pulzarutils.node_utils import NodeUtils
import requests

# Object to test
from master.master import Master


class TestUtilsMethods(unittest.TestCase):
    """Testing api calls
    """
    master_object = Master()

    def test_put(self):
        assert True is True

    def test_get(self):
        assert True is True

    def test_delete(self):
        assert True is True
    

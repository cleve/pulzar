import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import math
from pulzarutils.utils import Constants
from pulzarutils.utils import Utils
from pulzarutils.node_utils import NodeUtils

class TestUtilsMethods(unittest.TestCase):
    """Testing Util class
    """

    def setUp(self):
        const = Constants()
        self.node_utils = NodeUtils(const)

    @patch('pulzarcore.core_db.DB.get_keys_values')
    @patch.object(NodeUtils, '_node_candidates_since_path')
    def test_pick_a_volume2(self, mock_volumes, mock_db):
        mock_volumes.return_value = [b'node_a']
        mock_db.return_value = [('node_a', b'10:10:10:2020-01-01-00-00-00')]
        print(self.node_utils.pick_a_volume2('/example/fibbonacci'))
    

if __name__ == '__main__':
    unittest.main()
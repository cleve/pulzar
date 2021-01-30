import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import math
import datetime
from pulzarutils.utils import Constants
from pulzarutils.utils import Utils
from pulzarutils.node_utils import NodeUtils

class TestUtilsMethods(unittest.TestCase):
    """Testing Util class
    """

    def setUp(self):
        const = Constants()
        self.node_utils = NodeUtils(const)

    @patch('pulzarutils.utils.Utils.get_current_datetime')
    @patch('pulzarcore.core_db.DB.get_keys_values')
    @patch.object(NodeUtils, '_node_candidates_since_path')
    def test_pick_a_volume2(self, mock_volumes, mock_db, utils):
        utils.return_value = datetime.datetime.strptime('2020-01-01-00-00-00', '%Y-%m-%d-%H-%M-%S')
        mock_volumes.return_value = ['node_a']
        mock_db.return_value = [('node_a', b'10:10:10:2020-01-01-00-00-00')]
        self.assertEqual(
            'node_a',
            self.node_utils.pick_a_volume2('/example/fibbonacci')
        )

    @patch('pulzarutils.utils.Utils.get_current_datetime')
    @patch('pulzarcore.core_db.DB.get_keys_values')
    @patch.object(NodeUtils, '_node_candidates_since_path')
    def test_pick_a_volume2_different_volumes(self, mock_volumes, mock_db, utils):
        utils.return_value = datetime.datetime.strptime('2020-01-01-00-00-00', '%Y-%m-%d-%H-%M-%S')
        mock_volumes.return_value = ['node_a', 'node_b', 'node_c']
        mock_db.return_value = [
            ('node_a', b'10:10:10:2020-01-01-00-00-00'),
            ('node_b', b'12:10:10:2020-01-01-00-00-00'),
            ('node_c', b'9:10:10:2020-01-01-00-00-00'),
        ]
        self.assertEqual(
            'node_c',
            self.node_utils.pick_a_volume2('/example/fibbonacci')
        )


    

if __name__ == '__main__':
    unittest.main()
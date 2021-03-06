import unittest
from unittest.mock import MagicMock
import math
from pulzarutils.utils import Utils


class TestUtilsMethods(unittest.TestCase):
    """Testing Util class
    """

    def setUp(self):
        self.utils = Utils()

    def test_get_random_element_from_list(self):
        test_list = [3, 2, 1, 10]
        random_select = self.utils.get_random_element_from_list(test_list)
        self.assertIn(random_select, test_list)
        self.assertTrue(int, isinstance(random_select, int))

    def test_get_random_string(self):
        string = self.utils.get_random_string(10)
        self.assertEqual(len(string), 10)
        self.assertEqual(True, isinstance(string, str))

    def test_bytesto(self):
        self.assertAlmostEqual(
            1,
            math.ceil(self.utils.bytesto(1000000, 'm'))
        )

    def test_encode_base64(self):
        self.assertEqual(self.utils.encode_base_64(
            'string_to_encode'), b'c3RyaW5nX3RvX2VuY29kZQ==')

        self.assertEqual(self.utils.encode_base_64(
            'string_to_encode', to_str=True), 'c3RyaW5nX3RvX2VuY29kZQ==')

    def test_decode_base64(self):
        self.assertEqual(self.utils.decode_base_64(
            b'c3RyaW5nX3RvX2VuY29kZQ=='), b'string_to_encode')

        self.assertEqual(self.utils.decode_base_64(
            b'c3RyaW5nX3RvX2VuY29kZQ==', to_str=True), 'string_to_encode')

    def test_encode_byte_base_64(self):
        self.assertEqual(self.utils.encode_byte_base_64(
            b'string_to_encode'), b'c3RyaW5nX3RvX2VuY29kZQ==')

        self.assertEqual(self.utils.encode_byte_base_64(
            b'string_to_encode', to_str=True), 'c3RyaW5nX3RvX2VuY29kZQ==')
    
    def test_check_passport(self):
        env = {'HTTP_PASSPORT': self.utils.encode_byte_base_64(b'l415S4Nt05', to_str=True)}
        self.assertTrue(self.utils.check_passport(env))


if __name__ == '__main__':
    unittest.main()
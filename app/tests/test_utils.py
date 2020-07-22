import unittest
from utils.utils import Utils


class TestUtilsMethods(unittest.TestCase):
    """Testing Util class
    """

    def setUp(self):
        self.utils = Utils()

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


if __name__ == '__main__':
    unittest.main()

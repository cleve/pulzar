import json
import base64
import re
try:
    from PIL import Image
    from PIL import ImageOps
except ImportError:
    import Image
import pytesseract

# Public library from Vari
from pulzarutils.public import Public


class Ocr:
    """OCR third party app:
        This class allow us to get and search by text

        Use:
            server/extension/ocr?search=text
    """

    def __init__(self, arg1, search, file_path):
        self.arg1 = arg1
        self.search = search
        self.file_path = file_path
        self.public = Public()
        self.response = {}

    def do_the_work(self):
        """Method who actually do the hard work
        """
        image = Image.open(self.file_path)
        text = pytesseract.image_to_string(image, timeout=10)
        self.response['text'] = text

    def get_response(self):
        """Get the final object
        """
        return self.response


def execute(arguments, params, file_path=None):
    """Entrance point
    """
    search = None
    # Check arguments
    if file_path is None:
        raise ValueError('file path empty')
    if params:
        try:
            # Search text
            if 'search' in params:
                search = params['search'][0]
                if not isinstance(search, str):
                    search = None
        except Exception as err:
            print(err)

    if len(arguments) == 0:
        return json.dumps({'err': 'no args detected'})
    ocr = Ocr(arguments[0], search, file_path)
    ocr.do_the_work()
    return ocr.get_response()

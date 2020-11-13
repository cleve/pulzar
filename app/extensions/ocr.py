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
            server/extension/ocr/[image_name]?search=text&invert=[0|1]
    """

    def __init__(self, arg1, search, invert, percent, file_path):
        self.arg1 = arg1
        self.search = search
        self.invert = int(invert)
        self.percent = percent
        self.file_path = file_path
        self.public = Public()
        self.response = {}

    def do_the_work(self):
        """Method who actually do the hard work
        """
        image = Image.open(self.file_path)
        # Invert image if argument is not zero
        if self.invert > 0:
            image = ImageOps.invert(image.convert('RGB'))
        text = pytesseract.image_to_string(image, timeout=10)
        self.response['text'] = text
        if self.search is not None:
            if text.upper().find(self.search.upper()) >= 0:
                self.response['contains'] = True
            else:
                self.response['contains'] = False

    def get_response(self):
        """Get the final object
        """
        return self.response


def execute(arguments, params, file_path=None):
    """Entrance point
    """
    search = None
    percent = 80
    invert = 0
    # Check arguments
    if file_path is None:
        raise ValueError('file path empty')
    # Check params
    if params:
        try:
            # Search text
            if 'search' in params:
                search = params['search'][0]
                if not isinstance(search, str):
                    raise Exception('search must be string')
            # Percent
            if 'percent' in params:
                percent = params['percent'][0]
                if not isinstance(percent, int):
                    raise Exception('percent must be integer')
            # Invert
            if 'invert' in params:
                invert = params['invert'][0]
                if not isinstance(invert, int):
                    raise Exception('invert must be integer')
        except Exception as err:
            print(err)

    if len(arguments) == 0:
        raise Exception('no args detected')
    ocr = Ocr(arguments[0], search, invert, percent, file_path)
    ocr.do_the_work()
    return ocr.get_response()

try:
    from PIL import Image
    from PIL import ImageOps
except ImportError:
    import Image
import pytesseract

from pulzarutils.extension import Extension
# Public library
from pulzarutils.public import Public


class Ocr(Extension):
    """OCR third party app:
        This class allow us to get and search by text

        Use:
            server/extension/ocr/[image_name]?search=text&invert=[0|1]
    """

    def __init__(self, args, params, file_path):
        self.args = args
        self.params = params
        self.file_path = file_path
        self.public = Public()
        self.response = {}
        self.invert = 0
        self.percent = 80
        self.search = None

    def set_up(self):
        '''Setting extra parameters
        '''
        # Default values
        search = None
        invert = 0
        percent = 80
        # Check arguments
        if self.file_path is None:
            raise ValueError('file path empty')
        # Check params
        if self.params:
            try:
                # Search text
                if 'search' in self.params:
                    search = self.params['search'][0]
                    if not isinstance(search, str):
                        raise Exception('search must be string')
                # Percent
                if 'percent' in self.params:
                    percent = self.params['percent'][0]
                    if not isinstance(percent, int):
                        raise Exception('percent must be integer')
                # Invert
                if 'invert' in self.params:
                    invert = int(self.params['invert'][0])
                    if not isinstance(invert, int):
                        raise Exception('invert must be integer')
            except Exception as err:
                print(err)

        if len(self.args) == 0:
            raise Exception('no args detected')
        self.invert = invert
        self.percent = percent
        self.search = search

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

    def execute(self):
        """Entrance point
        """
        self.set_up()
        self.do_the_work()
        return self.get_response()

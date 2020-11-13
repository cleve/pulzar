import cv2
from pulzarutils.utils import Utils


class ImageUtils:
    def __init__(self, arg1, filename_template, file_name_source, percent=80):
        self.arg1 = arg1
        self.method = cv2.TM_CCOEFF_NORMED
        self.percent = 0.8

        # Images
        self.file_path_template = filename_template
        self.filename_source = file_name_source.name
        # Response
        self.response = {
            'found': False,
            'percent_of_match': None,
            'coordinates': {},
            'msg': None
        }

        # Set percent
        self.set_percent(percent)

    def set_percent(self, percent):
        if percent is None:
            self.response['percent_of_match'] = self.percent
            return
        self.percent = percent / 100.0
        self.response['percent_of_match'] = self.percent

    def do_the_work(self):
        '''Read source and template
        '''
        source_image = cv2.imread(self.filename_source)
        # Convert it to grayscale
        source_image_gray = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)

        # Read the template
        template = cv2.imread(self.file_path_template, 0)

        # Store width and height of template in w and h
        w, h = template.shape[::-1]

        # Perform match operations.
        result = cv2.matchTemplate(source_image_gray, template, self.method)
        mn, max_val, mnLoc, maxLoc = cv2.minMaxLoc(result)
        if max_val < self.percent:
            self.response['msg'] = 'percent criteria does not match'
            return
        # Image found
        self.response['found'] = True
        # Getting coordinates
        x, y = maxLoc
        trows, tcols = source_image.shape[:2]
        self.response['coordinates'] = {
            'x': x,
            'y': y,
            'w': tcols,
            'h': trows
        }

    def get_response(self):
        """Get the final object
        """
        return self.response


def execute(arguments, params, template_image=None):
    """Entrance point
    """
    percent = None
    # Check arguments
    if template_image is None:
        raise ValueError('image file empty')
    if len(arguments) == 0:
        raise Exception('no args detected')
    # Check parameters
    if params:
        # Checking params
        if 'percent' in params:
            int_percent = int(params['percent'][0])
            if int_percent >= 10 and int_percent <= 100:
                percent = int_percent
        if 'image_url' in params:
            # Download image
            base_image = Utils.download_file(params['image_url'][0])
        else:
            raise Exception("you must provide an url for the base image")

    image_matching = ImageUtils(
        arguments[0], template_image, base_image, percent)
    image_matching.do_the_work()
    return image_matching.get_response()

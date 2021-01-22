import cv2
from pulzarutils.utils import Utils
from pulzarutils.extension import Extension


class Imagematching(Extension):
    def __init__(self, arguments, params, template_image=None):
        self.utils = Utils()
        self.args = arguments
        self.params = params
        self.method = cv2.TM_CCOEFF_NORMED
        self.percent = 0.8

        # Images
        self.file_path = template_image
        self.filename_source = None
        # Response
        self.response = {
            'found': False,
            'percent_of_match': None,
            'coordinates': {},
            'msg': None
        }

    def set_up(self):
        '''Setting extra parameters
        '''
        percent = None
        # Check arguments
        if self.file_path is None:
            raise ValueError('image file empty')
        # Check parameters
        if self.params:
            # Checking params
            if 'percent' in self.params:
                int_percent = int(self.params['percent'][0])
                if int_percent >= 10 and int_percent <= 100:
                    percent = int_percent
            if 'image_url' in self.params:
                # Download image
                base_image = Utils.download_file(self.params['image_url'][0])
                if base_image is not None:
                    self.filename_source = base_image.name
                else:
                    raise Exception(
                        'Imagematching::Could not download the image, verify the source URL')
            else:
                raise Exception("you must provide an url for the base image")
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
        template = cv2.imread(self.file_path, 0)

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

    def clean(self):
        '''Deleting the base image downloaded from the url parameter
        '''
        self.utils.remove_file(self.filename_source)
    
    def get_response(self):
        """Get the final object
        """
        return self.response

    def execute(self):
        """Entrance point
        """
        self.set_up()
        self.do_the_work()
        self.clean()
        return self.get_response()

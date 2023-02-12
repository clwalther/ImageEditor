from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys
import math

class PNGImage:
    def __init__(self):
        self.pixeldata = None
        self.height    = None
        self.width     = None

    def load(self, name: str) -> int:
        """Loads data from file into list format.

            Returns:
                int: 0 if image was successfully loaded, -1 otherwise.
            """
        img = QtGui.QImage()
        if img.load(name):
            img = img.convertToFormat(QtGui.QImage.Format_RGB888)
            self.height = img.height()
            self.width = img.width()
            bare_data = list(img.scanLine(0).asarray(img.sizeInBytes()))
            self.pixeldata = []
            for i in range(0, len(bare_data), 3):
                self.pixeldata.append(bare_data[i:i+3])
            return 0
        return -1

    def save(self, name: str) -> int:
        """Writes the data into a file and saves it.

            Returns:
                int: 0 if saving was successful, -1 otherwise.
            """
        if self.pixeldata and self.height and self.width:
            flat_list = []
            for pixel in self.pixeldata:
                flat_list += pixel
            img = QtGui.QImage(bytes(flat_list), self.width, self.height, self.width*3, QtGui.QImage.Format_RGB888)
            if img.save(name):
                return 0
        return -1

    # ~ @clwalther
    def get_pixel(self, x: int, y: int) -> list:
        """Retrieve the RGB value of a given pixel in the image.

            Args:
                x (int): The x-coordinate of the pixel.
                y (int): The y-coordinate of the pixel.

            Returns:
                list: A list of 3 integers representing the red, green, and blue values of the pixel.

            Raises:
                IndexError: If the x and y values are outside the bounds of the image.
            """
        return self.pixeldata[y * self.width + x]

    def set_pixel(self, x: int, y: int, value: list) -> int:
        """Set the color value of a given pixel.

            Args:
                x (int): The x-coordinate of the pixel.
                y (int): The y-coordinate of the pixel.
                value (list): The color value of the pixel in the format [R, G, B], where R, G, and B are integers between 0 and 255.

            Returns:
                int: 0 if the operation is successful.

            Raises:
                ValueError: If the length of `value` is not 3 or if R, G, B are not integers between 0 and 255.
            """
        if not (len(value) == 3 and all(0 <= v <= 255 for v in value)):
            raise ValueError
        self.pixeldata[y * self.width + x] = list(map(int, value))

    def rotate(self, turn_index: int) -> int:
        """Rotate the image by 90°, 180°, or 270° clockwise.

            Args:
                turn_index (int): The number of turns to rotate the image (1, 2, or 3).

            Returns:
                int: 0 if the rotation was successful, raises ValueError if the turn_index is not in the range [1, 3].

            Raises:
                ValueError: If the turn_index is not in the range [1, 3]."""
        if not 1 <= turn_index <= 3:
            raise ValueError

        for _ in range(turn_index):
            flat_list = [[self.get_pixel(x, y) for x in range(self.width)] for y in range(self.height)]

            image_height = self.height
            image_width  = self.width

            self.height = image_width
            self.width  = image_height

            for y in range(image_height):
                for x in range(image_width):
                    self.set_pixel(image_height - y - 1, x, flat_list[y][x])

        return 0

    def convolve(self, image: list, sieve: list) -> list:
        """This function performs the convolution operation between an image and a filter/sieve.

            Args:
                image (list): A 2D list representing the image to be convolved. Each element of the list should be a list containing the pixel values of a row in the image.
                sieve (list): A 2D list representing the filter to be used for the convolution. Each element of the list should be a list containing the sieve coefficients for a row in the sieve.

            Returns:
                list: A 2D list representing the convolved image. Each element of the list should be a list containing the convolved pixel values for a row in the image.
            """
        image_height, image_width = len(image), len(image[0])
        sieve_height, sieve_width = len(sieve), len(sieve[0])

        output_image = [[[0, 0, 0] for x in range(image_width)] for y in range(image_height)]


        if sieve_height % 2 == 1 and sieve_width % 2 == 1:
            # loop over image
            for y in range(image_height):
                for x in range(image_width):
                    # loop over sieve
                    for k in range(int(-(sieve_height - 1) / 2), int(+(sieve_height - 1) / 2) + 1, 1):
                        for l in range(int(-(sieve_width - 1) / 2), int(+(sieve_width - 1) / 2) + 1, 1):

                            if 0 <= (y + k) < image_height and 0 <= (x + l) < image_width: # filters impossible indexs
                                for channelIndex in range(3):
                                    output_image[y][x][channelIndex] += int(image[y + k][x + l][channelIndex] * sieve[k][l][channelIndex])

                                    if output_image[y][x][channelIndex] > 255: # filters impossible values
                                        output_image[y][x][channelIndex] = 255
        else:
            raise IndexError

        return output_image

    def blur(self) -> int:
        """This function applies a blurring effect to the image. It uses a convolution operation with a pre-defined blurring constant (BLURRING_CONSTANT) to convolve the image with a sieve of size BLURRING_CONSTANT.

            Returns:
                int: 0 if successfull."""
        BLURRING_CONSTANT = 5

        image = [[self.get_pixel(x, y) for x in range(self.width)] for y in range(self.height)] # 1D list -> 2D list
        sieve = lambda size: [[[1/(size**2)]*3 for x in range(size)] for y in range(size)] # creats the sieve with a height of size and width of size

        convolved_image = self.convolve(image, sieve(BLURRING_CONSTANT))

        for x in range(self.width):
            for y in range(self.height):
                self.set_pixel(x, y, convolved_image[y][x])

        return 0

    def edge_detection(self) -> int:
        """This method of the class Image that performs edge detection on the image by convolving the image with two different kernels (sieves) and merging the results. The first kernel (sieve_0) detects vertical changes in the image, while the second kernel (sieve_1) detects horizontal changes. After convolving the image with both kernels, the rectified results are merged using the Pythagorean theorem to find the final magnitude of the edge. The final result is stored back in the original Image object.

            Returns:
                int: Always returns 0."""
        image = [[self.get_pixel(x, y) for x in range(self.width)] for y in range(self.height)] # 1D list -> 2D list
        sieve_0 = [[[-1/4]*3, [ +0 ]*3, [+1/4]*3],
                   [[-1/2]*3, [ +0 ]*3, [+1/2]*3],
                   [[-1/4]*3, [ +0 ]*3, [+1/4]*3]] # detects the vertical change
        sieve_1 = [[[-1/4]*3, [-1/2]*3, [-1/4]*3],
                   [[ +0 ]*3, [ +0 ]*3, [ +0 ]*3],
                   [[+1/4]*3, [+1/2]*3, [+1/4]*3]] # detects the horizontal change

        rectify = lambda array: [[[abs(array[y][x][i]) for i in range(len(array[0][0]))] for x in range(len(array[0]))] for y in range(len(array))]
        merge   = lambda  a, b: [[[(a[y][x][i]**2 + b[y][x][i]**2)**0.5 for i in range(len(a[0][0]))] for x in range(len(a[0]))] for y in range(len(a))] # pythagoras

        convolved_image_0 = self.convolve(image, sieve_0)
        convolved_image_1 = self.convolve(image, sieve_1)
        convolved_image_0 = rectify(convolved_image_0)
        convolved_image_1 = rectify(convolved_image_1)
        convolved_image   = merge(convolved_image_0, convolved_image_1)

        for x in range(self.width):
            for y in range(self.height):
                self.set_pixel(x, y, convolved_image[y][x])

        return 0

    # ~ @mateo
    def greyscale(self):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                self.set_pixel(x, y, [int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])] * 3)

    def invert(self):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                self.set_pixel(x, y, [255 - pixel[0], 255 - pixel[1], 255 - pixel[2]])

    def brightness(self, value):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                r_wert = min(255, pixel[0]*(1 + value))
                g_wert = min(255, pixel[1]*(1 + value))
                b_wert = min(255, pixel[2]*(1 + value))
                self.set_pixel(x, y, [r_wert, g_wert, b_wert])

    # ~ @lars
    def mirror_horizontal(self):
        flat_list = [[self.get_pixel(x, y) for x in range(self.width)] for y in range(self.height)]

        for x in range(self.width):
            for y in range(self.height):
                self.set_pixel(x, y, flat_list[self.height - y - 1][x])

    def mirror_vertical(self):
        flat_list = [[self.get_pixel(x, y) for y in range(self.height)] for x in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                self.set_pixel(x, y, flat_list[self.width - x - 1][y])

class ImageEditorApplication(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.canvas.paintEvent = self.draw
        self.image = None

        # connect actions to methods
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_cclk.clicked.connect(self.rotate_clockwise)
        self.btn_iclk.clicked.connect(self.rotate_counter_clockwise)
        self.btn_mhzt.clicked.connect(self.mirror_horizontal)
        self.btn_mvrt.clicked.connect(self.mirror_vertical)
        self.btn_grey.clicked.connect(self.greyscale)
        self.btn_invt.clicked.connect(self.invert)
        self.btn_blur.clicked.connect(self.blur)
        self.btn_edge.clicked.connect(self.edge_detection)
        self.sld_brgh.valueChanged.connect(self.changed_brightness)

    def open_file(self) -> int:
        """Opens file explorer instance and loads a chosen PNG File into the 'PNGImage' class.

            Returns:
                int: Result of 'PNGImage' method 'load' or -1 if there is no file.
            """
        options = QtWidgets.QFileDialog.Options()
        name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open Files", "","PNG-Files (*.png);;All Files (*)", options=options)
        if name:
            self.image = PNGImage()
            loaded = self.image.load(name)
            return loaded
        return -1

    def save_file(self) -> int:
        """Opens file explorer insance and saves a the current image into a PNG File.

            Returns:
                int: Result of 'PNGImage' method 'save' or -1 if there is no instance of 'PNGImage'.
                """
        if self.image:
            options = QtWidgets.QFileDialog.Options()
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save Files","","PNG-Files (*.png);;All Files (*)", options=options)
            if name:
                return self.image.save(name)
        return -1

    # ~ @clwalther
    def draw(self, event: QtCore.QEvent):
        """Draws the current image to the canvas.

            This function is called if changes have been made to parts of the screen and it updates the canvas
            with the current temporary image. It calculates the width and height of the canvas and the size of
            each pixel. It then uses a QPainter object to draw rectangles on the canvas, with the color of each
            rectangle determined by the corresponding pixel in the image.

            Args:
                event (QtCore.QEvent): Determins the redrawing of the canvas.
            """
        if self.image:
            canvas_width  = self.canvas.width()
            canvas_height = self.canvas.height()
            pixel_width   = canvas_width  / self.image.width
            pixel_height  = canvas_height / self.image.height

            pixel_size  = int(min(pixel_width, pixel_height))

            padding_x =(canvas_width  - (self.image.width  * pixel_size)) / 2
            padding_y = (canvas_height - (self.image.height * pixel_size)) / 2

            draw = QtGui.QPainter(self.canvas)
            draw.setPen(QtCore.Qt.NoPen)

            for y in range(self.image.height):
                for x in range(self.image.width):
                    pixel = self.image.get_pixel(x, y)
                    draw_x = int(padding_x + pixel_size * x)
                    draw_y = int(padding_y + pixel_size * y)

                    draw.setBrush(QtGui.QColor(pixel[0], pixel[1], pixel[2]))
                    draw.drawRect(draw_x, draw_y, pixel_size, pixel_size)
            draw.end()

    def rotate_clockwise(self) -> int:
        """Rotate the image clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` method `PNGImage` with turnIndex = 3.
            """
        if self.image:
            rotated = self.image.rotate(3)
            self.update()
            return rotated
        return -1

    def rotate_counter_clockwise(self) -> int:
        """Rotate the image counter-clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` method of `PNGImage` with turnIndex = 1.
            """
        if self.image:
            rotated = self.image.rotate(1)
            self.update()
            return rotated
        return -1

    def blur(self) -> int:
        """Connection to image blurring.

            Returns:
                int: Result of calling the `blur` method of `PNGImage` or -1, if failed."""
        if self.image:
            blurred = self.image.blur()
            self.update()
            return blurred
        return -1

    def edge_detection(self) -> int:
        """Connection to image edge detection.

            Returns:
                int: Result of calling the `edge_detection` method of `PNGImage` or -1, if failed."""
        if self.image:
            edge_detected = self.image.edge_detection()
            self.update()
            return edge_detected
        return -1

    # ~ @mateo
    def greyscale(self):
        if self.image:
            self.image.greyscale()
            self.update()

    def invert(self):
        if self.image:
            self.image.invert()
            self.update()

    def changed_brightness(self, value):
        if self.image:
            value = value / 100

            self.image.brightness(value)
            self.update()

    # ~ @lars
    def mirror_horizontal(self):
        if self.image:
            self.image.mirror_horizontal()
            self.update()

    def mirror_vertical(self):
        if self.image:
            self.image.mirror_vertical()
            self.update()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageEditorApplication()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

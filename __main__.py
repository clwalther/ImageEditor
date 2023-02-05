from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys
import numpy as np

class PNGImage:
    def __init__(self):
        self.pixeldata = None
        self.height = None
        self.width = None

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
            flat_list = []

            image_height = self.height
            image_width  = self.width

            self.height = image_width
            self.width  = image_height

            for y in range(image_height):
                start = image_width * (y + 0)
                stop  = image_width * (y + 1)
                flat_list.append(self.pixeldata[start:stop])

            for y in range(image_height):
                for x in range(image_width):
                    self.set_pixel(image_height - y - 1, x, flat_list[y][x])

        return 0

    def blur(self) -> int:
        return 0


class ImageEditorApplication(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.canvas.paintEvent = self.draw
        self.image = None

        ## connect actions to methods
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_cclk.clicked.connect(self.rotate_clockwise)
        self.btn_iclk.clicked.connect(self.rotate_counter_clockwise)
        # self.btn_mhzt.clicked.connect(...)
        # self.btn_mvrt.clicked.connect(...)
        # self.btn_gray.clicked.connect(...)
        # self.btn_invt.clicked.connect(...)
        # self.sld_brgh.valueChanged.connect(...)

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
            self.update()
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
            canvasWidth  = self.canvas.width()
            canvasHeight = self.canvas.height()
            pixelWidth   = canvasWidth  / self.image.width
            pixelHeight  = canvasHeight / self.image.height

            pixelSize    = int(min(pixelWidth, pixelHeight))

            paddingX = (canvasWidth  - (self.image.width  * pixelSize)) / 2
            paddingY = (canvasHeight - (self.image.height * pixelSize)) / 2

            draw = QtGui.QPainter(self.canvas)
            draw.setPen(QtCore.Qt.NoPen)

            for y in range(self.image.height):
                for x in range(self.image.width):
                    pixel = self.image.get_pixel(x, y)
                    drawX = int(paddingX + pixelSize * x)
                    drawY = int(paddingY + pixelSize * y)

                    draw.setBrush(QtGui.QColor(pixel[0], pixel[1], pixel[2]))
                    draw.drawRect(drawX, drawY, pixelSize, pixelSize)
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


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageEditorApplication()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

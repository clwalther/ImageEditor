from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys

class PNGImage():
    def __init__(self):
        self.pixeldata = None
        self.height    = None
        self.width     = None

    def load(self, name: str) -> int:
        """Loads data from file into list format.

            Returns: 0 if image was successfully loaded.
            """
        img = QtGui.QImage()
        if img.load(name):
            img = img.convertToFormat(QtGui.QImage.Format_RGB888)
            self.height = img.height()
            self.width = img.width()
            bareData = list(img.scanLine(0).asarray(img.sizeInBytes()))
            self.pixeldata = []
            for i in range(0, len(bareData), 3):
                self.pixeldata.append(bareData[i:i+3])
            return 0
        return -1

    def save(self, name: str) -> int:
        """Writes the data into a file and saves it.

            Returns: 0 if saving was successful."""
        if self.pixeldata and self.height and self.width:
            flatList = []
            for pixel in self.pixeldata:
                flatList += pixel
            img = QtGui.QImage(bytes(flatList), self.width, self.height, self.width*3, QtGui.QImage.Format_RGB888)
            if img.save(name):
                return 0
        return -1

    # ~ @clwalther
    def getPixel(self, x: int, y: int) -> list:
        """Retrieve the RGB value of a given pixel in the image.

            Parameters:
                x (int): The x-coordinate of the pixel.
                y (int): The y-coordinate of the pixel.

            Returns:
                list: A list of 3 integers representing the red, green, and blue values of the pixel.

            Raises:
                IndexError: If the x and y values are outside the bounds of the image.
            """
        return self.pixeldata[y * self.width + x]

    def setPixel(self, x: int, y: int, value: list) -> int:
        """Set the color value of a given pixel.

            Parameters:
                x (int): The x-coordinate of the pixel.
                y (int): The y-coordinate of the pixel.
                value (list): The color value of the pixel in the format [R, G, B], where R, G, and B are integers between 0 and 255.

            Returns:
                int: 0 if the operation is successful.

            Raises:
                ValueError: If the length of `value` is not 3 or if R, G, B are not integers between 0 and 255.
            """
        if not len(value) == 3 and 0 <= value[0] == value[1] == value[2] <= 255:
            raise ValueError
        self.pixeldata[y * self.width + x] = list(map(int, value))
        return 0

    def rotate(self, turnIndex: int) -> int:
        """Rotate the image by 90°, 180°, or 270° clockwise.

            Args:
                turnIndex (int): The number of turns to rotate the image (1, 2, or 3).

            Returns:
                int: 0 if the rotation was successful, raises ValueError if the turnIndex is not in the range [1, 3].

            Raises:
                ValueError: If the turnIndex is not in the range [1, 3]."""
        if not 1 <= turnIndex <= 3:
            raise ValueError

        for _ in range(turnIndex):
            flatList = []

            imageHeight = self.height
            imageWidth  = self.width

            self.height = imageWidth
            self.width  = imageHeight

            for y in range(imageHeight):
                start = imageWidth * (y + 0)
                stop  = imageWidth * (y + 1)
                flatList.append(self.pixeldata[start:stop])

            for y in range(imageHeight):
                for x in range(imageWidth):
                    self.setPixel(imageHeight - y - 1, x, flatList[y][x])

        return 0


class ImageEditorApplication(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.canvas.paintEvent = self.draw
        self.image = None

        ## connect actions to methods
        self.btn_open.clicked.connect(self.openFile)
        self.btn_save.clicked.connect(self.saveFile)
        self.btn_cclk.clicked.connect(self.rotateClkWise)
        self.btn_iclk.clicked.connect(self.rotateCrClkWise)
        # self.btn_mhzt.clicked.connect(...)
        # self.btn_mvrt.clicked.connect(...)
        # self.btn_gray.clicked.connect(...)
        # self.btn_invt.clicked.connect(...)
        # self.sld_brgh.valueChanged.connect(...)

    def openFile(self) -> int:
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

    def saveFile(self) -> int:
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
                    pixel = self.image.getPixel(x, y)
                    drawX = int(paddingX + pixelSize * x)
                    drawY = int(paddingY + pixelSize * y)

                    draw.setBrush(QtGui.QColor(pixel[0], pixel[1], pixel[2]))
                    draw.drawRect(drawX, drawY, pixelSize, pixelSize)
            draw.end()

    def rotateClkWise(self) -> int:
        """Rotate the image clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` method `PNGImage` with turnIndex = 3.
            """
        if self.image:
            rotated = self.image.rotate(3)
            self.update()
            return rotated
        return -1

    def rotateCrClkWise(self) -> int:
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

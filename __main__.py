from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys

class PNGBild():
    def __init__(self):
        self.pixeldata = None
        self.height = None
        self.width = None

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

            Returns: 0 if saving was successful.
        """
        if self.pixeldata and self.height and self.width:
            flatList = []
            for pixel in self.pixeldata:
                flatList += pixel
            img = QtGui.QImage(bytes(flatList), self.width, self.height, self.width*3, QtGui.QImage.Format_RGB888)
            if img.save(name):
                return 0
        return -1

    def getPixel(self, x: int, y: int) -> list:
        """Returns the pixel value of a given pixel-x-y."""
        return self.pixeldata[y * self.width + x]

    def setPixel(self, x: int, y: int, value: list) -> int:
        """Sets the pixel identified by x-y to given color value."""
        if not len(value) == 3 and map(int, value):
            raise ValueError
            return -1
        self.pixeldata[y * self.width + x] = value
        return 0


class BilderApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.canvas.paintEvent = self.draw

        self.image = None

        ## connect buttons to methods
        self.button_oeffnen.clicked.connect(self.openFile)
        self.button_speichern.clicked.connect(self.saveFile)
        self.button_drehen_links.clicked.connect(self.rotateClkWise)
        self.button_drehen_rechts.clicked.connect(self.rotateCrClkWise)
        # self.button_spiegeln_horizontal.clicked.connect(...)
        # self.button_spiegeln_vertikal.clicked.connect(...)
        # self.button_graustufen.clicked.connect(...)
        # self.button_invertieren.clicked.connect(...)
        self.slider_helligkeit.valueChanged.connect(self.changedBrightness)

    def openFile(self) -> int:
        """Opens file explorer instance and loads a chosen PNG File into the 'PNGBild' class.

            Returns:
                int: Result of 'PNGBild' method 'load' or -1 if there is no file.
            """
        options = QtWidgets.QFileDialog.Options()
        name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Open Files", "","PNG-Files (*.png);;All Files (*)", options=options)
        if name:
            self.image = PNGBild()
            loaded = self.image.load(name)
            self.update()
            return loaded
        return -1

    def saveFile(self) -> int:
        """Opens file explorer insance and saves a the current image into a PNG File.

            Returns:
                int: Result of 'PNGBild' method 'save' or -1 if there is no instance of 'PNGBild'.
                """
        if self.image:
            options = QtWidgets.QFileDialog.Options()
            name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                "Save Files","","PNG-Files (*.png);;All Files (*)", options=options)
            if name:
                return self.image.save(name)
        return -1

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

            drawRootX = (canvasWidth  - (self.image.width  * pixelSize)) / 2
            drawRootY = (canvasHeight - (self.image.height * pixelSize)) / 2

            draw = QtGui.QPainter(self.canvas)
            draw.setPen(QtCore.Qt.NoPen)

            for y in range(self.image.height):
                for x in range(self.image.width):
                    pixel = self.image.getPixel(x, y)
                    drawX = int(drawRootX + pixelSize * x)
                    drawY = int(drawRootY + pixelSize * y)

                    draw.setBrush(QtGui.QColor(pixel[0], pixel[1], pixel[2]))
                    draw.drawRect(drawX, drawY, pixelSize, pixelSize)
            draw.end()

    def rotateClkWise(self) -> int:
        """Rotate the image clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` function with turnIndex = 3.
            """
        return self.rotate(3)

    def rotateCrClkWise(self) -> int:
        """Rotate the image counter-clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` function with turnIndex = 1.
            """
        return self.rotate(1)

    def rotate(self, turnIndex: int) -> int:
        """Rotate the image by 90°, 180°, or 270° clockwise.

            Args:
                turnIndex (int): The number of turns to rotate the image (1, 2, or 3).

            Returns:
                int: 0 if the rotation was successful, raises ValueError if the turnIndex is not in the range [1, 3].

            Raises:
                ValueError: If the turnIndex is not in the range [1, 3].
            """
        if not 1 <= turnIndex <= 3:
            raise ValueError
            return -1

        for _ in range(turnIndex):
            flatList = []

            imageHeight = self.image.height
            imageWidth  = self.image.width

            self.image.height = imageWidth
            self.image.width  = imageHeight

            for y in range(imageHeight):
                start = imageWidth * (y + 0)
                stop  = imageWidth * (y + 1)
                flatList.append(self.image.pixeldata[start:stop])

            for x in range(imageHeight):
                for y in range(imageWidth):
                    self.image.setPixel(imageHeight - x - 1, y, flatList[x][y])

        self.update()

        return 0

    def changedBrightness(self, value: int) -> int:
        """Changes brightness of the """
        value = (value + 100) / 200

        if not value >= 0 and value <= 1:
            raise ValueError
            return -1

        return 0


def main():
    app = QtWidgets.QApplication(sys.argv)
    myWindow = BilderApp()
    myWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

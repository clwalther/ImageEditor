from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys

class PNGBild():
    def __init__(self):
        self.pixeldata = None
        self.height = None
        self.width = None

    def laden(self, name: str) -> bool:
        ## lädt eine Datei und belegt die Attribute pixeldata, height und width
        ## Hier bitte nichts ändern!
        img = QtGui.QImage()
        if img.load(name):
            img = img.convertToFormat(QtGui.QImage.Format_RGB888)
            self.height = img.height()
            self.width = img.width()
            rohdaten = list(img.scanLine(0).asarray(img.sizeInBytes()))
            self.pixeldata = []
            for i in range(0, len(rohdaten), 3):
                self.pixeldata.append(rohdaten[i:i+3])
            return True
        else:
            print("Ein-/Ausgabefehler beim Laden der Datei '" + name + "'.! Ist die Datei lesbar, im richtigen Format und der Name richtig?")
            return False

    def speichern(self, name: str) -> bool:
        ## speichert das Bild in einer Datei
        ## Hier bitte nichts ändern!
        if self.pixeldata and self.height and self.width:
            flache_liste = []
            for pixel in self.pixeldata:
                flache_liste += pixel
            img = QtGui.QImage(bytes(flache_liste), self.width, self.height, self.width*3, QtGui.QImage.Format_RGB888)
            if img.save(name):
                print("Datei erfolgreich gespeichert")
            else:
                print("Ein-/Ausgabefehler beim Speichern der Datei '" + name + "'.! Ist die Datei bzw. das Verzeichnis schreibbar?")

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
        ## Lädt die Benutzeroberfläche und regstriert unsere Zeichenmethode
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.canvas.paintEvent = self.draw

        self.image = None

        ## verknüpft die Buttons mit den entsprechenden Methoden
        self.button_oeffnen.clicked.connect(self.datei_oeffnen)
        self.button_speichern.clicked.connect(self.datei_speichern)
        self.button_drehen_links.clicked.connect(self.rotateClkWise)
        self.button_drehen_rechts.clicked.connect(self.rotateCrClkWise)
        # self.button_spiegeln_horizontal.clicked.connect(...)
        # self.button_spiegeln_vertikal.clicked.connect(...)
        # self.button_graustufen.clicked.connect(...)
        # self.button_invertieren.clicked.connect(...)
        self.slider_helligkeit.valueChanged.connect(self.changedBrightness)

    def datei_oeffnen(self):
        ## Öffnet einen Datei-Dialog und lädt die gewählte Datei in self.image
        ## Hier bitte nichts ändern!
        options = QtWidgets.QFileDialog.Options()
        datei_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Bilddatei öffnen", "","PNG-Bilder (*.png);;Alle Dateien (*)", options=options)
        if datei_name:
            self.image = PNGBild()
            self.image.laden(datei_name)
        self.repaint() # löst den paintEvent aus, damit die neue Datei gleich angezeigt wird.

    def datei_speichern(self):
        ## Öffnet einen Datei-Dialog und speichert self.image in der gewählten Datei
        ## Hier bitte nichts ändern!
        if self.image:
            options = QtWidgets.QFileDialog.Options()
            datei_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                "Datei speichern","","PNG-Bilder (*.png);;Alle Dateien (*)", options=options)
            if datei_name:
                self.image.speichern(datei_name)

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
                int: Result of calling the `rotate` function with turnIndex = 1.
            """
        return self.rotate(1)

    def rotateCrClkWise(self) -> int:
        """Rotate the image counter-clockwise by 90°.

            Returns:
                int: Result of calling the `rotate` function with turnIndex = 3.
            """
        return self.rotate(3)

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
            imageWdith  = self.image.width

            self.image.height = imageWdith
            self.image.width  = imageHeight

            for y in range(imageHeight):
                start = imageWdith * (y + 0)
                stop  = imageWdith * (y + 1)
                flatList.append(self.image.pixeldata[start:stop])

            for x in range(imageHeight):
                for y in range(imageWdith):
                    self.image.setPixel(x, y, flatList[x][y])

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

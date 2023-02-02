from PyQt5 import uic, QtGui, QtCore, QtWidgets
import sys

class PNGBild():
    pixeldaten = None    # Platzhalter für die Bilddaten
    hoehe = None
    breite = None

    def laden(self, name: str) -> bool:
        ## lädt eine Datei und belegt die Attribute pixeldaten, hoehe und breite
        ## Hier bitte nichts ändern!
        img = QtGui.QImage()
        if img.load(name):
            img = img.convertToFormat(QtGui.QImage.Format_RGB888)
            self.hoehe = img.height()
            self.breite = img.width()
            print("Datei erfolgreich geladen")
            rohdaten = list(img.scanLine(0).asarray(img.sizeInBytes()))
            self.pixeldaten = []
            for i in range(0, len(rohdaten), 3):
                self.pixeldaten.append(rohdaten[i:i+3])
            return True
        else:
            print("Ein-/Ausgabefehler beim Laden der Datei '" + name + "'.! Ist die Datei lesbar, im richtigen Format und der Name richtig?")
            return False


    def speichern(self, name: str) -> bool:
        ## speichert das Bild in einer Datei
        ## Hier bitte nichts ändern!
        if self.pixeldaten and self.hoehe and self.breite:
            flache_liste = []
            for pixel in self.pixeldaten:
                flache_liste += pixel
            img = QtGui.QImage(bytes(flache_liste), self.breite, self.hoehe, self.breite*3, QtGui.QImage.Format_RGB888)
            if img.save(name):
                print("Datei erfolgreich gespeichert")
            else:
                print("Ein-/Ausgabefehler beim Speichern der Datei '" + name + "'.! Ist die Datei bzw. das Verzeichnis schreibbar?")


    def set_pixel(self, x:int, y:int, farbe:list):
        ## Setze Pixel (X/Y) auf farbe, dies ist eine Liste mit drei Zahlen [R, G, B]
        # self.pixeldaten[...] = ...
        pass

    def get_pixel(self, x:int, y:int) -> list:
        return self.pixeldaten[0] # natürlich statt der 0 noch das richtige Listenelement bestimmen!


class BilderApp(QtWidgets.QMainWindow):
    bild = None
    def __init__(self, parent=None):
        ## Lädt die Benutzeroberfläche und regstriert unsere Zeichenmethode
        super().__init__(parent)
        uic.loadUi('.index.ui', self)
        self.leinwand.paintEvent = self.zeichne_leinwand

        ## verknüpft die Buttons mit den entsprechenden Methoden
        self.button_oeffnen.clicked.connect(self.datei_oeffnen)
        self.button_speichern.clicked.connect(self.datei_speichern)
        ## Die folgenden Verknüpfungen bedienen die optionalen Buttons. Einfach die
        ## drei Punkte durch die aufzurufenden Methode ersetzen, ohne Klammern()!
        self.button_drehen_links.clicked.connect(self.drehen_links)
        # self.button_drehen_rechts.clicked.connect(...)
        # self.button_spiegeln_horizontal.clicked.connect(...)
        # self.button_spiegeln_vertikal.clicked.connect(...)
        # self.button_graustufen.clicked.connect(...)
        # self.button_invertieren.clicked.connect(...)
        self.slider_helligkeit.valueChanged.connect(self.helligkeit_geaendert)

    def datei_oeffnen(self):
        ## Öffnet einen Datei-Dialog und lädt die gewählte Datei in self.bild
        ## Hier bitte nichts ändern!
        options = QtWidgets.QFileDialog.Options()
        datei_name, _ = QtWidgets.QFileDialog.getOpenFileName(self,
            "Bilddatei öffnen", "","PNG-Bilder (*.png);;Alle Dateien (*)", options=options)
        if datei_name:
            self.bild = PNGBild()
            self.bild.laden(datei_name)
        self.repaint() # löst den paintEvent aus, damit die neue Datei gleich angezeigt wird.

    def datei_speichern(self):
        ## Öffnet einen Datei-Dialog und speichert self.bild in der gewählten Datei
        ## Hier bitte nichts ändern!
        if self.bild:
            options = QtWidgets.QFileDialog.Options()
            datei_name, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                "Datei speichern","","PNG-Bilder (*.png);;Alle Dateien (*)", options=options)
            if datei_name:
                self.bild.speichern(datei_name)

    def drehen_links(self):
        print("Links drehen geklickt!")
        # Hier muss natürlich noch die richtige Implementierung erfolgen!

    def helligkeit_geaendert(self, wert):
        ## Die valueChanged-Methode des Sliders übergibt den aktuellen Wert als ersten Parameter
        print("Helligkeit:", wert)

    def zeichne_leinwand(self, event):
        ## Wird immer aufgerufen, wenn die ganze oder ein Teil der Leinwand neu gezeichnet werden muss.
        leinwandbreite = self.leinwand.width()
        leinwandhoehe = self.leinwand.height()
        if self.bild:   # macht nur etwas, wenn schon ein Bild geladen wurde.
            painter = QtGui.QPainter(self.leinwand)         # Zeichenobjekt erzeugen
            painter.setPen(QtCore.Qt.NoPen)                 # Linienstift "pen" auf "nichts" setzen
            painter.setBrush(QtGui.QColor(0, 255, 255))     # Füllungsfarbe Cyan
            painter.drawRect(20, 100, 40, 80)               # Beispielrechteck bei x=20, y=100,
                                                            # Breite=40 und Höhe=80
            painter.end()


## Die folgenden Zeilen sorgen für das Erzeugen des Fensters und das Starten einer Eventschleife,
## die ab jetzt die Kontrolle übernimmt.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWindow = BilderApp()
    myWindow.show()
    sys.exit(app.exec_())




# ImageEditor

Python-Qt basiertes Bildbearbeitungsprojekt für den Informatik-Kurs.

## Einführung

Dies ist die Dokumentation für das Informatik-Kursprojekt Bilddateien. <br>
Das Folgende gilt für `python version 3.10.7` mit dem letzten stabilen Release von `PyQt5`. Um den Code vollständig zu verstehen, empfehlen wir, die ***Doc-Strings*** zu lesen.

## Inhaltsverzeichnis
- Dokumentation
    - @clwalther
        - `PNGImage`.get_pixel()
        - `PNGImage`.set_pixel()
        - `PNGImage`.rotate()
        - `PNGImage`.convolve()
        - `PNGImage`.blur()
        - `PNGImage`.edge_detection()
        - `ImageEditorApplication`.draw()
- Gemeinsamer Teil
    - Auflösung
    - Farbtiefe
    - Farbmodi
    - Metadaten

## Dokumentation
### `PNGImage`.get_pixel (@clwalther)

Die Methode `get_pixel` liefert die RGB-Werte eines Pixels in dem Bild. Es nimmt zwei Argumente entgegen, `x` und `y`, die die x- und y-Koordinaten des Pixels darstellen. Es gibt eine Liste von drei Integern zurück, die die Rot-, Grün- und Blauwerte des Pixels darstellen. Wenn die x- und y-Werte außerhalb des Bildbereichs liegen, wird ein `IndexError` ausgelöst.

---

### `PNGImage`.set_pixel (@clwalther)

Die Methode `set_pixel` legt die Farbwerte eines bestimmten Pixels fest. Es nimmt drei Argumente entgegen: `x`, `y` und `value`. `x` und `y` stellen die x- und y-Koordinaten des Pixels dar, während `value` die Farbwerte des Pixels im Format [R, G, B] ist, wobei R, G und B Integern zwischen 0 und 255 sind. Die Methode gibt 0 zurück, wenn der Vorgang erfolgreich war. Wenn die Länge von value nicht 3 ist oder wenn R, G, B keine Integern zwischen 0 und 255 sind, wird ein `ValueError` ausgelöst.

---

### `PNGImage`.rotate (@clwalther)

Die Methode `rotate` dreht das Bild um 90°, 180° oder 270° im Uhrzeigersinn. Es nimmt ein Argument `turn_index`, das die Anzahl der Drehungen des Bildes darstellt. `turn_index` muss entweder 1, 2 oder 3 sein. Die Methode gibt 0 zurück, wenn die Rotation erfolgreich war. Wenn der `turn_index` nicht im Bereich [1, 3] liegt, wird ein `ValueError` ausgelöst.

---

### `PNGImage`.convolve (@clwalther)
Die Methode `convolve` nimmt die Argumente: `image` und `sieve`, 2-Dimensionale Listen und nimmt die (unvollständige) mathematische operation der Falutung vor, welche wieder als 2D Liste zurückgegeben wird.
Wenn `sieve` keine eindeutige Mitte hat, ihre Seite länge nicht ungerade, wird ein `IndexError` ausgelöst.

---

### `PNGImage`.blur (@clwather)
Die Funktion `blur` wendet einen Blurring-Effekt auf das Bild an. Dies wird durch eine Konvolutionsoperation mit einer vordefinierten Konstanten (`BLURRING_CONSTANT`) erreicht, bei der das Bild mit einem Sieb von Größe `BLURRING_CONSTANT` konvolviert wird. Die Funktion gibt `0` zurück, wenn sie erfolgreich war. Innerhalb der Funktion wird ein 2D-Liste aus den Pixelwerten des Bildes erstellt, ein Sieb mit einer Größe von `BLURRING_CONSTANT` wird generiert und dann wird die Konvolution durchgeführt. Die resultierende Konvolutionsbild wird schließlich den Pixelwerten des ursprünglichen Bildes zugewiesen.

---

### `PNGImage`.edge_detection (@clwather)
Die Methode `edge_detection` führt eine Kantenerkennung auf dem Bild durch, indem es das Bild mit zwei verschiedenen `Kernels` konvolviert und die Ergebnisse zusammenführt. Der erste Kernel (`sieve_0`) erkennt vertikale Änderungen im Bild, während der zweite Kernel (`sieve_1`) horizontale Änderungen erkennt. Nach dem Konvolvieren des Bildes mit beiden Kernels werden die rechteckierten Ergebnisse mithilfe des Pythagoras zum endgültigen Kantenmagnitude zusammengeführt. Das endgültige Ergebnis wird im ursprünglichen `Image-Objekt` gespeichert. Die Methode gibt immer `0` zurück, wenn sie erfolgreich war.


---

### `ImageEditorApplication`.draw (@clwalther)

In der Klasse `ImageEditorApplication` nimmt die Methode `draw` ein Argument: `event`: `QtCore.QEvent`. Diese Methode wird aufgerufen, wenn Updates aufgerufen werden und die Anwendung Teile der Anwendung erneut auf den Bildschirm rendern möchte. Falls dies der Fall ist, wird folgendes Verfahren durchgeführt:

    1. Die Größe der Pixel wird bestimmt, indem das Kleinere von `pixel_width` und `pixel_height` gewählt wird.
    2. Um die Mitte auszurichten, werden die erforderlichen Offsets berechnet und in `padding_x` und `padding_y` gespeichert.
    3. Das Bild wird über `x` und `y` iteriert und das RGB-Pixel wird als Rechteck auf die Leinwand gezeichnet.


## Gemeinsamer Teil

### Auflösung:
`Auflösung` bezieht sich auf die `Schärfe` und `Klarheit` eines Bildes. Es beschreibt die `Anzahl` der `Pixel`, die das `Bild` enthält, und somit auch die Genauigkeit der Darstellung von Details. Je höher die Auflösung eines Bildes ist, desto mehr Details können darauf dargestellt werden, und desto klarer und schärfer wird das Bild aussehen. Eine niedrigere Auflösung führt dazu, dass das Bild unschärfer und verschwommen erscheint

### Farbtiefe:
`Farbtiefe` bezieht sich auf die `Anzahl` der `Farben`, die in einem Bild dargestellt werden können. Es gibt verschiedene Farbtiefen, die die Anzahl der `Bits pro Pixel` definieren, die verwendet werden, um eine Farbe zu codieren. Eine höhere Farbtiefe bedeutet, dass mehr Farben dargestellt werden können, was zu einer reicheren und klareren Farbdarstellung führt. Eine niedrigere Farbtiefe führt dazu, dass Farben blockiger und nicht so detailreich wirken.

### Farbmodi:
`Farbmodi` beziehen sich auf die Art und Weise, wie `Farbinformationen` in einem digitalen Bild gespeichert werden. Es gibt verschiedene Farbmodi, die unterschiedliche Anzahlen von Farbinformationen speichern und `unterschiedliche Farbräume` abbilden können. Die häufigsten Farbmodi sind `RGB` (Rot-Grün-Blau), `CMYK` (Cyan-Magenta-Gelb-Schwarz) und `Graustufen`.

`RGB` ist ein `additiver` Farbmodus, bei dem Farbinformationen durch die Kombination von Rot-, Grün- und Blau-Licht erzeugt werden. Es wird häufig für die Darstellung von Farbinformationen auf Computerbildschirmen und -projektoren verwendet.

`CMYK` ist ein `subtraktiver` Farbmodus, bei dem Farbinformationen durch die Überlagerung von Cyan-, Magenta-, Gelb- und Schwarz-Tinten erzeugt werden. Es wird häufig für die Darstellung von Farbinformationen in Druckmedien wie Zeitungen und Zeitschriften verwendet.

`Graustufen` sind ein einfacher Farbmodus, bei dem jedes Pixel einen Grauwert auf z.B: einer Skala von 0 (schwarz) bis 255 (weiß) hat. Es wird häufig für die Darstellung von monochromen Bildern und bei der Verarbeitung von Bildern verwendet (z.B: bei Computertomographie).

### Metadaten
`Metadaten` beziehen sich auf `zusätzliche Informationen`, die zu einem digitalen Bild gespeichert werden können, die jedoch `nicht Teil` des eigentlichen Bildes sind. Dies kann beispielsweise Informationen über das Datum, die Zeit, den Autor, die Kamera, die verwendeten Einstellungen und vieles mehr sein.

Metadaten können sehr hilfreich sein, um Bilder zu organisieren, zu beschreiben und zu finden, und sie können auch für die Verwendung von Bildern bei der Veröffentlichung und Verteilung wichtig sein.

### BONUS: Datenkompression
`DEFLATE` ist ein Verfahren zur Datenkompression, das auf der `LZ77`-Kompressionsmethode und dem `Huffman`-Coding basiert. Es wird häufig verwendet, um Daten in verschiedenen Dateitypen, einschließlich `PNG`-Bildern und ZIP-Archiven, zu komprimieren.

Das DEFLATE-Verfahren arbeitet, indem es `wiederholte` Zeichenfolgen in einem Datensatz erkennt und sie durch Referenzen auf bereits `gespeicherte Zeichenfolgen` ersetzt. Die so erzeugten Referenzen werden dann mit einem `Huffman`-Code kodiert, der den Code für jede Referenz so optimiert, dass die `häufiger vorkommenden Referenzen kürzer codiert` werden `als die selteneren`.

Insgesamt ermöglicht DEFLATE eine effiziente Kompression von Daten, wodurch die Größe der Daten reduziert wird und die Übertragungszeiten verkürzt werden.

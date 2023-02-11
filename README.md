# ImageEditor

Python-Qt basiertes Bildbearbeitungsprojekt für den Informatik-Kurs.

## Einführung

Dies ist die Dokumentation für das Informatik-Kursprojekt Bilddateien. <br>
Das Folgende gilt für `python version 3.10.7` mit dem letzten stabilen Release von `PyQt5`. Um den Code vollständig zu verstehen, empfehlen wir, die ***Doc-Strings*** zu lesen.

## Inhaltsverzeichnis

- @clwalther
    - PNGImage.get_pixel()
    - PNGImage.set_pixel()
    - PNGImage.rotate()
    - ImageEditorApplication.draw()

## Dokumentation
### `PNGImage`.get_pixel (@clwalther)

Die Methode `get_pixel` liefert die RGB-Werte eines Pixels in dem Bild. Es nimmt zwei Argumente entgegen, `x` und `y`, die die x- und y-Koordinaten des Pixels darstellen. Es gibt eine Liste von drei Integern zurück, die die Rot-, Grün- und Blauwerte des Pixels darstellen. Wenn die x- und y-Werte außerhalb des Bildbereichs liegen, wird ein `IndexError` ausgelöst.

---

### `PNGImage`.set_pixel (@clwlather)

Die Methode `set_pixel` legt die Farbwerte eines bestimmten Pixels fest. Es nimmt drei Argumente entgegen: `x`, `y` und `value`. `x` und `y` stellen die x- und y-Koordinaten des Pixels dar, während `value` die Farbwerte des Pixels im Format [R, G, B] ist, wobei R, G und B Integern zwischen 0 und 255 sind. Die Methode gibt 0 zurück, wenn der Vorgang erfolgreich war. Wenn die Länge von value nicht 3 ist oder wenn R, G, B keine Integern zwischen 0 und 255 sind, wird ein `ValueError` ausgelöst.

---

### PNGImage.rotate (@clwalther)

Die Methode rotate dreht das Bild um 90°, 180° oder 270° im Uhrzeigersinn. Es nimmt ein Argument `turn_index`, das die Anzahl der Drehungen des Bildes darstellt. `turn_index` muss entweder 1, 2 oder 3 sein. Die Methode gibt 0 zurück, wenn die Rotation erfolgreich war. Wenn der `turn_index` nicht im Bereich [1, 3] liegt, wird ein `ValueError` ausgelöst.


---

ImageEditorApplication.draw (@clwalther)

In der Klasse ImageEditorApplication nimmt die Methode `draw` ein Argument: `event`: `QtCore.QEvent`. Diese Methode wird aufgerufen, wenn Updates aufgerufen werden und die Anwendung Teile der Anwendung erneut auf den Bildschirm rendern möchte. Falls dies der Fall ist, wird folgendes Verfahren durchgeführt:

    1. Die Größe der Pixel wird bestimmt, indem das Kleinere von `pixel_width` und `pixel_height` gewählt wird.
    2. Um die Mitte auszurichten, werden die erforderlichen Offsets berechnet und in `padding_x` und `padding_y` gespeichert.
    3. Das Bild wird über `x` und `y` iteriert und das RGB-Pixel wird als Rechteck auf die Leinwand gezeichnet.

---

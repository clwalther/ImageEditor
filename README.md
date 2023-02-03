# ImageEditor
Python-Qt based image-editor project for CS-class.

## Introduction
This is the documentation for the CS-class project `Bilddateien`.<br>
The following will be true in `python version 3.10.7` with `PyQt5` last stable relase. To fully understand the code we recommend to go read the ***__doc-strings__***.

## Table of Contents
- @clwalther
    - `PNGImage`.getPixel()
    - `PNGImage`.setPixel()
    - `PNGImage`.rotate()
    - `ImageEditorApplication`.draw()


## Documentation
---
### `PNGImage`.getPixel (@clwalther)
In the class `PNGImage` the method `getPixel` has two positional arguments: `x`: `int`, `y`: `int`. The method returns the RGB value of the pixel identified by these coordinates as a `list`.

---

### `PNGImage`.setPixel (@clwlather)
In the class `PNGImage` the method `setPixel` has three arguments: `x`: `int`, `y`: `int`, `value`: `list`. The first two arguments are again used to identify the pixel but the third is the RGB value that pixel should store now.

A `ValueError` is raised if the list doesn't contain three `int` and if they are not in the interval [0, 255].

---

### `PNGImage`.rotate (@clwalther)
In the class `PNGImage` the method `rotate` takes one argument `turnIndex`: `int`. This variable defines to what ammount the image should be turned.

    1 <==> 90°
    2 <==> 180°
    3 <==> 270°

Depending on this the following will be executed for either one, two or three times:

1. the height and width of the image are beeing readjusted
2. the 'rows' of the image are beeing stripped out of the main pixeldata and are stored seperatly in an other list
3. it is beeing looped over the previous image layout but the pixels that are beeing placed have their x-y-coordinates basically swaped.

---

### `ImageEditorApplication`.draw (@clwalther)
In the class `ImageEditorApplication` the method `draw` takes one argument: `event`: `QtCore.QEvent`. This method is called when updates are beeing called and the application wants to rerender parts of the application to the screen. If this is the case, the following procedure will unfold:

1. The size of the pixels is determined by choosing the smallest of the `pixelWidth` and `pixelHeight`.
2. To center the necessary offsets are beeing calculated and saved in `paddingX` and `paddingY`.
3. The image is beeing iterated over for `x` and `y` and the pixel RGB is than beeing drawn as a rectangle to the canvas.

---

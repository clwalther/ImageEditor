# ImageEditor
Python-Qt based image-editor project for CS-class.

## Introduction
This is the documentation for the CS-class project `Bilddateien`.<br>
The following will be true in `python version 3.10.7` with `PyQt5` last stable relase. To fully understand the code we recommend to go read the ***__doc-strings__***.

## Table of Contents
- @clwalther
    - `PNGImage`.get_pixel()
    - `PNGImage`.set_pixel()
    - `PNGImage`.rotate()
    - `ImageEditorApplication`.draw()


## Documentation

### `PNGImage`.get_pixel (@clwalther)
The `get_pixel` method retrieves the RGB value of a pixel in the image. It takes two arguments, `x` and `y`, which represent the x and y coordinates of the pixel, respectively. It returns a list of three integers that represent the red, green, and blue values of the pixel. If the x and y values are outside the bounds of the image, the method raises an `IndexError`.

---

### `PNGImage`.set_pixel (@clwlather)
The `set_pixel` method sets the color value of a given pixel. It takes three arguments: `x`, `y`, and `value`. `x` and `y` represent the x and y coordinates of the pixel, respectively, and value is the color value of the pixel in the format [R, G, B], where R, G, and B are integers between 0 and 255. The method returns 0 if the operation is successful. If the length of value is not 3 or if R, G, B are not integers between 0 and 255, the method raises a `ValueError`.

---

### `PNGImage`.rotate (@clwalther)
The `rotate` method rotates the image by 90°, 180°, or 270° clockwise. It takes one argument, `turn_index`, which represents the number of turns to rotate the image. turn_index must be either 1, 2, or 3. The method returns 0 if the rotation was successful. If the `turn_index` is not in the range [1, 3], the method raises a `ValueError`.

---

### `ImageEditorApplication`.draw (@clwalther)
In the class `ImageEditorApplication` the method `draw` takes one argument: `event`: `QtCore.QEvent`. This method is called when updates are beeing called and the application wants to rerender parts of the application to the screen. If this is the case, the following procedure will unfold:

1. The size of the pixels is determined by choosing the smallest of the `pixel_width` and `pixel_height`.
2. To center the necessary offsets are beeing calculated and saved in `padding_x` and `padding_y`.
3. The image is beeing iterated over for `x` and `y` and the pixel RGB is than beeing drawn as a rectangle to the canvas.

---

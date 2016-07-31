Introduction
============

*EmuSnap Crop* is a simple tool to make removing "blank" borders around emulator screenshots much more easy and quick.

Requisites
==========

  * Python 2.x
  * Python libraries:
    * Tkinter
    * Pillow
    
Non-GUI controls
================

You can control the program with the on-screen buttons but also with the following keyboard/mouse shortcuts:

  * `w` Activate/deactivate top crop.
  * `s` Activate/deactivate bottom crop.
  * `a` Activate/deactivate left crop.
  * `d` Activate/deactivate right crop.
  * `z` Change zoom (1x, 2x, 3x).
  * `c` Change crop indicator color.
  * `ESC` Exit program.
  * `Ctrl s` Save image, original file will be overwritten.
  * `Ctrl Shift s` Save image without confirmation, original file will be overwritten.
  * `Right arrow` Load next image.
  * `Left arrow` Load previous image.
  * `+` Increase crop size by one pixel.
  * `-` Decrease crop size by one pixel.
  * `Shift +` Increase crop size by 8 pixels.
  * `Shift -` Decrease crop size by 8 pixels.
  * `Mouse wheel up` Increase crop size by 1 pixel (Linux only?).
  * `Mouse wheel down` Decrease crop size by 1 pixel (Linux only?).
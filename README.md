# KivySpriteTouch
If you want to manipulate pixels then upload them to a widget, this is the LGPL library (not quite modular yet, but with example) for you.

##KivySpriteTouch
* The example is a paint program (KivySpriteTouch.py) with save feature!

##KPImage
* The KPImage class (short for Kivy pixel image) is what you want to use if you want to manipulate pixels yourself and later upload them to a Kivy Widget.
* KPImage integrates with kivy pixel formats, and accounts for the oddity where pygame saves png file with Green and Blue switched. (see saveAs method)
* Has a Python-only base class called PPImage (short for Python pixel image) that does not depend on anything outside of python itself.

##Release notes
* (2015-03-05) First working version uploaded to GitHub 

##Known Issues
* move blitting code from example program brushAt method to PPImage (create blit method)
* add clipping to blit code, to prevent exception when blitting near edge (exception handling already present)

# KivySpriteTouch
If you want to manipulate pixels then upload them to a widget, this is the LGPL library (not quite modular yet, but with example) for you.

## Components
### KivySpriteTouch
* The example is a paint program (KivySpriteTouch.py) with save feature!

### KPImage
* The KPImage class (short for Kivy pixel image) is what you want to use if you want to manipulate pixels yourself and later upload them to a Kivy Widget.
* KPImage integrates with kivy pixel formats, and accounts for the oddity where pygame saves png file with Green and Blue switched. (see saveAs method if you want to see how the problem is fixed)
* Has a Python-only base class called PPImage (short for Python pixel image) that does not depend on anything outside of python itself.

### Release notes
* (2015-03-05) First working version uploaded to GitHub

## Known Issues
* move blitting code from example program brushAt method to PPImage (create blit method)
* add clipping to blit code, to prevent exception when blitting near edge (exception handling already present)
* How much color is affected should be inverse of background alpha (so drawing on transparent image doesn't leave black fringe around brush strokes)
* don't lose data when resizing window
* (!) Make objects (drawings) that can be saved as sprites
* (!) detect byte order of surface, to avoid green-red reversal issue in kivy 1.8.0 pygame.image.fromstring with parameter self.fbo.pixelsd
* (!) Make all objects except menu pixel-based (so use widget instead of FloatLayout)

## Planned Features
* Make animated sprites
* Save sprite animations as gif or zipped png sequence so as to be played back by Kivy's built-in animation player (just use gif or zip as source for Image)

## Developer Notes
* KivySpriteTouch was originally forked from FBO Canvas from Kivy 1.8.0 examples.

### Ideas
To save space for large sandy or grassy areas, only save:
- bumpByte (i.e. one for grass, one for sand, etc)

Then during runtime:
- Use slightly randomized pallete
  - greens-yellows for grass
  - black-brown for terrain damage!
    (for damage, edit the bump map as well)
- Apply an over-all smoother hilly randomized bump mapping
  - byte-based, or try area FX

### Widget Anatomy
See also:
- ~/.local/lib/python3.9/site-packages/kivy/uix/widget.py

#### Button
```
canvas.children:[
    kivy.graphics.context_instructions.Color,
    kivy.graphics.context_instructions.BindTexture,
    kivy.graphics.vertex_instructions.BorderImage,
    kivy.graphics.context_instructions.Color,
    kivy.graphics.context_instructions.BindTexture,
    kivy.graphics.vertex_instructions.Rectangle
]
```

# Deprecated
(KivyPixels)

* Moved from kivyspritetouch.py to kivypixels.py:
   ```Python
    def setBrushColor(self, color):
        self._brush_color = color
        # print("  self._brush_color.rgba:"
              # + str( (self._brush_color.rgba) ) )
        # During the PixelWidget constructor, param is ColorInstruction
        print("  self._brush_color:" + str( self._brush_color ) )
        print("  type(self._brush_color):" + str( type(self._brush_color) ) )
        if self.brushImage is not None:
            self.brushImage.blit_copy(self.brushOriginalImage)
            self.brushImage.tintByColor(self._brush_color)
        else:
            print("ERROR: brushImage is None")
```

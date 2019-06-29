# Deprecated

* (kivypixels.py) This method is apparently redundant. It was in the
  ownCloud branch which does not have the brushAt method.
```Python
    def drawFromKivyImage_ToTopLeft_FillRestWithTransparent(self, thisKivyImage):
        maxAlpha = 0
        sourcePixelCount = 0
        #source image channel offsets:
        bOffset = 0
        gOffset = 1
        rOffset = 2
        aOffset = 3
        dest_line_byte_index = 0
        dest_pixel_byte_index = 0
        participle = "reading pixels"
        result_string = "FAIL"
        try:
            dest_line_byte_index = 0
            for y in range(self.height):
                participle = "(no pixel yet)"
                dest_pixel_byte_index = dest_line_byte_index
                if (y<thisKivyImage.height):
                    for x in range(self.width):
                        if (x<thisKivyImage.width):
                            participle = "reading pixel"
                            color = thisKivyImage.read_pixel(x,y)
                            participle = "copying channels"
                            #+.5 for rounding:
                            thisA = int(255.0*color[aOffset]+.5)
                            self.data[dest_pixel_byte_index + self.bOffset] = int(255.0*color[bOffset]+.5)
                            self.data[dest_pixel_byte_index + self.gOffset] = int(255.0*color[gOffset]+.5)
                            self.data[dest_pixel_byte_index + self.rOffset] = int(255.0*color[rOffset]+.5)
                            self.data[dest_pixel_byte_index + self.aOffset] = thisA
                            participle = "after reading channels"
                            sourcePixelCount += 1
                            if (thisA>maxAlpha):
                                maxAlpha = thisA
                        else:
                            self.data[dest_pixel_byte_index + self.bOffset] = 0
                            self.data[dest_pixel_byte_index + self.gOffset] = 0
                            self.data[dest_pixel_byte_index + self.rOffset] = 0
                            self.data[dest_pixel_byte_index + self.aOffset] = 0
                        dest_pixel_byte_index += self.byteDepth
                else:
                    for x in range(thisKivyImage.width):
                        self.data[dest_pixel_byte_index + self.bOffset] = 0
                        self.data[dest_pixel_byte_index + self.gOffset] = 0
                        self.data[dest_pixel_byte_index + self.rOffset] = 0
                        self.data[dest_pixel_byte_index + self.aOffset] = 0
                        dest_pixel_byte_index += self.byteDepth
                dest_line_byte_index += self.stride
            result_string = "OK"
        #except Exception as e:
        #    print("Could not finish "+participle+" drawFromKivyImage_ToTopLeft_FillRestWithTransparent: "+str(e))
        except:
            print("Could not finish "+participle+" drawFromKivyImage_ToTopLeft_FillRestWithTransparent: ")
            view_traceback()
            print("dump:")
            print(self.get_dump())
        if self.enableDebug:
            print("drawFromKivyImage_ToTopLeft_FillRestWithTransparent..."+result_string+" {sourcePixelCount:"+str(sourcePixelCount)+"; maxAlpha:"+str(maxAlpha)+"; dest_line_byte_index:"+str(dest_line_byte_index)+"; dest_pixel_byte_index:"+str(dest_pixel_byte_index)+"}")
            print()
```

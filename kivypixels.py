from pythonpixels import PPImage, PPColor
#from pythonpixels import PPColor
import pygame
import os

from pythonpixels import bufferToTupleStyleString

class KPImage(PPImage):
    brushFileName = None
    brushSurface = None
    brushPixels = None
    brushImage = None
    brushTexture = None
    
    def static_createFromImageFile(self,fileName):
        returnKVI = None
        if os.path.exists(fileName):
            newSurface = pygame.image.load(fileName)
            returnKVI = KPImage(newSurface.get_width(), newSurface.get_height(), KPImage.defaultByteDepth)
            data = pygame.image.tostring(newSurface, 'RGBA', False)
            #drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(self, inputArray, inputStride, inputByteDepth, inputWidth, inputHeight, bOffset, gOffset, rOffset, aOffset):
            
            newSurface_byteDepth = newSurface.get_bytesize() #int(newSurface.get_bitsize()/8)
            newSurface_stride = newSurface.get_pitch() #newSurface.get_width() * newSurface_byteDepth
            bOffset = 0
            gOffset = 1
            rOffset = 2
            aOffset = 3
            returnKVI.drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(data, newSurface_stride, newSurface_byteDepth, newSurface.get_width(), newSurface.get_height(), bOffset, gOffset, rOffset, aOffset)
        else:
            print("ERROR in KivyPixels.static_createFromImageFile: file \""+fileName+"\"does not exist")
        return returnKVI
    
    def load(self, fileName):
        self.lastUsedFileName = fileName
        newSurface = pygame.image.load(fileName)
        self.init(newSurface.get_width(), newSurface.get_height(), KPImage.defaultByteDepth)
        data = pygame.image.tostring(newSurface, 'RGBA', False)
        #drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(self, inputArray, inputStride, inputByteDepth, inputWidth, inputHeight, bOffset, gOffset, rOffset, aOffset):
        
        newSurface_byteDepth = newSurface.get_bytesize() #int(newSurface.get_bitsize()/8)
        newSurface_stride = newSurface.get_pitch() #newSurface.get_width() * newSurface_byteDepth
        bOffset = 0
        gOffset = 1
        rOffset = 2
        aOffset = 3
        KPImage.drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(self, data, newSurface_stride, newSurface_byteDepth, newSurface.get_width(), newSurface.get_height(), bOffset, gOffset, rOffset, aOffset)
    
    
    
    def saveAs(self, fileName):
        IsOK = None
        print("Saving \"" + os.path.join(os.getcwd(), fileName) + "\"")
        
        #self.updateVariableImageSize()
        #self.assumed_fbo_stride = int(self.fbo.size[0]) * self.assumed_fbo_byteDepth
        #self.pixelBuffer.array_DrawToSelf_ToTopLeft_FillRestWithTransparent_ToCustomByteOrder(self.fbo.pixels, self.assumed_fbo_stride, self.assumed_fbo_byteDepth, self.fbo.size[0], self.fbo.size[1], bOffset, gOffset, rOffset, aOffset)
        try:
            if (self.IsDebugMode):
                print("self.width:"+str(self.width))
                print("self.height:"+str(self.height))
                print("len(self.buffer):"+str(len(self.buffer)))
                #print("self.getMaxChannelValueNotIncludingAlpha():"+str(self.getMaxChannelValueNotIncludingAlpha()))
                #print("self.getMaxAlphaValue():"+str(self.getMaxAlphaValue()))
            translatedImage = KPImage(self.width, self.height, self.byteDepth)

            # since pygame.image.fromstring (or pygame.image.save??) has odd (accidentally [??] errant) byte order,
            # channel offsets are:
            translatedImage.bOffset = self.gOffset #such as 1
            translatedImage.gOffset = self.bOffset #such as 0
            translatedImage.rOffset = self.rOffset #such as 2
            translatedImage.aOffset = self.aOffset #such as 3
            # NOTE: kivy's pygame.image.fromstring(data, (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True) #is not at fault for channel order issue, and has correct channel order
            translatedImage.drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(self.buffer, self.stride, self.byteDepth, self.width, self.height, self.bOffset, self.gOffset, self.rOffset, self.aOffset)
            data = bytes(translatedImage.buffer) #convert from bytearray to bytes
            if (self.IsDebugMode):
                debugX = 3
                debugY = self.height - 3
                if (debugX>=self.width): debugX=self.width-1
                if (debugY>=self.height): debugY=self.height-1
                debugIndex = debugY*self.stride + debugX*self.byteDepth
                print("debug pixel at ("+str(debugX)+","+str(debugY)+"): "+bufferToTupleStyleString(data,debugIndex,self.byteDepth))
            surface = pygame.image.fromstring(data, (self.width, self.height), 'RGBA', True)
            pygame.image.save(surface, fileName)
            IsOK = True
        except Exception as e:
            IsOK = False
            print("Could not finish saving: "+str(e))

        return IsOK
    
    def save(self):
        return self.saveAs(self.lastUsedFileName)
    
    def tintByColor(self, color):
        #thisPPColor = PPColor()
        #thisPPColor.setBytesFromRGBA( int(color.r*255.0+.5), int(color.g*255.0+.5), int(color.b*255.0+.5), int(color.a*255.0+.5) )
        source_bOffset=0
        source_gOffset=1
        source_rOffset=2
        source_aOffset=3
        try:
            pixelByteIndex = 0
            if (self.aOffset is not None):
                for pixelIndex in range(0,self.width*self.height):
                    self.buffer[pixelByteIndex+self.bOffset] = int( float(self.buffer[pixelByteIndex+self.bOffset]) * color[source_bOffset] + .5 )  #+ .5 for rounding
                    self.buffer[pixelByteIndex+self.gOffset] = int( float(self.buffer[pixelByteIndex+self.gOffset]) * color[source_gOffset] + .5 )  #+ .5 for rounding
                    self.buffer[pixelByteIndex+self.rOffset] = int( float(self.buffer[pixelByteIndex+self.rOffset]) * color[source_rOffset] + .5 )  #+ .5 for rounding
                    self.buffer[pixelByteIndex+self.aOffset] = int( float(self.buffer[pixelByteIndex+self.aOffset]) * color[source_aOffset] + .5 )  #+ .5 for rounding
                    pixelByteIndex += self.byteDepth
            elif (self.byteDepth==3):
                for pixelIndex in range(0,self.width*self.height):
                    self.buffer[pixelByteIndex+self.bOffset] = int( float(self.buffer[pixelByteIndex+self.bOffset]) * color[source_bOffset] + .5 )  #+ .5 for rounding
                    self.buffer[pixelByteIndex+self.gOffset] = int( float(self.buffer[pixelByteIndex+self.gOffset]) * color[source_gOffset] + .5 )  #+ .5 for rounding
                    self.buffer[pixelByteIndex+self.rOffset] = int( float(self.buffer[pixelByteIndex+self.rOffset]) * color[source_rOffset] + .5 )  #+ .5 for rounding
                    pixelByteIndex += self.byteDepth
            else:
                print("Not yet implemented KVImage tintByColor where self.byteDepth="+str(self.byteDepth))
        except:
            try:
                pixelByteIndex = 0
                if (self.aOffset is not None):
                    for pixelIndex in range(0,self.width*self.height):
                        self.buffer[pixelByteIndex+self.bOffset] = int( float(self.buffer[pixelByteIndex+self.bOffset]) * color.b + .5 )  #+ .5 for rounding
                        self.buffer[pixelByteIndex+self.gOffset] = int( float(self.buffer[pixelByteIndex+self.gOffset]) * color.g + .5 )  #+ .5 for rounding
                        self.buffer[pixelByteIndex+self.rOffset] = int( float(self.buffer[pixelByteIndex+self.rOffset]) * color.r + .5 )  #+ .5 for rounding
                        self.buffer[pixelByteIndex+self.aOffset] = int( float(self.buffer[pixelByteIndex+self.aOffset]) * color.a + .5 )  #+ .5 for rounding
                        pixelByteIndex += self.byteDepth
                elif (self.byteDepth==3):
                    for pixelIndex in range(0,self.width*self.height):
                        self.buffer[pixelByteIndex+self.bOffset] = int( float(self.buffer[pixelByteIndex+self.bOffset]) * color.b + .5 )  #+ .5 for rounding
                        self.buffer[pixelByteIndex+self.gOffset] = int( float(self.buffer[pixelByteIndex+self.gOffset]) * color.g + .5 )  #+ .5 for rounding
                        self.buffer[pixelByteIndex+self.rOffset] = int( float(self.buffer[pixelByteIndex+self.rOffset]) * color.r + .5 )  #+ .5 for rounding
                        pixelByteIndex += self.byteDepth
                else:
                    print("Not yet implemented KVImage tintByColor where self.byteDepth="+str(self.byteDepth))
                
            except:
                print("Could not finish KVImage tintByColor: color="+str(color))
    
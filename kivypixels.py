from pythonpixels import PPImage, PPColor
# from pythonpixels import PPColor
from pythonpixels import vec4_from_vec3, bgr_from_hex
import pygame
import os

from pythonpixels import bufferToTupleStyleString

# formerly static_createFromImageFile
def load_image(self,fileName):
    returnKVI = None
    if os.path.exists(fileName):
        newSurface = pygame.image.load(fileName)
        returnKVI = KPImage(newSurface.get_size())
        data = pygame.image.tostring(newSurface, 'RGBA', False)
        # blit_copy_with_bo(self, inputArray, inputStride,
                          # inputByteDepth, input_size,
                          # bOffset, gOffset, rOffset, aOffset):

        newSurface_byteDepth = newSurface.get_bytesize()
            # int(newSurface.get_bitsize()/8)
        newSurface_stride = newSurface.get_pitch()
            # newSurface.get_width() * newSurface_byteDepth
        bOffset = 0
        gOffset = 1
        rOffset = 2
        aOffset = 3
        returnKVI.blit_copy_with_bo(data, newSurface_stride,
                                    newSurface_byteDepth,
                                    newSurface.get_size(),
                                    bOffset, gOffset, rOffset,
                                    aOffset)
    else:
        print("ERROR in kivypixels.load_image:" +
              " file '" + fileName + "' does not exist")
    return returnKVI

class KPImage(PPImage):

    def __init__(self, size, byteDepth=4):
        super(KPImage, self).__init__(size, byteDepth=4)
        self.brushFileName = None
        self.brushOriginalImage = None  # no scale, no color
        self._brush_color = (1.0, 1.0, 1.0, 1.0)
        self.brushImage = None
        self.brushPixels = None
        self.brushSurface = None
        self.brushTexture = None

    def setBrushColor(self, color):
        #print("setting brush color to " + str(color))
        self._brush_color = color
        if self.brushImage is not None:
            self.brushImage.blit_copy(self.brushOriginalImage)
            self.brushImage.tintByColor(self._brush_color)
        else:
            raise ValueError("brushImage is None in setBrushColor"
                             " (you must call setBrushPath first)")

    def copyRuntimeVarsByRefFrom(self, kpimage):
        self.brushFileName = kpimage.brushFileName
        self.brushOriginalImage = kpimage.brushOriginalImage
        self._brush_color = kpimage._brush_color
        self.brushImage = kpimage.brushImage
        self.brushPixels = kpimage.brushPixels
        self.brushSurface = kpimage.brushSurface
        self.brushTexture = kpimage.brushTexture

    def setBrushPath(self, path):
        if os.path.isfile(path):
            self.brushFileName = path
            self.brushOriginalImage = load_image(self, path)
            print("loading brush '" + path + "'")
            if self.brushOriginalImage is not None:
                self.brushImage = KPImage(
                    self.brushOriginalImage.get_size(),
                    byteDepth=self.brushOriginalImage.byteDepth)
            else:
                raise ValueError("self.brushOriginalImage could not"
                                 " be loaded in setBrushPath")
        else:
            print("ERROR in setBrushPath: missing " + path +
                  "'")

    def load(self, fileName):
        self.lastUsedFileName = fileName
        newSurface = pygame.image.load(fileName)
        self.init(newSurface.get_size())
        data = pygame.image.tostring(newSurface, 'RGBA', False)
        # blit_copy_with_bo(self, inputArray, inputStride,
                          # inputByteDepth, input_size,
                          # bOffset, gOffset, rOffset, aOffset):

        newSurface_byteDepth = newSurface.get_bytesize()
            # int(newSurface.get_bitsize() / 8)
        newSurface_stride = newSurface.get_pitch()
            # newSurface.get_width() * newSurface_byteDepth
        bOffset = 0
        gOffset = 1
        rOffset = 2
        aOffset = 3
        KPImage.blit_copy_with_bo(self, data, newSurface_stride,
                                  newSurface_byteDepth,
                                  newSurface.get_size(),
                                  bOffset, gOffset, rOffset, aOffset)



    def saveAs(self, fileName):
        IsOK = None
        print("Saving '" + fileName + "'")
        # os.path.join(os.getcwd(), fileName)
        print("  current directory: " + os.getcwd())

        # self.updateVariableImageSize()
        # self.assumed_fbo_stride = (int(self.fbo.size[0]) *
                                   # self.assumed_fbo_byteDepth)
        # self.pixelBuffer.blit_copy_with_bo(self.fbo.pixels,
                                           # self.assumed_fbo_stride,
                                           # self.assumed_fbo_byteDepth,
                                           # self.fbo.size,
                                           # bOffset, gOffset, rOffset,
                                           # aOffset)
        try:
            if (self.enableDebug):
                print("self.size:"+str(self.size))
                print("len(self.data):"+str(len(self.data)))
                # print("self.getMaxChannelValueNotIncludingAlpha():" +
                      # str(self.getMaxChannelValueNotIncludingAlpha()))
                # print("self.getMaxAlphaValue():" +
                      # str(self.getMaxAlphaValue()))
            translatedImage = KPImage(self.size,
                                      byteDepth=self.byteDepth)


            # Kivy 1.8.0 channel offsets are:
            # bOffset = 2 #formerly 0 #blue comes from green channel
            # gOffset = 0 #formerly 1 #green comes from blue channel
            # rOffset = 1 #formerly 2
            # aOffset = 3 #formerly 3

            # since pygame.image.fromstring (or pygame.image.save??)
            # has odd (accidentally [??] errant) byte order,
            # channel offsets are:
            # translatedImage.bOffset = self.gOffset #such as 1
            # translatedImage.gOffset = self.bOffset #such as 0
            # translatedImage.rOffset = self.rOffset #such as 2
            # translatedImage.aOffset = self.aOffset #such as 3
            translatedImage.bOffset = 0
            translatedImage.gOffset = 1
            translatedImage.rOffset = 2
            translatedImage.aOffset = 3
            # NOTE: kivy's pygame.image.fromstring(data,
            # (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True)
            # is not at fault for channel order issue, and has correct
            # channel order
            translatedImage.blit_copy_with_bo(self.data, self.stride,
                                              self.byteDepth,
                                              self.size,
                                              self.bOffset,
                                              self.gOffset,
                                              self.rOffset,
                                              self.aOffset)
            data = bytes(translatedImage.data)  # convert from bytearray
                                                # to bytes
            if (self.enableDebug):
                debugX = 3
                debugY = self.height - 3
                if (debugX>=self.width):
                    debugX=self.width-1
                if (debugY>=self.height):
                    debugY=self.height-1
                debugIndex = debugY*self.stride + debugX*self.byteDepth
                print("debug pixel at (" + str(debugX) + "," +
                      str(debugY) + "): " +
                      bufferToTupleStyleString(data, debugIndex,
                      self.byteDepth)
                )
            surface = pygame.image.fromstring(data, self.size, 'RGBA',
                                              True)
            pygame.image.save(surface, fileName)

            IsOK = True
        except Exception as e:
            IsOK = False
            print("Could not finish saving: "+str(e))

        return IsOK

    def save(self):
        return self.saveAs(self.lastUsedFileName)

    def brushAt(self, centerX, centerY):
        # normalSize = self.brushImage.get_norm_image_size()
        # self.brushImage.size[0] = self.brushImage.size[0]
            # # int(normalSize[0])
        # self.brushImage.size[1] = self.brushImage.size[1]
            # # int(normalSize[1])

        # self.set_at(touch.x, touch.y, self._brush_color)
            # # dont' uncomment, since size of this is only set at
            # # Save now (not on_size)

        # self.assumed_fbo_stride = (int(self.fbo.size[0]) *
                                   # self.assumed_fbo_byteDepth)
        # self.array_set_at_GRBA(self.fbo.pixels, assumed_fbo_stride,
                               # assumed_fbo_byteDepth, touch.x,
                               # touch.y, _brush_color)
        # self.fbo.add(self._brush_color)
        # brushPoint = Point(points=(atX, atY))
        # self.fbo.add(brushPoint)
        # brushLine = Line(
            # points=[centerX, centerY, centerX+1, centerY], width=1)
        # self.fbo.add(brushLine)

        #destX = centerX - self.brushImage.center_x
        #destY = centerY - self.brushImage.center_y

        destX = int(centerX) - int(self.brushImage.size[0]/2)
        destY = int(centerY) - int(self.brushImage.size[1]/2)
        #destLineStartX = destX

        bOffset = self.bOffset
        gOffset = self.gOffset
        rOffset = self.rOffset
        aOffset = self.aOffset

        # brushBuffer_byteDepth = 4
        # brushBuffer_stride = int(self.brushImage.width) *
                             # brushBuffer_byteDepth
        src = self.brushImage.data  # self.brushPixels
        # d_bi:
        di = destY * self.stride + destX * self.byteDepth
        destLineStartIndex = di
        if self.enableDebug:
            print()
            print("self.brushImage.size:" +
                  str(self.brushImage.size))
            print("brushImage.byteDepth:" +
                  str(self.brushImage.byteDepth))
            print("brushImage.stride:" + str(self.brushImage.stride))
            print("self.stride:" + str(self.stride))
            print("self.byteDepth:" + str(self.byteDepth))
            print("d_bi:" + str(di))

        sourceLineStartIndex = 0
        debugPixelWriteCount = 0
        try:
            for sourceY in range(0,int(self.brushImage.size[1])):
                #destX = destLineStartX
                di = destLineStartIndex
                si = sourceLineStartIndex  # s_bi
                for sourceX in range(0,int(self.brushImage.size[0])):
                    sab = src[si + aOffset]  # src_a_i
                    # src_a:
                    a = sab/255.0
                    # src_inv_a:
                    ia = 1.0 - a
                    dab = self.data[di+aOffset]
                    da = dab/255.0

                    # si = sourceY * brushBuffer_stride +
                        # sourceX * brushBuffer_byteDepth
                    if (sab != 0):
                        # calculate resulting alpha:
                        # a_total_i = dab
                        # if sab > dab:
                            # a_total_i = sab
                        a_total_i = int(dab) + sab
                        if a_total_i>255:
                            a_total_i = 255

                        # do alpha formula on colors

                        # account for dest (color transparent more):
                        # (from here down, 'a' affects color not alpha)
                        dia = 1.0 - da
                        # use alpha formula to overlay 1.0 onto brush's
                        # alpha as dest alpha approaches 0.0 (dia 1.0)
                        # to remove black fringe around brush stroke
                        # ba = da*a  # both alpha
                        # bia = 1.0 - ba
                        # a = da*a + dia*1.0
                        # a = dia*a + dia*da
                        # a = ia*a + a*da
                        ia = 1.0 - a

                        # self.data[di+bOffset] = int(round(
                            # ia*float(self.data[di+bOffset]) +
                            # a*float(src[si+bOffset])))
                        # self.data[di+gOffset] = int(round(
                            # ia*float(self.data[di+gOffset]) +
                            # a*float(src[si+gOffset])))
                        # self.data[di+rOffset] = int(round(
                            # ia*float(self.data[di+rOffset]) +
                            # a*float(src[si+rOffset])))
                        # self.data[di+aOffset] = a_total_i

                        res = [int( ia*float(self.data[di+bOffset]) +
                                    a*float(src[si+bOffset]) + .5 ),
                               int( ia*float(self.data[di+gOffset]) +
                                    a*float(src[si+gOffset]) + .5 ),
                               int( ia*float(self.data[di+rOffset]) +
                                    a*float(src[si+rOffset]) + .5 ),
                               a_total_i]
                        # brushBGRABytes = bytes(res)
                        self.data[di+bOffset] = res[0]
                        self.data[di+gOffset] = res[1]
                        self.data[di+rOffset] = res[2]
                        self.data[di+aOffset] = res[3]

                        debugPixelWriteCount += 1
                    #destX += 1
                    di += self.byteDepth
                    si += self.brushImage.byteDepth
                #destY += 1
                destLineStartIndex += self.stride
                sourceLineStartIndex += self.brushImage.stride
        #except:
        except Exception as e:
            print("Could not finish brushAt: "+str(e))
            print("    d_bi:" + str(di) +
                  "; s_bi:" + str(si) +
                  "; len(self.data):" + str(len(self.data)) +
                  "; len(brushPixels):" + str(len(src)))
         # if (debugColor is not None):
             # print("debugColor:" + str(debugColor.b) +
                   # "," + str(debugColor.g) +
                   # "," + str(debugColor.r) +
                   # "," + str(debugColor.a))
         # else:
             # print("debugColor:None")
        # self.fbo.add(self._brush_color)
        # # brushRect = Rectangle(texture=self.brushTexture,
            # # pos = ((atX-self.brushImage.center_x,
                    # # atY-self.brushImage.center_y),
                  # # size=(self.brushImage.size[0],
                        # # self.brushImage.size[1]))
        # brushRect = Rectangle(texture=self.brushTexture,
                              # pos=(destX,destY),
                              # size=(self.brushImage.size[0],
                                    # self.brushImage.size[1]))
        # # brushRect = Rectangle(source=self.brushFileName,
                              # # pos=(touch.x,touch.y), size=(16,16))
        # self.fbo.add(brushRect)
        if self.enableDebug:
            print("debugPixelWriteCount:"+str(debugPixelWriteCount))

    def tintByColor(self, color):
        # thisPPColor = PPColor()
        # thisPPColor.setBytesFromRGBA(int(color.r*255.0+.5),
                                     # int(color.g*255.0+.5),
                                     # int(color.b*255.0+.5),
                                     # int(color.a*255.0+.5) )
        source_bOffset=0
        source_gOffset=1
        source_rOffset=2
        source_aOffset=3
        if len(color) < 4:
            color = vec4_from_vec3(color, 1.0)
        di = 0  # pixelByteIndex
        if (self.aOffset is not None):
            for pixelIndex in range(0,self.size[0]*self.size[1]):
                self.data[di+self.bOffset] = int(round(
                    float(self.data[di+self.bOffset]) *
                    color[source_bOffset]))
                self.data[di+self.gOffset] = int(round(
                    float(self.data[di+self.gOffset]) *
                    color[source_gOffset]))
                self.data[di+self.rOffset] = int(round(
                    float(self.data[di+self.rOffset]) *
                    color[source_rOffset]))
                self.data[di+self.aOffset] = int(round(
                    float(self.data[di+self.aOffset]) *
                    color[source_aOffset]))
                di += self.byteDepth
        elif (self.byteDepth==3):
            for pixelIndex in range(0,self.size[0]*self.size[1]):
                self.data[di+self.bOffset] = int(round(
                    float(self.data[di+self.bOffset]) *
                    color[source_bOffset]))
                self.data[di+self.gOffset] = int(round(
                    float(self.data[di+self.gOffset]) *
                    color[source_gOffset]))
                self.data[di+self.rOffset] = int(round(
                    float(self.data[di+self.rOffset]) *
                    color[source_rOffset]))
                di += self.byteDepth
        else:
            print("Not yet implemented KVImage tintByColor where" +
                  " self.byteDepth=" + str(self.byteDepth))

if __name__ == "__main__":
    print("This module should be imported by your program.")
    print("  tests:")
    size = (128, 128)
    src_img = KPImage(size)
    dst_img = KPImage(size)
    print("blit_copy_with_bo 32-bit...")
    print("  src_img: " + str(src_img.get_dict(data_enable=False)))
    print("  dst_img: " + str(dst_img.get_dict(data_enable=False)))
    dst_img.blit_copy_with_bo(src_img.data, src_img.stride,
        src_img.byteDepth, src_img.size, src_img.bOffset,
        src_img.gOffset, src_img.rOffset, src_img.aOffset)
    print("blit_copy_with_bo grayscale...")
    src_img = KPImage(size, byteDepth=1)
    dst_img = KPImage(size, byteDepth=1)
    print("  src_img: " + str(src_img.get_dict(data_enable=False)))
    print("  dst_img: " + str(dst_img.get_dict(data_enable=False)))
    dst_img.blit_copy_with_bo(src_img.data, src_img.stride,
        src_img.byteDepth, src_img.size, src_img.bOffset,
        src_img.gOffset, src_img.rOffset, src_img.aOffset)
    print("  done testing kivypixels.")


import os
import io
import time

try:
    import kivy
except ImportError as ex:
    print("This module requires kivy. Try:")
    print("python -m pip install --user --upgrade pip")
    print("python -m pip install --user --upgrade setuptools wheel")
    print("python -m pip install --user --upgrade kivy")
    raise ex

from kivy.resources import resource_find
# from pythonpixels import PPColor
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import Texture
# import timeit
# from timeit import default_timer as best_timer
pygame_enable = False
try:
    # kivy 1.8 and earlier:
    import pygame
    pygame_enable = True
except:
    pass
# except Exception as e:
# #   print("Could not finish importing pygame:"+str(e))
# from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
# try:
# #   # kivy 1.9.0 way:
# #   import io
# #   from kivy.uix.Image import Image
# #   #from kivy.core.image import Image as CoreImage
# except:
# #   pass

from kivypixels.common import view_traceback
from kivypixels.pythonpixels import PPImage, PPColor, vec4_from_vec3
from kivypixels.pythonpixels import bufferToTupleStyleString


def get_ext_lower(path):
    fileName, fileExtension = os.path.splitext(path)
    fileExtension = fileExtension[1:]
    return fileExtension.lower()


def load_image(self,fileName):
    result = None
    data = None
    participle = "(before initializing)"
    # if os.path.exists(fileName):
        # result = KPImage(1,1,4)
        # result.load(fileName)
        # return result

    try:
        if os.path.exists(fileName):
            try:
                #kivy 1.8.0 way:
                participle = "loading Kivy 1.8 image from file"
                newSurface = pygame.image.load(fileName)
                participle = "accessing Kivy 1.8 image attributes"
                result = KPImage(newSurface.get_size())
                participle = "getting data from Kivy 1.8 image"
                data = pygame.image.tostring(newSurface, 'RGBA', False)
                participle = "after loading image"
                newBD = newSurface.get_bytesize()
                # int(newSurface.get_bitsize()//8)
                newStride = newSurface.get_pitch()
                # newSurface.get_width() * newBD

                # Source offsets
                eB = 0
                eG = 1
                eR = 2
                eA = 3
                result.blit_copy_with_bo(data, newStride,
                                         newBD,
                                         newSurface.get_size(),
                                         eB, eG, eR, eA)
            except:
                # kivy 1.9.0 way:
                # participle = "loading Kivy 1.9 unparsed file as bytes"
                # compressed = io.BytesIO(open(fileName, "rb").read())
                # participle = ("loading Kivy 1.9 image from unparsed"
                # " file bytes")
                this_ext = get_ext_lower(fileName)
                # participle = ("loading Kivy 1.9 " + this_ext
                # + " format data from unparsed file bytes")
                # im = CoreImage(compressed, ext=this_ext,
                # filename=fileName, keep_data=True)
                im = im = CoreImage(fileName, keep_data=True)
                participle = ("accessing Kivy 1.9 image attributes"
                              " (after parsing " + this_ext
                              + " format)")
                result = KPImage((im.width, im.height))
                result.enableDebug = True
                result.drawKivyImage(im)
        else:
            print("ERROR in kivypixels.load_image:"
                  + " file '" + fileName + "' does not exist")
    except Exception as e:
        print("Could not finish {} in static_createFromImageFile: {}"
              "".format(participle, e))
    return result


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
        previousByteCount = self.byteCount
        try:
            if os.path.exists(fileName):
                try:
                    #kivy 1.8.0 way:
                    participle = "loading Kivy 1.8 image from file"
                    newSurface = pygame.image.load(fileName)
                    participle = "accessing Kivy 1.8 image attributes"
                    self.init(newSurface.get_size())
                    participle = "getting data from Kivy 1.8 image"
                    data = pygame.image.tostring(newSurface, 'RGBA',
                                                 False)
                    participle = "after loading image"
                    newBD = newSurface.get_bytesize()
                        # int(newSurface.get_bitsize() / 8)
                    newStride = newSurface.get_pitch()
                        # newSurface.get_width() * newBD
                    # source color locations:
                    eB = 0
                    eG = 1
                    eR = 2
                    eA = 3
                    self.blit_copy_with_bo(data, newStride,
                                           newBD,
                                           newSurface.get_size(),
                                           eB, eG, eR, eA)

                except:
                    # kivy 1.9.0 way:
                    # participle = ("loading Kivy 1.9 unparsed file as"
                    # " bytes")
                    # compressed = io.BytesIO(
                    # open(fileName, "rb").read()
                    # )
                    # participle = ("loading Kivy 1.9 image from"
                    # " unparsed file bytes")
                    this_ext = get_ext_lower(fileName)
                    # participle = ("loading Kivy 1.9 " + this_ext
                    # + " format data from unparsed file bytes")
                    # im = CoreImage(compressed, ext=this_ext,
                    # filename=fileName, keep_data=True)
                    im = CoreImage(fileName, keep_data=True)
                    participle = ("accessing Kivy 1.9 image attributes"
                                  " (after parsing {} format)"
                                  "".format(this_ext))
                    self.init((im.width, im.height))
                    self.enableDebug = True
                    participle = ("reading pixels from Kivy 1.9 image"
                                  " (after parsing {} format)"
                                  "".format(this_ext))
                    self.drawKivyImage(im)
            else:
                print("ERROR in KivyPixels.static_createFromImageFile:"
                      " file \"{}\"does not exist".format(fileName))
        #except Exception as e:
        #    print("Could not finish {} in load: {}"
        #    "".format(participle, e))
        except:
            print("Could not finish {} in static_createFromImageFile:"
                  "".format(participle))
            view_traceback()

    def getNew(self, size, byteDepth=4):
        return KPImage(size, byteDepth=byteDepth)

    def saveAs(self, fileName, flip_enable=False):
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
                                           # eB, eG, eR, eA)
        try:
            if (self.enableDebug):
                print("self.size:"+str(self.size))
                print("len(self.data):"+str(len(self.data)))
                # print("self.getMaxChannelValueNotIncludingAlpha():" +
                      # str(self.getMaxChannelValueNotIncludingAlpha()))
                # print("self.getMaxAlphaValue():" +
                      # str(self.getMaxAlphaValue()))

            if (self.enableDebug):
                debugX = 3
                debugY = self.size[1] - 3
                if (debugX>=self.size[0]):
                    debugX=self.size[0]-1
                if (debugY>=self.size[1]):
                    debugY=self.size[1]-1
                debugIndex = debugY*self.stride + debugX*self.byteDepth
                print("debug pixel at (" + str(debugX) + ","
                      + str(debugY) + "): "
                      + bufferToTupleStyleString(data, debugIndex,
                                                 self.byteDepth))
            if pygame_enable:  # Kivy 1.8 and earlier:

                translatedImage = KPImage(self.size,
                                          byteDepth=self.byteDepth)
                # Kivy 1.8.0 channel offsets are:
                # eB = 2 #formerly 0 #blue comes from green channel
                # eG = 0 #formerly 1 #green comes from blue channel
                # eR = 1 #formerly 2
                # eA = 3 #formerly 3

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
                # is not at fault for channel order issue, & has correct
                # channel order
                translatedImage.blit_copy_with_bo(self.data,
                                                  self.stride,
                                                  self.byteDepth,
                                                  self.size,
                                                  self.bOffset,
                                                  self.gOffset,
                                                  self.rOffset,
                                                  self.aOffset)
                data = bytes(translatedImage.data)
                # ^ convert from bytearray to bytes
                surface = pygame.image.fromstring(data, self.size,
                                                  'RGBA', True)
                pygame.image.save(surface, fileName)
            else:
                # Kivy 1.9.0+:
                # data = bytes(translatedImage.data)
                # ^ convert from bytearray to bytes
                # CoreImage can load io.BytesIO but must have
                # file header
                translatedImage = self
                print("  tricking Kivy so flipped warning won't"
                      " matter...")
                if not flip_enable:
                    # kivy texture is upside-down, so negate that:
                    print("  manually un-flipping")
                    translatedImage = self.copy_flipped_v()
                print("  saving...")
                this_texture = None
                if self.byteDepth == 4:
                    this_texture = Texture.create(size=self.size,
                                                  colorfmt='rgba',
                                                  bufferfmt='ubyte')
                    this_texture.blit_buffer(translatedImage.data,
                                             colorfmt='rgba',
                                             bufferfmt='ubyte')
                elif self.byteDepth == 3:
                    this_texture = Texture.create(size=self.size,
                                                  colorfmt='rgb',
                                                  bufferfmt='ubyte')
                    this_texture.blit_buffer(translatedImage.data,
                                             colorfmt='rgb',
                                             bufferfmt='ubyte')
                elif self.byteDepth == 1:
                    this_texture = Texture.create(size=self.size,
                                                  colorfmt='luminance',
                                                  bufferfmt='ubyte')
                    this_texture.blit_buffer(translatedImage.data,
                                             colorfmt='luminance',
                                             bufferfmt='ubyte')
                elif self.byteDepth == 2:
                    this_texture = Texture.create(size=self.size,
                                                  colorfmt='luminance',
                                                  bufferfmt='ushort')
                    this_texture.blit_buffer(translatedImage.data,
                                             colorfmt='luminance',
                                             bufferfmt='ushort')
                else:
                    print("NOT YET IMPLEMENTED: saving with this"
                          " byteDepth ({})".format(self.byteDepth))
                # See
                # https://kivy.org/docs/api-kivy.graphics.texture.html
                # im = CoreImage(bytes(translatedImage.data), ext="png")
                if this_texture is not None:
                    this_texture.save(fileName)
                    print("  saved.")
                    # im = CoreImage(this_texture)
                    # im.save(fileName, flipped=False)

            IsOK = True
        except:
            IsOK = False

            print("Could not finish saving: ")
            view_traceback()

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

        # internal offsets:
        iB = self.bOffset
        iG = self.gOffset
        iR = self.rOffset
        iA = self.aOffset

        # brushBuffer_byteDepth = 4
        # brushBuffer_stride = int(self.brushImage.size[0]) *
                             # brushBuffer_byteDepth
        src = self.brushImage.data  # self.brushPixels
        # d_bi:
        di = destY * self.stride + destX * self.byteDepth
        dstLSI = di  # destLineStartIndex
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

        srcLSI = 0
        debugPixelWriteCount = 0
        try:
            for sourceY in range(0,int(self.brushImage.size[1])):
                #destX = destLineStartX
                di = dstLSI
                si = srcLSI  # s_bi
                for sourceX in range(0,int(self.brushImage.size[0])):
                    sab = src[si+iA]  # src_a_i
                    # src_a:
                    a = sab/255.0
                    # src_inv_a:
                    ia = 1.0 - a
                    dab = self.data[di+iA]
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

                        # self.data[di+iB] = int(round(
                            # ia*float(self.data[di+iB]) +
                            # a*float(src[si+iB])))
                        # self.data[di+iG] = int(round(
                            # ia*float(self.data[di+iG]) +
                            # a*float(src[si+iG])))
                        # self.data[di+iR] = int(round(
                            # ia*float(self.data[di+iR]) +
                            # a*float(src[si+iR])))
                        # self.data[di+aOffset] = a_total_i

                        res = [int(ia*float(self.data[di+iB])
                                   + a*float(src[si+iB]) + .5),
                               int(ia*float(self.data[di+iG])
                                   + a*float(src[si+iG]) + .5),
                               int(ia*float(self.data[di+iR])
                                   + a*float(src[si+iR]) + .5),
                               a_total_i]
                        # brushBGRABytes = bytes(res)
                        self.data[di+iB] = res[0]
                        self.data[di+iG] = res[1]
                        self.data[di+iR] = res[2]
                        self.data[di+iA] = res[3]

                        debugPixelWriteCount += 1
                    # destX += 1
                    di += self.byteDepth
                    si += self.brushImage.byteDepth
                # destY += 1
                dstLSI += self.stride
                srcLSI += self.brushImage.stride
        except Exception as e:
            print("Could not finish brushAt: "+str(e))
            print("    d_bi:" + str(di) +
                  "; s_bi:" + str(si) +
                  "; len(self.data):" + str(len(self.data)) +
                  "; len(brushPixels):" + str(len(src)))
        if self.enableDebug:
            print("debugPixelWriteCount:"+str(debugPixelWriteCount))


    def drawKivyImage(self, thisKivyImage):
        maxAlpha = 0
        sourcePixelCount = 0

        # External (source in this case) channel offsets
        # (since may differ from self):
        eB = 0
        eG = 1
        eR = 2
        eA = 3

        # Internal offsets:
        iB = self.bOffset
        iG = self.gOffset
        iR = self.rOffset
        iA = self.aOffset

        dest_line_byte_index = 0
        dI = 0  # dest pixel byte index
        participle = "reading pixels"
        result_string = "FAIL"
        try:
            dest_line_byte_index = 0
            for y in range(self.size[1]):
                participle = "(no pixel yet)"
                dI = dest_line_byte_index
                if (y<thisKivyImage.size[1]):
                    for x in range(self.size[0]):
                        if (x<thisKivyImage.size[0]):
                            participle = "reading pixel"
                            color = thisKivyImage.read_pixel(x,y)
                            participle = "copying channels"
                            #+.5 for rounding:
                            thisA = int(255.0*color[eA]+.5)
                            self.data[dI + iB] = int(255.0*color[eB]+.5)
                            self.data[dI + iG] = int(255.0*color[eG]+.5)
                            self.data[dI + iR] = int(255.0*color[eR]+.5)
                            self.data[dI + iA] = thisA
                            participle = "after reading channels"
                            sourcePixelCount += 1
                            if (thisA>maxAlpha):
                                maxAlpha = thisA
                        else:
                            self.data[dI + iB] = 0
                            self.data[dI + iG] = 0
                            self.data[dI + iR] = 0
                            self.data[dI + iA] = 0
                        dI += self.byteDepth
                else:
                    for x in range(thisKivyImage.size[0]):
                        self.data[dI + iB] = 0
                        self.data[dI + iG] = 0
                        self.data[dI + iR] = 0
                        self.data[dI + iA] = 0
                        dI += self.byteDepth
                dest_line_byte_index += self.stride
            result_string = "OK"
        except:
            print("Could not finish " + participle + " drawKivyImage: ")
            view_traceback()
            print("dump:")
            print(self.get_dump())
        if self.enableDebug:
            print("drawKivyImage..." + result_string
                  + " {sourcePixelCount:" + str(sourcePixelCount)
                  + "; maxAlpha:" + str(maxAlpha)
                  + "; dest_line_byte_index:"
                  + str(dest_line_byte_index)
                  + "; dI:"
                  + str(dI) + "}")
            print()

    def tintByColorInstruction(self, colorInstruction):
        color = colorInstruction
        self.tintByColor( (color.b, color.g, color.r, color.a) )

    def tintByColor(self, colorVec4OrVec3):
        color = colorVec4OrVec3
        # thisPPColor = PPColor()
        # thisPPColor.setBytesFromRGBA(int(color.r*255.0+.5),
        # int(color.g*255.0+.5),
        # int(color.b*255.0+.5),
        # int(color.a*255.0+.5) )
        eB = 0
        eG = 1
        eR = 2
        eA = 3
        # Internal offsets:
        iB = self.bOffset
        iG = self.gOffset
        iR = self.rOffset
        iA = self.aOffset
        print("  tinting brush: "+str(color))
        if len(color) < 4:
            color = vec4_from_vec3(color, 1.0)
        di = 0  # pixelByteIndex
        try:
            if (iA is not None):
                for pixelIndex in range(0,self.size[0]*self.size[1]):
                    self.data[di+iB] = int(round(
                        float(self.data[di+iB])
                        * color[eB]))
                    self.data[di+iG] = int(round(
                        float(self.data[di+iG])
                        * color[eG]))
                    self.data[di+iR] = int(round(
                        float(self.data[di+iR])
                        * color[eR]))
                    self.data[di+iA] = int(round(
                        float(self.data[di+iA])
                        * color[eA]))
                    di += self.byteDepth
            elif (self.byteDepth==3):
                for pixelIndex in range(0,self.size[0]*self.size[1]):
                    self.data[di+iB] = int(round(
                        float(self.data[di+iB])
                        * color[eB]))
                    self.data[di+iG] = int(round(
                        float(self.data[di+iG])
                        * color[eG]))
                    self.data[di+iR] = int(round(
                        float(self.data[di+iR])
                        * color[eR]))
                    di += self.byteDepth
            else:
                print("Not yet implemented KVImage tintByColor where"
                      " self.byteDepth=" + str(self.byteDepth))
        except:
            print("Triggered alternate tintByColor algorithm:")
            view_traceback()
            try:
                di = 0
                totalCount = self.size[0]*self.size[1]
                if (iA is not None):
                    for pixelIndex in range(0, totalCount):
                        self.data[di+iB] = int(round(
                            float(self.data[di+iB]) * color.b
                        ))
                        self.data[di+iG] = int(round(
                            float(self.data[di+iG]) * color.g
                        ))
                        self.data[di+iR] = int(round(
                            float(self.data[di+iR]) * color.r
                        ))
                        self.data[di+iA] = int(round(
                            float(self.data[di+iA]) * color.a
                        ))
                        di += self.byteDepth
                elif (self.byteDepth==3):
                    for pixelIndex in range(0, totalCount):
                        self.data[di+iB] = int(
                            float(self.data[di+iB])
                            * color.b + .5
                        )  #+ .5 for rounding
                        self.data[di+iG] = int(
                            float(self.data[di+iG])
                            * color.g + .5
                        )  #+ .5 for rounding
                        self.data[di+iR] = int(
                            float(self.data[di+iR])
                            * color.r + .5
                        )  #+ .5 for rounding
                        di += self.byteDepth
                else:
                    print("Not yet implemented KVImage tintByColor"
                          " where self.byteDepth={}"
                          "".format(self.byteDepth))

            except:
                print("Could not finish KVImage tintByColor: color={}"
                      "".format(color))
                view_traceback()


if __name__ == "__main__":
    print("kivypixels should be imported by your program not run.")


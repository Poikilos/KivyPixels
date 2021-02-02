#!/usr/bin/env python

try:
    import kivy
except ImportError as ex:
    print("This program requires kivy. Try:")
    print("python -m pip install --user --upgrade pip")
    print("python -m pip install --user --upgrade setuptools wheel")
    print("python -m pip install --user --upgrade kivy")
    exit(1)

from kivypixels import KPImage #, load_image
from kivy.uix.widget import Widget
from kivy.graphics import Fbo, ClearColor, ClearBuffers
# from kivy.graphics.fbo import Fbo
from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Canvas, Color, Rectangle
from kivypixels.pythonpixels import ibgr_from_hex  # , vec4_from_vec3


class PixelWidget(Widget):
    enableDebug = False
    texture = ObjectProperty(None, allownone=True)
    alpha = NumericProperty(1)
    viewImage = None
    # TOTALBYTECOUNT = None
    # TOTALPIXELCOUNT = None
    # STRIDE = None
    # viewImage = None
    # assumed_fbo_byteDepth = 4
    # assumed_fbo_stride = None

    # brushFboWidgetSimple = None

    saveButton = None

    colorI = None
    # brushFileName = "brushTrianglePointingDown-25percent.png"
    _brush_color = None
    brushOriginalImage = None
    brushImage = None
    paletteWidget = None

    def __init__(self, **kwargs):
        # super(PixelWidget, self).__init__(**kwargs)
        Widget.__init__(self, **kwargs)
        self.canvas = Canvas()
        with self.canvas:
            self.fbo = Fbo(size=self.size)
            self.fbo_color = Color(1, 1, 1, 1)
            self.fbo_rect = Rectangle()

        with self.fbo:
            ClearColor(0, 0, 0, 0)
            ClearBuffers()

        # wait that all the instructions are in the canvas to set
        # texture
        self.texture = self.fbo.texture

        self.viewImage = KPImage(self.fbo.size)
        # Since in kivy's pygame.image.fromstring(data, (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True)
        #   saves with odd (errant??) byte order,
        #   channel offsets are:
        self.viewImage_bOffset = 2 #bOffset = 0 #blue comes from green channel
        self.viewImage_gOffset = 0 #gOffset = 1 #green comes from blue channel
        self.viewImage_rOffset = 1 #rOffset = 2
        self.viewImage_aOffset = 3 #aOffset = 3
        self.viewImage.bOffset=self.viewImage_bOffset
        self.viewImage.gOffset=self.viewImage_gOffset
        self.viewImage.rOffset=self.viewImage_rOffset
        self.viewImage.aOffset=self.viewImage_aOffset

        # self.viewImage.fill_icolor(0, 0, 0, 255)
        print("size:"+str(self.viewImage.size))
        # print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
        # print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))

        self.viewImage.setBrushPath("brush2.png")
        self.viewImage.setBrushColor((1,1,1,1))
        # self.brushImage = Image(source=self.brushFileName, keep_data=True)
        # self.brushImage = CoreImage(self.brushFileName)

        # self.brushTexture = self.brushImage.texture

        self.palettes = {}
        # CGA palette names:
        self.palettes["CGA"] = ["black", "blue", "green", "cyan",
                      "red", "magenta", "brown", "light gray",
                      "gray", "light blue", "light green", "light cyan",
                      "light red", "light magenta", "yellow", "white"]
        # CGA palette:
        self.paletteColors = {}
        self.paletteColors['black'] = ibgr_from_hex('000000')
        self.paletteColors['blue'] = ibgr_from_hex('0000AA')
        self.paletteColors['green'] = ibgr_from_hex('00AA00')
        self.paletteColors['cyan'] = ibgr_from_hex('00AAAA')
        self.paletteColors['red'] = ibgr_from_hex('AA0000')
        self.paletteColors['magenta'] = ibgr_from_hex('AA00AA')
        self.paletteColors['brown'] = ibgr_from_hex('AA5500')
            # or sometimes dark yellow AAAA00 such as early RCA monitors
        self.paletteColors['light gray'] = ibgr_from_hex('AAAAAA')
        self.paletteColors['gray'] = ibgr_from_hex('555555')
        self.paletteColors['light blue'] = ibgr_from_hex('5555FF')
        self.paletteColors['light green'] = ibgr_from_hex('55FF55')
        self.paletteColors['light cyan'] = ibgr_from_hex('55FFFF')
        self.paletteColors['light red'] = ibgr_from_hex('FF5555')
        self.paletteColors['light magenta'] = ibgr_from_hex('FF55FF')
        self.paletteColors['yellow'] = ibgr_from_hex('FFFF55')
        self.paletteColors['white'] = ibgr_from_hex('FFFFFF')
        self.updateColorNames()



        # self.brushFboWidgetSimple = FboWidgetSimple()
        # self.add_widget(self.brushFboWidgetSimple)
        # self.brushFboWidgetSimple.size = self.brushImage.size
        # TODO: see if Kivy app can use pygame.sprite.Sprite
        # self.brushPixels = self.brushSurface.tostring()

        # brushFboRectangle = Rectangle(
            # texture=self.brushTexture,
            # pos=(0,0),
            # size=self.brushImage.size)
        # self.brushFboWidgetSimple.fbo.add(brushFboRectangle)


        # self.texture = Texture.create(size=(512, 512),
                                      # colorfmt='RGBA',
                                      # bufferfmt='ubyte')
        # self.texture.add_reload_observer(self.populate_texture)
        # self.fbo.texture.add_reload_observer(
            # self.fbo_populate_texture)
        # self.populate_texture(self.texture)
        # self.populate_texture(self.fbo.texture)

    # def populate_texture(self, texture):
        # texture.blit_buffer(bytes(self.viewImage.data))

    # def fbo_populate_texture(self, texture):
        # texture.blit_buffer(bytes(self.viewImage.data))

    # def add_widget(self, *largs):
        # # trick to attach graphics instruction to fbo instead of
        # # canvas
        # canvas = self.canvas
        # self.canvas = self.fbo
        # ret = super(PixelWidget, self).add_widget(*largs)
        # self.canvas = canvas
        # return ret

    # def remove_widget(self, *largs):
        # canvas = self.canvas
        # self.canvas = self.fbo
        # super(PixelWidget, self).remove_widget(*largs)
        # self.canvas = canvas

    def updateColorNames(self):
        self.colorNames = []
        for k, v in self.paletteColors.items():
            self.colorNames.append(k)

    def updatePixelViewSize(self):
        if ((self.fbo.size[0]!=self.viewImage.size[0]) or
                (self.fbo.size[1]!=self.viewImage.size[1])):
            newKPImage = KPImage(self.fbo.size)
            newKPImage.blit_copy(self.viewImage)
            newKPImage.copyRuntimeVarsByRefFrom(self.viewImage)
            self.viewImage = newKPImage
            self.viewImage.bOffset=self.viewImage_bOffset
            self.viewImage.gOffset=self.viewImage_gOffset
            self.viewImage.rOffset=self.viewImage_rOffset
            self.viewImage.aOffset=self.viewImage_aOffset


            print("size:" + str(self.viewImage.size))
            # print("TOTALBYTECOUNT:" + str(self.TOTALBYTECOUNT))
            # print("TOTALPIXELCOUNT:" + str(self.TOTALPIXELCOUNT))

    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value
        tenthOfW = int(self.fbo_rect.size[0] / 10)
        if tenthOfW < 1:
            tenthOfW = 1
        tenthOfH = int(self.fbo_rect.size[1] / 10)
        if tenthOfH < 1:
            tenthOfH = 1

        if (self.saveButton is not None):
            self.saveButton.width = tenthOfW * 2
            self.saveButton.height = tenthOfH
        # if (self.brushImage is not None):
            # pass
            # self.brushImage.size = (tenthOfW, tenthOfW)
        self.updatePixelViewSize()
        self.uploadBufferToTexture()

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_alpha(self, instance, value):
        self.fbo_color.rgba = (1, 1, 1, value)

    def setBrushColorToNextInPalette(self, forward=True):
        if (self.colorI is None):
            self.colorI = 0
        else:
            if forward:
                self.colorI += 1
            else:
                self.colorI -= 1
        if (self.colorI>=len(self.colorNames)):
            self.colorI=0
        elif (self.colorI<0):
            self.colorI = len(self.colorNames) - 1
        selectedColor = self.paletteColors[self.colorNames[self.colorI]]
        print("Selected color " + str(self.colorI) + ": " + str(selectedColor))
        self.viewImage.setBrushColor(selectedColor)

    def on_touch_down(self, touch):
        super(PixelWidget, self).on_touch_down(touch)
        #if touch.button == "scrollup":
        #    self.setBrushColorToNextInPalette(True)
        #elif touch.button == "scrolldown":
        #    self.setBrushColorToNextInPalette(False)
        # # self.setBrushColorToNextInPalette()
        # color = self.paletteWidget.pickedColor
        # # color3 = color.r/255.0, color.g/255.0, color.b/255.0
        # # color3 = self.paletteWidget.pickedColor.rgb
        # color3 = color[0], color[1], color[2]
        # # print("pickedColor: " + str(color3))
        if touch.button == "middle":
            # TODO: fix this (use manually-managed pixel widget)
            self.paletteWidget.open()
            self.paletteWidget.adjust_rects()
        else:
            print("touch.button:"+str(touch.button))
            if str(touch.button) == "scrollup":
                self.setBrushColorToNextInPalette(forward=False)
            elif str(touch.button) == "scrolldown":
                self.setBrushColorToNextInPalette()
            # else:
                # self.setBrushColor(self.paletteWidget.pickedColor)
            # self.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
            self.viewImage.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
            self.uploadBufferToTexture()

    def on_touch_move(self, touch):
        super(PixelWidget, self).on_touch_move(touch)
        # self.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
        self.viewImage.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
        self.uploadBufferToTexture()

    def uploadBufferToTexture(self):
        # formerly used ImageData (decided to not use core.ImageData --
        # didn't seem to work in Kivy 1.8.0): https://groups.google.com/
        # forum/#!topic/kivy-users/3jYJtVk5vPQ
        self.texture.blit_buffer(bytes(self.viewImage.data),
                                 colorfmt='rgba', bufferfmt='ubyte')
        # NOTE: blit_buffer has no return
        # self.ask_update()  # does nothing
        self.canvas.ask_update()

    def onSaveButtonClick(self,instance):
        # see C:\Kivy-1.8.0-py3.3-win32\kivy\kivy\tests\test_graphics.py
        # data = self.fbo.pixels
        saveFileName = "Untitled1.png"
        index = 1
        while os.path.isfile(saveFileName):
            index += 1
            saveFileName = "Untitled"+str(index)+".png"
        self.viewImage.saveAs(saveFileName)
        if self.enableDebug:
            if self.brushImage is not None:
                self.brushImage.saveAs("debug-save-brush.png")

   # def onColorButtonClick(self,instance):
       # self.paletteWidget.open()

#     def onEraserButtonClick(self, instance):
#         #TODO: finish this
#         print("eraser")

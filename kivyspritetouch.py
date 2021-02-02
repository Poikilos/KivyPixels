'''
KivySpriteTouch
==========
based on http://kivy.org/docs/examples/gen__canvas__fbo_canvas__py.html

'''
try:
    import kivy
except ImportError as ex:
    print("This program requires kivy. Try:")
    print("python -m pip install --user --upgrade pip")
    print("python -m pip install --user --upgrade setuptools wheel")
    print("python -m pip install --user --upgrade kivy")
    exit(1)

from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.colorpicker import ColorPicker
# from kivy.uix.button import Button
from kivy.uix.popup import Popup
import os
from kivy.graphics.instructions import InstructionGroup

__all__ = ('PixelWidget', )

from kivy.graphics import Color, Rectangle, Canvas
#from kivy.graphics import ClearBuffers, ClearColor
#from kivy.graphics import Line
#from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.app import App
#from kivy.core.window import Window
#from kivy.animation import Animation
from kivy.factory import Factory

from kivy.uix.widget import Widget
from kivy.graphics import Fbo, ClearColor, ClearBuffers
#from kivy.graphics import Ellipse
#from kivy.uix.image import Image
#from kivy.core.image import Image as CoreImage

#import os
#from kivy.graphics import Point
#import random
#TODO: implement resize
#from array import array

#from pythonpixels import PPImage
#from pythonpixels import PPColor
from kivypixels import KPImage, load_image
#class MainForm(BoxLayout):
from pythonpixels import vec4_from_vec3, ibgr_from_hex

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


def component_to_id(component):
    return str(component).replace(".", "o")


def color_to_id(color):
    return ("color_" + component_to_id(color[0])
            + "_" + component_to_id(color[1])
            + "_" + component_to_id(color[2])
            + "_" + component_to_id(color[3]))


class ColorPopup(Popup):
    # ends up as ObservableList, not Color for some reason:
    pickedColor = Color(1,1,1,1)
    # pickedColor = (1.0, 1.0, 1.0, 1.0)
    title = "Color Selector"
    mainBoxLayout = None
    # mainColorPicker = None
    buttonBoxLayout = None
    okButton = None
    cancelButton = None
    row_lists = None
    #isStillPushingColorButton = None
    #content = content

    def adjust_rects(self):
        if self.row_lists is not None:
            self.free_widget.size = self.mainBoxLayout.size
            self.free_widget.pos = self.mainBoxLayout.pos
            cell_w = self.free_widget.size[0] / 16
            cell_h = self.free_widget.size[1] / 16
            print("adjust_rects...")
            print("  self.free_widget.size: "+str(self.free_widget.size))
            print("  cell size:"+str( (cell_w, cell_h) ))
            for y in range(0,16):
                for x in range(0,16):
                    #self.row_lists[y][x]["rect"].pos = (x*cell_w, y*cell_h)
                    #self.row_lists[y][x]["rect"].size = (cell_w, cell_h)
                    self.row_lists[y][x].pos = (x*cell_w, y*cell_h)
                    self.row_lists[y][x].size = (cell_w, cell_h)
                    print("Color: "+str(self.row_lists[y][x].id))
                    #print("Color: "+str( (self.row_lists[y][x]["ci"].r, \
                    #                      self.row_lists[y][x]["ci"].g, \
                    #                      self.row_lists[y][x]["ci"].b ) ) )

    def __init__(self, **kwargs):
        # super(ColorPopup, self).__init__(**kwargs)
        Popup.__init__(self, **kwargs)
        self.row_lists = list()
        self.mainBoxLayout = BoxLayout(orientation='vertical')
        self.add_widget(self.mainBoxLayout)
        #self.isStillPushingColorButton = True

        # self.mainColorPicker = ColorPicker()
        #self.mainColorPicker.color = self.pickedColor
        # self.mainBoxLayout.add_widget(self.mainColorPicker)

        self.buttonBoxLayout = BoxLayout(orientation='horizontal')
        self.buttonBoxLayout.size_hint=(1.0,.2)
        self.mainBoxLayout.add_widget(self.buttonBoxLayout)

        self.colors_v_layout = BoxLayout(orientation='vertical')
        self.free_widget = FloatLayout(size_hint=(1.0, 1.0), size=self.mainBoxLayout.size)
        #self.mainBoxLayout.add_widget(self.colors_v_layout)
        self.mainBoxLayout.add_widget(self.free_widget)
        cell_w = self.free_widget.size[0] / 16
        cell_h = self.free_widget.size[1] / 16
        for y in range(0,16):
            #this_h_layout = BoxLayout(orientation='horizontal')
            #self.colors_v_layout.add_widget(this_h_layout)
            this_list = list()
            for x in range(0,16):
                color = [x*16.0/256.0,y*16.0/256.0,0, 1.0]
                #this_rect = Rectangle(pos=(x*cell_w,y*cell_h), \
                #                      size=(cell_w,cell_h) \
                #                      )
                #_color_instruction = Color(r=color[0], g=color[1], b=color[2], a=1.0)
                #self.free_widget.canvas.add(_color_instruction)
                #self.free_widget.canvas.add(this_rect)
                idStr = color_to_id(color)
                this_button = Factory.Button(background_color=color)
                # id=idStr ID is not a string!
                self.free_widget.add_widget(this_button)
                #this_button.canvas_before.add(_color_instruction)
                #this_dict = dict()
                #this_dict["rect"] = this_rect
                #this_dict["ci"] = _color_instruction
                print("C:"+idStr)
                #print(" == Color: "+str( (_color_instruction.r, \
                #                         _color_instruction.g, \
                #                          _color_instruction.b ) ) )
                #this_list.append(this_dict)
                this_list.append(this_button)
                #this_h_layout.add_widget(Rectangle(color=(x,y,128)))
            self.row_lists.append(this_list)

        # self.okButton = Factory.Button(text="OK")
        # self.okButton.bind(on_press=self.onOKButtonClick)
        # self.buttonBoxLayout.add_widget(self.okButton)

        # self.cancelButton = Factory.Button(text="Cancel")
        # self.cancelButton.bind(on_press=self.onCancelButtonClick)
        # self.buttonBoxLayout.add_widget(self.cancelButton)

        # self.bind(on_touch_up=self.onAnyClick)
        # self.bind(on_dismiss=self.onDismiss)

#    def onOKButtonClick(self, instance):
#        #root.dismiss()
#        self.pickedColor = self.mainColorPicker.color
#        #self.isStillPushingColorButton = True
#        self.dismiss()
#
#    def onCancelButtonClick(self, instance):
#        #root.dismiss()
#        #self.isStillPushingColorButton = True
#        self.dismiss()

#     def onAnyClick(self, touch, *largs):
#         if not self.isStillPushingColorButton:
#             self.pickedColor = self.mainColorPicker.color
#             self.isStillPushingColorButton = True
#             self.dismiss()
#         self.isStillPushingColorButton = False

#     def onDismiss(self, instance):
#         self.isStillPushingColorButton = True


class KivySpriteTouchApp(App):

    mainWidget = None
    buttonsLayout = None

    saveButton = None
    colorButton = None
    eraserButton = None

    def build(self):
        self.pixelWidget = None

        self.mainWidget = BoxLayout(orientation='horizontal')

        self.pixelWidget = PixelWidget()
        self.mainWidget.add_widget(self.pixelWidget)

        self.buttonsLayout = BoxLayout(orientation='vertical',
                                       size_hint=(.1,1.0))
        self.mainWidget.add_widget(self.buttonsLayout)

        self.paletteWidget = ColorPopup(size_hint=(.9,.8))

        self.saveButton = Factory.Button(text="Save")
        # id="saveButton"
        self.buttonsLayout.add_widget(self.saveButton)
        self.saveButton.bind(on_press=self.pixelWidget.onSaveButtonClick)

        #self.paletteButton = Factory.Button(text="Save")
        # id="paletteButton"
        #self.buttonsLayout.add_widget(self.paletteButton)
        #self.paletteButton.bind(on_press=self.paletteWidget.open())

        # self.colorButton = Factory.Button(text="Color",
                                          # id="colorButton")
        # self.buttonsLayout.add_widget(self.colorButton)
        # self.colorButton.bind(on_press=self.pixelWidget.onColorButtonClick)

        # self.eraserButton = Factory.Button(text="Eraser",
                                           # id="eraserButton")
        # self.buttonsLayout.add_widget(self.eraserButton)
        # self.eraserButton.bind(
            # on_press=self.pixelWidget.onEraserButtonClick)

        return self.mainWidget

    def saveBrush(self):
        if self.brushImage is not None:
            self.brushImage.saveAs("debug save (brush).png")
        # normalSize = self.brushImage.get_norm_image_size()
        # self.brushImage.size = (int(normalSize[0]), int(normalSize[1]))
        # data = bytes(self.brushImage.data)
            # # convert from bytearray to bytes
        # surface = pygame.image.fromstring(data,
            # self.brushImage.size,
            # 'RGBA',
            # True)
        # pygame.image.save(surface, "debug save (brush).png")


if __name__ == "__main__":
    KivySpriteTouchApp().run()

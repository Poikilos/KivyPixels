
'''
KivySpriteTouch
==========
based on http://kivy.org/docs/examples/gen__canvas__fbo_canvas__py.html

'''
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.button import Button
from kivy.uix.popup import Popup

'''
# TODO: Animated Sprites
# see http://kivy.org/docs/api-kivy.uix.image.html
animatedImage = Image(source='animated.gif')
# animatedImage = AsyncImage(source='animated.gif')
# options:
# allow_stretch=True #default is False
# keep_ratio=False #default is True
# color = Color(rMultiplier, gMultiplier, bMultiplier, aMultiplier)
    # # ListProperty; default is [1,1,1,1]
# keep_data = True  # keeps the raw pixels such as for pixel-based
    # # collision detection; default is False
# anim_delay=-1 #-1 is stop; default is .25 (4fps)
# animatedImage.reload() #if file was loaded, you can reload it
# anim_loop=1 #0 is infinite


'''

'''

this program does not use kv language such as:
<ColorSelector>:
    color: 1, 1, 1, 1
    title: 'Color Selector'
    content:content
    BoxLayout:
        id: content
        orientation: 'vertical'
        ColorPicker:
            id: clr_picker
            color: root.color
            on_touch_up:
                root.color = clr_picker.color
                root.dismiss()
        BoxLayout:
            size_hint_y: None
            height: '27sp'
            Button:
                text: 'ok'
                on_release:
                    root.color = clr_picker.color
                    root.dismiss()
            Button:
                text: 'cancel'
                on_release: root.dismiss()

'''
__all__ = ('PixelWidget', )

from kivy.graphics import Color, Rectangle, Canvas
#from kivy.graphics import ClearBuffers, ClearColor
#from kivy.graphics import Line
#from kivy.graphics.fbo import Fbo
#from kivy.uix.floatlayout import FloatLayout
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
from kivypixels import KPImage
#class MainForm(BoxLayout):
from pythonpixels import vec4_from_vec3, bgr_from_hex

class PixelWidget(Widget):
    debugEnabled = False
    texture = ObjectProperty(None, allownone=True)
    alpha = NumericProperty(1)
    viewImage = None
    #TOTALBYTECOUNT = None
    #TOTALPIXELCOUNT = None
    #STRIDE = None
    #viewImage = None
    #assumed_fbo_byteDepth = 4
    #assumed_fbo_stride = None

    #brushFboWidgetSimple = None

    saveButton = None

    brushPaletteIndex = None
    #brushFileName = "brushTrianglePointingDown-25percent.png"

    paletteWidget = None

    def __init__(self, **kwargs):
        super(PixelWidget, self).__init__(**kwargs)
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
        # self.viewImage.fill_icolor(0, 0, 0,
                                                           # 255)
        print("size:"+str(self.viewImage.size))
        # print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
        # print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))
        self.viewImage.setBrushPath("brush2.png")
        self.viewImage.setBrushColor(bgr_from_hex('FFFFFF'))
        # self.brushImage = Image(source=self.brushFileName,
                                # keep_data=True)
        # self.brushImage = CoreImage(self.brushFileName)

        # self.brushTexture = self.brushImage.texture
        # CGA palette names:
        self.names = ["black", "blue", "green", "cyan",
                      "red", "magenta", "brown", "light gray",
                      "gray", "light blue", "light green", "light cyan",
                      "light red", "light magenta", "yellow", "white"]
        # CGA palette:
        self.paletteColors = {}
        self.paletteColors['black'] = bgr_from_hex('000000')
        self.paletteColors['blue'] = bgr_from_hex('0000AA')
        self.paletteColors['green'] = bgr_from_hex('00AA00')
        self.paletteColors['cyan'] = bgr_from_hex('00AAAA')
        self.paletteColors['red'] = bgr_from_hex('AA0000')
        self.paletteColors['magenta'] = bgr_from_hex('AA00AA')
        self.paletteColors['brown'] = bgr_from_hex('AA5500')
            # or sometimes dark yellow AAAA00 such as early RCA monitors
        self.paletteColors['light gray'] = bgr_from_hex('AAAAAA')
        self.paletteColors['gray'] = bgr_from_hex('555555')
        self.paletteColors['light blue'] = bgr_from_hex('5555FF')
        self.paletteColors['light green'] = bgr_from_hex('55FF55')
        self.paletteColors['light cyan'] = bgr_from_hex('55FFFF')
        self.paletteColors['light red'] = bgr_from_hex('FF5555')
        self.paletteColors['light magenta'] = bgr_from_hex('FF55FF')
        self.paletteColors['yellow'] = bgr_from_hex('FFFF55')
        self.paletteColors['white'] = bgr_from_hex('FFFFFF')




        # self.brushFboWidgetSimple = FboWidgetSimple()
        # self.add_widget(self.brushFboWidgetSimple)
        # self.brushFboWidgetSimple.width = self.brushImage.width
        # self.brushFboWidgetSimple.height = self.brushImage.height
        # TODO: see if Kivy app can use pygame.sprite.Sprite
        # self.brushPixels = self.brushSurface.tostring()

        # brushFboRectangle = Rectangle(
            # texture=self.brushTexture,
            # pos=(0,0),
            # size=(self.brushImage.width,self.brushImage.height))
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

    def updatePixelViewSize(self):
        if ((self.fbo.size[0]!=self.viewImage.size[0]) or
                (self.fbo.size[1]!=self.viewImage.size[1])):
            newKPImage = KPImage(self.fbo.size)
            newKPImage.blit_copy(self.viewImage)
            newKPImage.copyRuntimeVarsByRefFrom(self.viewImage)
            self.viewImage = newKPImage

            print("size:" + str(self.viewImage.size))
            # print("TOTALBYTECOUNT:" + str(self.TOTALBYTECOUNT))
            # print("TOTALPIXELCOUNT:" + str(self.TOTALPIXELCOUNT))

    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value

        if (self.saveButton is not None):
            self.saveButton.width=self.fbo_rect.size[0]/5
            self.saveButton.height=self.fbo_rect.size[1]/10
        # if (self.brushImage is not None):
        #     pass
            # self.brushImage.width=self.fbo_rect.size[0]/10
            # self.brushImage.height=self.brushImage.width
        self.updatePixelViewSize()
        self.uploadBufferToTexture()

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_alpha(self, instance, value):
        self.fbo_color.rgba = (1, 1, 1, value)

    def setBrushColor_to_next_in_palette(self):
        if (self.brushPaletteIndex is None):
            self.brushPaletteIndex = 0
        else:
            self.brushPaletteIndex += 1
        if (self.brushPaletteIndex>=len(self.names)):
            self.brushPaletteIndex=0
        self.viewImage.setBrushColor(
            self.paletteColors[self.names[self.brushPaletteIndex]])

    def on_touch_down(self, touch):
        super(PixelWidget, self).on_touch_down(touch)
        # self.setBrushColor_to_next_in_palette()
        color = self.paletteWidget.pickedColor
        # color3 = color.r/255.0, color.g/255.0, color.b/255.0
        # color3 = self.paletteWidget.pickedColor.rgb
        color3 = color[0], color[1], color[2]
        # print("pickedColor: " + str(color3))
        self.viewImage.setBrushColor(color3)
        self.viewImage.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
        self.uploadBufferToTexture()

    def on_touch_move(self, touch):
        super(PixelWidget, self).on_touch_move(touch)
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
        # saveFileName = "Untitled1.png"
        self.viewImage.saveAs("Untitled1.png")
        if self.debugEnabled:
            self.brushImage.saveAs("debug-save-brush.png")

    def onColorButtonClick(self,instance):
        self.paletteWidget.open()

#     def onEraserButtonClick(self, instance):
#         #TODO: finish this
#         print("eraser")

class ColorPopup(Popup):
    # ends up as ObservableList, not Color for some reason:
    # pickedColor = Color(1,1,1,1)
    pickedColor = (1.0,1.0,1.0,1.0)
    title = "Color Selector"
    mainBoxLayout = None
    mainColorPicker = None
    buttonBoxLayout = None
    okButton = None
    cancelButton = None
    #isStillPushingColorButton = None
    #content = content
    def __init__(self, **kwargs):
        super(ColorPopup, self).__init__(**kwargs)

        self.mainBoxLayout = BoxLayout(orientation='vertical')
        self.add_widget(self.mainBoxLayout)
        #self.isStillPushingColorButton = True

        self.mainColorPicker = ColorPicker()
        #self.mainColorPicker.color = self.pickedColor
        self.mainBoxLayout.add_widget(self.mainColorPicker)

        self.buttonBoxLayout = BoxLayout(orientation='horizontal')
        self.buttonBoxLayout.size_hint=(1.0,.2)
        self.mainBoxLayout.add_widget(self.buttonBoxLayout)


        self.okButton = Button(text="OK")
        self.okButton.bind(on_press=self.onOKButtonClick)
        self.buttonBoxLayout.add_widget(self.okButton)

        self.cancelButton = Button(text="Cancel")
        self.cancelButton.bind(on_press=self.onCancelButtonClick)
        self.buttonBoxLayout.add_widget(self.cancelButton)

        #self.bind(on_touch_up=self.onAnyClick)
        #self.bind(on_dismiss=self.onDismiss)

    def onOKButtonClick(self, instance):
        #root.dismiss()
        self.pickedColor = self.mainColorPicker.color
        #self.isStillPushingColorButton = True
        self.dismiss()

    def onCancelButtonClick(self, instance):
        #root.dismiss()
        #self.isStillPushingColorButton = True
        self.dismiss()

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
    pixelWidget = None
    saveButton = None
    colorButton = None
    eraserButton = None

    def build(self):

        self.mainWidget = BoxLayout(orientation='horizontal')

        pixelWidget = PixelWidget()
        self.mainWidget.add_widget(pixelWidget)

        self.buttonsLayout = BoxLayout(orientation='vertical',
                                       size_hint=(.1,1.0))
        self.mainWidget.add_widget(self.buttonsLayout)

        pixelWidget.paletteWidget = ColorPopup(size_hint=(.9,.5))

        self.saveButton = Factory.Button(text="Save", id="saveButton")
        self.buttonsLayout.add_widget(self.saveButton)
        self.saveButton.bind(on_press=pixelWidget.onSaveButtonClick)

        self.colorButton = Factory.Button(text="Color",
                                          id="colorButton")
        self.buttonsLayout.add_widget(self.colorButton)
        self.colorButton.bind(on_press=pixelWidget.onColorButtonClick)

        # self.eraserButton = Factory.Button(text="Eraser",
                                           # id="eraserButton")
        # self.buttonsLayout.add_widget(self.eraserButton)
        # self.eraserButton.bind(
            # on_press=pixelWidget.onEraserButtonClick)

        return self.mainWidget

    def saveBrush(self):
        self.brushImage.saveAs("debug save (brush).png")
        # normalSize = self.brushImage.get_norm_image_size()
        # self.brushImage.width = int(normalSize[0])
        # self.brushImage.height = int(normalSize[1])
        # data = bytes(self.brushImage.data)
            # # convert from bytearray to bytes
        # surface = pygame.image.fromstring(data,
            # (self.brushImage.width, self.brushImage.height),
            # 'RGBA',
            # True)
        # pygame.image.save(surface, "debug save (brush).png")


if __name__ == "__main__":
    KivySpriteTouchApp().run()

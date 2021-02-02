#!/usr/bin/env python
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
#class MainForm(BoxLayout):
from kivypixels.pythonpixels import vec4_from_vec3, ibgr_from_hex



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

        self.paletteButton = Factory.Button(text="Palette")
        # id="paletteButton"
        self.buttonsLayout.add_widget(self.paletteButton)
        self.paletteButton.bind(on_press=self.paletteWidget.open)

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

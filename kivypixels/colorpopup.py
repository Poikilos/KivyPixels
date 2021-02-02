#!/usr/bin/env python
import colorsys

try:
    import kivy
except ImportError as ex:
    print("This program requires kivy. Try:")
    print("python -m pip install --user --upgrade pip")
    print("python -m pip install --user --upgrade setuptools wheel")
    print("python -m pip install --user --upgrade kivy")
    exit(1)

from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.graphics import (Canvas, PushMatrix, PopMatrix, Translate,
                           Scale)
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.event import EventDispatcher
from kivy.uix.widget import WidgetBase
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ColorProperty

def component_to_id(component):
    return str(component).replace(".", "o")


def color_to_id(color):
    return ("color_" + component_to_id(color[0])
            + "_" + component_to_id(color[1])
            + "_" + component_to_id(color[2])
            + "_" + component_to_id(color[3]))


class RectButton(Button):
    plainColor = ColorProperty([1, 1, 1])

    def __init__(self, **kwargs):
        color = kwargs.get('color')
        super(RectButton, self).__init__(**kwargs)
        self.border = [0, 0, 0, 0]
        if color is not None:
            self.plainComponents = [color[0], color[1], color[2],
                                    color[3]]
        else:
            self.plainComponents = [1, 1, 1, 1]
        self.plainColor = tuple(self.plainComponents)
        print("type(plainColor):{}"
              "".format(type(self.plainColor).__name__))
        # assert(type(self.plainColor).__name__ == "Color")
        # ^ Color, but ONLY accepts list since is a ColorProperty
        print("RectButton color:{}".format(self.color))
        print("RectButton plainComponents:{}"
              "".format(self.plainComponents))
        print("RectButton plainColor:{}".format(self.plainColor))
        self.background_color = self.plainColor
        self.background_normal = ''
        with self.canvas:
            pass
            # self.canvas.clear()
            # self.plainColor
            # Rectangle(pos=self.pos, size=self.size)

    def getColor(self):
        if type(self.plainColor).__name__ != "Color":
            print("WARNING: plainColor is not a Color!")
            return Color(self.plainColor)
        return self.plainColor
        # return self.background_color

'''
    def on_press(self):
        pass
        print("CLICKED")

    def register_event_type(self, fn):
        # NOTE: Can't inherit from EventDispatcher since that is
        # incompatible with other bases classes (Kivy refuses)
        print("REGISTER {}".format(fn))
'''

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
    # isStillPushingColorButton = None
    # content = content

    def adjust_rects(self):
        return
        '''
        if self.row_lists is not None:
            # self.free_widget.size = self.mainBoxLayout.size
            # self.free_widget.pos = self.mainBoxLayout.pos
            # cell_w = self.free_widget.size[0] / 16
            # cell_h = self.free_widget.size[1] / 16
            # cell_w = self.colorsHLayouts[0].size[0] / 16
            # cell_h = self.free_widget.size[1] / 16
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
        '''

    def onChoose(self, instance):
        print("Clicked {}".format(instance.plainComponents))
        self.callback(instance.plainComponents)
        self.dismiss()

    def onChangeBrightness(self, instance):
        v = instance.plainColor[0]
        print("clicked v:{}".format(v))
        for y in range(len(self.row_lists)):
            row = self.row_lists[y]
            for x in range(len(row)):
                h = y*16.0/256.0
                s = x*16.0/256.0
                a = 1.0
                button = row[x]
                # print("button.color:{}".format(button.color))
                button.plainComponents = (
                    list(colorsys.hsv_to_rgb(h, s, v)) + [1.0]
                )
                button.plainColor = tuple(button.plainComponents)
                button.background_color = tuple(button.plainComponents)
                # button.plainColor = button.background_color


    def __init__(self, callback, **kwargs):
        # super(ColorPopup, self).__init__(**kwargs)
        Popup.__init__(self, **kwargs)
        self.callback = callback
        if callback is None:
            raise ValueError("You must specify a callback for"
                             " ColorPopup for when a color is chosen to"
                             " receive the color.")
        self.row_lists = list()
        self.mainBoxLayout = BoxLayout(orientation='vertical')
        self.add_widget(self.mainBoxLayout)
        # self.isStillPushingColorButton = True

        # self.mainColorPicker = ColorPicker()
        # self.mainColorPicker.color = self.pickedColor
        # self.mainBoxLayout.add_widget(self.mainColorPicker)

        self.buttonBoxLayout = BoxLayout(orientation='horizontal')
        self.buttonBoxLayout.size_hint=(1.0,.2)
        self.mainBoxLayout.add_widget(self.buttonBoxLayout)

        self.cancelButton = Factory.Button(text="Close")
        # id="cancelButton"
        self.buttonBoxLayout.add_widget(self.cancelButton)
        self.cancelButton.bind(on_press=self.dismiss)

        self.paletteLayout = BoxLayout(orientation='horizontal')
        self.brightnessLayout = BoxLayout(orientation='vertical')
        self.colors_v_layout = BoxLayout(orientation='vertical')
        self.colorsHLayouts = []
        # self.free_widget = FloatLayout(size_hint=(1.0, 1.0),
        # size=self.mainBoxLayout.size)
        self.mainBoxLayout.add_widget(self.paletteLayout)
        self.paletteLayout.add_widget(self.colors_v_layout)
        self.paletteLayout.add_widget(self.brightnessLayout)
        divisor = 16
        for i in reversed(range(divisor + 1)):
            v = i * 16 / 256
            color = [v, v, v, 1.0]
            thisBtn = RectButton(
                    color=color,
                    on_press=self.onChangeBrightness
            )
            thisBtn.plainComponents = color
            thisBtn.plainColor = tuple(thisBtn.plainComponents)
            self.brightnessLayout.add_widget(thisBtn)
        # self.mainBoxLayout.add_widget(self.free_widget)
        # cell_w = self.free_widget.size[0] / divisor
        # cell_h = self.free_widget.size[1] / divisor
        # cell_w = self.colors_v_layout.width / divisor
        # cell_h = cell_w
        left = 0
        yPx = 0
        xPx = 0
        l = 1.0
        v = 1.0
        for y in range(0,16):
            this_h_layout = BoxLayout(orientation='horizontal')
            self.colors_v_layout.add_widget(this_h_layout)
            self.colorsHLayouts.append(this_h_layout)
            this_list = list()
            xPx = left
            for x in range(0,16):
                # hsla = [x*16.0/256.0, y*16.0/256.0, 0, 1.0]
                h = y*16.0/256.0
                s = x*16.0/256.0
                a = 1.0
                # color = [x*16.0/256.0, y*16.0/256.0, 0, 1.0]
                # color = list(colorsys.hls_to_rgb(h, l, s)) + [1.0]
                # ^ always white if l is 1!
                color = list(colorsys.hsv_to_rgb(h, s, v)) + [1.0]
                print("COLOR:{}".format(color))
                # this_rect = Rectangle(pos=(x*cell_w,y*cell_h), \
                # size=(cell_w,cell_h) \
                # )
                # _color_instruction = Color(r=color[0], g=color[1],
                # b=color[2], a=1.0)
                # self.free_widget.canvas.add(_color_instruction)
                # self.free_widget.canvas.add(this_rect)
                idStr = color_to_id(color)
                size16 = 1.0 / divisor
                # thisBtn = Factory.Button(
                thisBtn = RectButton(
                    # background_color=color,
                    color=color,
                    # size_hint=(size16, size16),
                    # pos=(xPx, yPx),
                    # size=(cell_w, cell_h),
                    on_press=self.onChoose,
                    # border=(0, 0, 0, 0),
                )

                btnCanvas = thisBtn.canvas
                print("dir(canvas):{}".format(dir(thisBtn.canvas)))
                print("canvas:{}".format(thisBtn.canvas))
                print("canvas.children:{}"
                      "".format(thisBtn.canvas.children))
                # ^ See widget anatomy in readme.
                print("canvas.length():{}"
                      "".format(thisBtn.canvas.length()))
                good_size = None
                good_pos = None
                '''
                for i in reversed(range(thisBtn.canvas.length())):
                    child = thisBtn.canvas.children[i]
                    typeName = type(child).__name__
                    print("  canvas[{}]:{}".format(i, typeName))
                    if typeName == "BindTexture":
                        thisBtn.canvas.remove(child)
                    elif typeName == "Color":
                        if i > 0:
                            pass
                            # thisBtn.canvas.remove(child)
                            # ^ white
                    elif typeName == "BorderImage":
                        thisBtn.canvas.remove(child)
                        # thisBtn.canvas.add(Rectangle())
                    elif typeName == "Rectangle":
                        print("dir(child):{}".format(dir(child)))
                        print("child.pos:{}".format(child.pos))
                        print("child.size:{}".format(child.size))
                        good_pos = child.pos
                        good_size = child.size
                        # child.source = None
                        # thisBtn.canvas.remove(child)
                        # new = Rectangle(pos=good_pos, size=good_size)
                        # thisBtn.canvas.add(new)
                    else:
                        pass
                        # thisBtn.canvas.remove(child)

                # size is always 0,0
                # pos is always 50, 50
                # children: Color, BindTexture, BorderImage, Color,
                # BindTexture, Rectangle

                # group: None
                # exit(0)

                # btnCanvas.clear()
                # btnCanvas.add(PushMatrix())
                thisBtn.plainComponents = color
                thisBtn.plainColor = tuple(thisBtn.plainComponents)
                btnCanvas.add(thisBtn.getColor())
                # btnCanvas.add(Size(thisBtn.size))
                # ^ expected kivy.graphics.instructions.Instruction, got
                # ObservableReferenceList
                # btnCanvas.add(Scale(thisBtn.size))
                # btnCanvas.add(thisBtn.pos)
                # ^ expected kivy.graphics.instructions.Instruction, got
                # ObservableReferenceList
                # btnCanvas.add(Translate(thisBtn.pos))
                btnCanvas.add(Rectangle(size=good_size,
                                        pos=good_pos))
                # btnCanvas.add(Rectangle())
                # btnCanvas.add(PopMatrix())
                # id=idStr ID is not a string!
                # self.free_widget.add_widget(thisBtn)
                # thisBtn.canvas_before.add(_color_instruction)
                '''
                #this_dict = dict()
                #this_dict["rect"] = this_rect
                #this_dict["ci"] = _color_instruction
                print("C:"+idStr)
                # print(" == Color: "+str( (_color_instruction.r, \
                # # _color_instruction.g, \
                # # _color_instruction.b ) ) )
                # this_list.append(this_dict)
                this_list.append(thisBtn)
                # this_h_layout.add_widget(Rectangle(color=(x,y,128)))
                this_h_layout.add_widget(thisBtn)
                # xPx += cell_w
            # yPx += cell_h
            self.row_lists.append(this_list)

        # self.okButton = Factory.Button(text="OK")
        # self.okButton.bind(on_press=self.onOKButtonClick)
        # self.buttonBoxLayout.add_widget(self.okButton)

        # self.cancelButton = Factory.Button(text="Cancel")
        # self.cancelButton.bind(on_press=self.onCancelButtonClick)
        # self.buttonBoxLayout.add_widget(self.cancelButton)

        # self.bind(on_touch_up=self.onAnyClick)
        # self.bind(on_dismiss=self.onDismiss)

'''
    def onOKButtonClick(self, instance):
        #root.dismiss()
        self.pickedColor = self.mainColorPicker.color
        #self.isStillPushingColorButton = True
        self.dismiss()

    def onCancelButtonClick(self, instance):
        #root.dismiss()
        #self.isStillPushingColorButton = True
        self.dismiss()

    def onAnyClick(self, touch, *largs):
        if not self.isStillPushingColorButton:
            self.pickedColor = self.mainColorPicker.color
            self.isStillPushingColorButton = True
            self.dismiss()
        self.isStillPushingColorButton = False

    def onDismiss(self, instance):
        self.isStillPushingColorButton = True
'''

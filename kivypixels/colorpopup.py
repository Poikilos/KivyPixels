#!/usr/bin/env python

try:
    import kivy
except ImportError as ex:
    print("This program requires kivy. Try:")
    print("python -m pip install --user --upgrade pip")
    print("python -m pip install --user --upgrade setuptools wheel")
    print("python -m pip install --user --upgrade kivy")
    exit(1)

from kivy.uix.popup import Popup
from kivy.graphics import Color  # , Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory

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
        print("Clicked {}".format(instance.background_color))
        self.callback(instance.background_color)
        self.dismiss()

    def __init__(self, callback, **kwargs):
        # super(ColorPopup, self).__init__(**kwargs)
        Popup.__init__(self, **kwargs)
        self.callback = callback
        if callback is None:
            raise ValueError("You must specify a callback for"
                             " ColorPopup for when a color is chosen to"
                             " recieve the color.")
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

        self.cancelButton = Factory.Button(text="Close")
        # id="cancelButton"
        self.buttonBoxLayout.add_widget(self.cancelButton)
        self.cancelButton.bind(on_press=self.dismiss)


        self.colors_v_layout = BoxLayout(orientation='vertical')
        self.colorsHLayouts = []
        # self.free_widget = FloatLayout(size_hint=(1.0, 1.0), size=self.mainBoxLayout.size)
        self.mainBoxLayout.add_widget(self.colors_v_layout)
        # self.mainBoxLayout.add_widget(self.free_widget)
        divisor = 16
        # cell_w = self.free_widget.size[0] / divisor
        # cell_h = self.free_widget.size[1] / divisor
        # cell_w = self.colors_v_layout.width / divisor
        # cell_h = cell_w
        left = 0
        yPx = 0
        xPx = 0
        for y in range(0,16):
            this_h_layout = BoxLayout(orientation='horizontal')
            self.colors_v_layout.add_widget(this_h_layout)
            self.colorsHLayouts.append(this_h_layout)
            this_list = list()
            xPx = left
            for x in range(0,16):
                color = [x*16.0/256.0,y*16.0/256.0,0, 1.0]
                #this_rect = Rectangle(pos=(x*cell_w,y*cell_h), \
                #                      size=(cell_w,cell_h) \
                #                      )
                #_color_instruction = Color(r=color[0], g=color[1], b=color[2], a=1.0)
                #self.free_widget.canvas.add(_color_instruction)
                #self.free_widget.canvas.add(this_rect)
                idStr = color_to_id(color)
                size16 = 1.0 / divisor
                this_button = Factory.Button(
                    background_color=color,
                    #size_hint=(size16, size16),
                    # pos=(xPx, yPx),
                    #size=(cell_w, cell_h),
                    on_press=self.onChoose,
                    border=(0, 0, 0, 0)
                )
                # id=idStr ID is not a string!
                # self.free_widget.add_widget(this_button)
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
                this_h_layout.add_widget(this_button)
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

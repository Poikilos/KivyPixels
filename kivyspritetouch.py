'''
KivySpriteTouch
==========
based on http://kivy.org/docs/examples/gen__canvas__fbo_canvas__py.html

"This demonstrates a layout using an FBO (Frame Buffer Off-screen)
instead of a plain canvas. You should see a black canvas with a
button labelled 'FBO' in the bottom left corner. Clicking it
animates the button moving right to left."

This fork of FBO Canvas is renamed KivySpriteTouch.
Known Issues (with priority) (x or date=done):
-(high) Make objects (drawings) that can be saved as sprites
-(high) detect byte order of surface, to avoid green-red reversal issue in kivy 1.8.0 pygame.image.fromstring with parameter self.fbo.pixelsd
-(high) Make all objects except menu pixel-based (so use widget instead of FloatLayout)
-(feature request) Make animated sprites
-(feature request) Save sprite animations as gif or zipped png sequence so as to be played back by built-in kivy animation player (just use gif or zip as source for Image)
'''
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.button import Button
from kivy.uix.popup import Popup

'''
#TODO: Animated Sprites
#see http://kivy.org/docs/api-kivy.uix.image.html
animatedImage = Image(source='animated.gif')
#animatedImage = AsyncImage(source='animated.gif')
#options:
#allow_stretch=True #default is False
#keep_ratio=False #default is True
#color = Color(rMultiplier,gMultiplier,bMultiplier,aMultiplier) #ListProperty; default is [1,1,1,1]
#keep_data = True #keeps the raw pixels such as for pixel-based collision detection; default is False
#anim_delay=-1 #-1 is stop; default is .25 (4fps)
#animatedImage.reload() #if file was loaded, you can reload it
#anim_loop=1 #0 is infinite


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

class PixelWidget(Widget):
    IsDebugMode = False
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
    
    paletteColors = None
    redColor = None
    greenColor = None
    blueColor = None
    brushPaletteIndex = None
    #brushFileName = "brushTrianglePointingDown-25percent.png"
    _brush_color = None
    brushOriginalImage = None
    brushImage = None
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

        # wait that all the instructions are in the canvas to set texture
        self.texture = self.fbo.texture
        
        self.viewImage = KPImage(self.fbo.size[0],self.fbo.size[1],KPImage.defaultByteDepth)
        #self.viewImage.FillAllDestructivelyUsingColorBytes(0, 0, 0, 255)
        print("width:"+str(self.viewImage.width))
        print("height:"+str(self.viewImage.height))
        #print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
        #print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))
        self.brushOriginalImage = KPImage.static_createFromImageFile(self, "brush2.png")
        self.brushImage = KPImage(self.brushOriginalImage.width, self.brushOriginalImage.height, self.brushOriginalImage.byteDepth)
        self.set_brush_color(Color(1,1,1,1))
        #self.brushImage = Image(source=self.brushFileName, keep_data=True)
        #self.brushImage = CoreImage(self.brushFileName)
        
        #self.brushTexture = self.brushImage.texture
        
        self.redColor = Color(1,0,0,1)
        self.greenColor = Color(0,1,0,1)
        self.blueColor = Color(0,0,1,1)
        self.paletteColors = list()
        self.paletteColors.append(self.redColor)
        self.paletteColors.append(self.greenColor)
        self.paletteColors.append(self.blueColor)
        
        
        
        #self.brushFboWidgetSimple = FboWidgetSimple()
        #self.add_widget(self.brushFboWidgetSimple)
        #self.brushFboWidgetSimple.width = self.brushImage.width
        #self.brushFboWidgetSimple.height = self.brushImage.height
        #TODO: see if Kivy app can use pygame.sprite.Sprite
        #self.brushPixels = self.brushSurface.tostring()
        
        #brushFboRectangle = Rectangle(texture=self.brushTexture, pos=(0,0), size=(self.brushImage.width,self.brushImage.height))
        #self.brushFboWidgetSimple.fbo.add(brushFboRectangle)
        


        #self.texture = Texture.create(size=(512, 512), colorfmt='RGBA', bufferfmt='ubyte')
        #self.texture.add_reload_observer(self.populate_texture)
        #self.fbo.texture.add_reload_observer(self.fbo_populate_texture)
        #self.populate_texture(self.texture)
        #self.populate_texture(self.fbo.texture)


    #def populate_texture(self, texture):
    #    texture.blit_buffer(bytes(self.viewImage.buffer))
        

    #def fbo_populate_texture(self, texture):
    #    texture.blit_buffer(bytes(self.viewImage.buffer))
        
#     def add_widget(self, *largs):
#         # trick to attach graphics instruction to fbo instead of canvas
#         canvas = self.canvas
#         self.canvas = self.fbo
#         ret = super(PixelWidget, self).add_widget(*largs)
#         self.canvas = canvas
#         return ret
# 
#     def remove_widget(self, *largs):
#         canvas = self.canvas
#         self.canvas = self.fbo
#         super(PixelWidget, self).remove_widget(*largs)
#         self.canvas = canvas

    def updatePixelViewSize(self):
        if (self.fbo.size[0]!=self.viewImage.width) or (self.fbo.size[1]!=self.viewImage.height):
            newKPImage = KPImage(self.fbo.size[0],self.fbo.size[1],KPImage.defaultByteDepth)
            newKPImage.drawToSelfTopLeft_LineCopy_FillRestWithTransparent(self.viewImage)
            self.viewImage = newKPImage
            
            print("width:"+str(self.viewImage.width))
            print("height:"+str(self.viewImage.height))
            #print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
            #print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))
            
        
        
    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value
        
        if (self.saveButton is not None):
            self.saveButton.width=self.fbo_rect.size[0]/5
            self.saveButton.height=self.fbo_rect.size[1]/10
        #if (self.brushImage is not None):
        #    pass
            #self.brushImage.width=self.fbo_rect.size[0]/10
            #self.brushImage.height=self.brushImage.width
        self.updatePixelViewSize()
        self.uploadBufferToTexture()
        

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_alpha(self, instance, value):
        self.fbo_color.rgba = (1, 1, 1, value)

    def set_brush_color(self, color):
        self._brush_color = color
        self.brushImage.drawToSelfTopLeft_LineCopy_FillRestWithTransparent(self.brushOriginalImage)
        self.brushImage.tintByColor(self._brush_color)
        
    def set_brush_color_to_next_in_palette(self):
        if (self.brushPaletteIndex is None):
            self.brushPaletteIndex = 0
        else:
            self.brushPaletteIndex += 1
        if (self.brushPaletteIndex>=len(self.paletteColors)):
            self.brushPaletteIndex=0
        self.set_brush_color(self.paletteColors[self.brushPaletteIndex])

    def on_touch_down(self, touch):
        super(PixelWidget, self).on_touch_down(touch)
        #self.set_brush_color_to_next_in_palette()
        self.set_brush_color(self.paletteWidget.pickedColor)
        self.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])

    def on_touch_move(self, touch):
        super(PixelWidget, self).on_touch_move(touch)
        self.brushAt(touch.x-self.pos[0], touch.y-self.pos[1])
    
    def uploadBufferToTexture(self):
        #formerly used ImageData (decided to not use core.ImageData -- didn't seem to work in Kivy 1.8.0):https://groups.google.com/forum/#!topic/kivy-users/3jYJtVk5vPQ
        self.texture.blit_buffer(bytes(self.viewImage.buffer), colorfmt='rgba', bufferfmt='ubyte')
        #NOTE: blit_buffer has no return
        #self.ask_update() #does nothing
        self.canvas.ask_update()
        
    def brushAt(self, centerX, centerY):
        
        #normalSize = self.brushImage.get_norm_image_size()
        self.brushImage.width = self.brushImage.width  # int(normalSize[0])
        self.brushImage.height = self.brushImage.height # int(normalSize[1])
        
        #self.viewImage.set_at(touch.x, touch.y, self._brush_color) #dont' uncomment, since size of this is only set at Save now (not on_size)
        
        #self.assumed_fbo_stride = int(self.fbo.size[0]) * self.assumed_fbo_byteDepth
        #self.viewImage.array_set_at_GRBA(self.fbo.pixels, assumed_fbo_stride, assumed_fbo_byteDepth, touch.x, touch.y, _brush_color)
        #self.fbo.add(self._brush_color)
        #brushPoint = Point(points=(atX, atY))
        #self.fbo.add(brushPoint)
        #brushLine = Line(points=[centerX, centerY, centerX+1, centerY], width=1)
        #self.fbo.add(brushLine)
        
        #destX = centerX - self.brushImage.center_x
        #destY = centerY - self.brushImage.center_y

        destX = int(centerX) - int(self.brushImage.width/2)
        destY = int(centerY) - int(self.brushImage.height/2)
        #destLineStartX = destX
        
        #Since in kivy's pygame.image.fromstring(data, (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True)
        # saves with odd (errant??) byte order,
        # channel offsets are:
        bOffset = 2 #bOffset = 0 #blue comes from green channel
        gOffset = 0 #gOffset = 1 #green comes from blue channel
        rOffset = 1 #rOffset = 2 
        aOffset = 3 #aOffset = 3
        
        #brushBuffer_byteDepth = 4
        #brushBuffer_stride = int(self.brushImage.width) * brushBuffer_byteDepth
        thisBrushBuffer = self.brushImage.buffer  # self.brushPixels
        destByteIndex = destY*self.viewImage.stride + destX*self.viewImage.byteDepth
        destLineStartIndex = destByteIndex
        if self.IsDebugMode:
            print()
            print("self.brushImage.width:"+str(self.brushImage.width))
            print("self.brushImage.height:"+str(self.brushImage.height))
            print("brushImage.byteDepth:"+str(self.brushImage.byteDepth))
            print("brushImage.stride:"+str(self.brushImage.stride))
            print("self.viewImage.stride:"+str(self.viewImage.stride))
            print("self.viewImage.byteDepth:"+str(self.viewImage.byteDepth))
            print("destByteIndex:"+str(destByteIndex))
            
        sourceLineStartIndex = 0
        debugPixelWriteCount = 0
        try:
            for sourceY in range(0,int(self.brushImage.height)):
                #destX = destLineStartX
                destByteIndex = destLineStartIndex
                sourceByteIndex = sourceLineStartIndex
                for sourceX in range(0,int(self.brushImage.width)):
                    brushThisPixelAlphaByte = thisBrushBuffer[sourceByteIndex + aOffset]
                    brushThisPixelAlphaMultiplier = brushThisPixelAlphaByte/255.0
                    brushThisPixelInverseAlphaMultiplier = 1.0 - brushThisPixelAlphaMultiplier
                    #sourceByteIndex = sourceY*brushBuffer_stride + sourceX*brushBuffer_byteDepth
                    if (brushThisPixelAlphaByte != 0):
                        #do alpha formula on each channel (+.5 for rounding)
                        
                        aTotalInt = int(self.viewImage.buffer[destByteIndex+aOffset]) + brushThisPixelAlphaByte
                        if aTotalInt>255:
                            aTotalInt = 255
                        #self.viewImage.buffer[destByteIndex+bOffset] = int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+bOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+bOffset]) + .5 )
                        #self.viewImage.buffer[destByteIndex+gOffset] = int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+gOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+gOffset]) + .5 )
                        #self.viewImage.buffer[destByteIndex+rOffset] = int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+rOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+rOffset]) + .5 )
                        #self.viewImage.buffer[destByteIndex+aOffset] = aTotalInt
                        brushBGRAByteArray=[int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+bOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+bOffset]) + .5 ), int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+gOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+gOffset]) + .5 ), int(  brushThisPixelInverseAlphaMultiplier*float(self.viewImage.buffer[destByteIndex+rOffset]) + brushThisPixelAlphaMultiplier*float(thisBrushBuffer[sourceByteIndex+rOffset]) + .5 ), aTotalInt]
                        #brushBGRABytes = bytes(brushBGRAByteArray)
                        self.viewImage.buffer[destByteIndex+bOffset] = brushBGRAByteArray[0]
                        self.viewImage.buffer[destByteIndex+gOffset] = brushBGRAByteArray[1]
                        self.viewImage.buffer[destByteIndex+rOffset] = brushBGRAByteArray[2]
                        self.viewImage.buffer[destByteIndex+aOffset] = brushBGRAByteArray[3]
                        
                        debugPixelWriteCount += 1
                    #destX += 1
                    destByteIndex += self.viewImage.byteDepth
                    sourceByteIndex += self.brushImage.byteDepth
                #destY += 1
                destLineStartIndex += self.viewImage.stride
                sourceLineStartIndex += self.brushImage.stride
            self.uploadBufferToTexture()
        #except:
        except Exception as e:
            print("Could not finish brushAt: "+str(e))
            print("    destByteIndex:"+str(destByteIndex)+"; sourceByteIndex:"+str(sourceByteIndex)+"; len(self.viewImage.buffer):"+str(len(self.viewImage.buffer))+"; len(brushPixels):"+str(len(thisBrushBuffer)))
#         if (debugColor is not None):
#             print("debugColor:"+str(debugColor.b)+","+str(debugColor.g)+","+str(debugColor.r)+","+str(debugColor.a))
#         else:
#             print("debugColor:None")
        #self.fbo.add(self._brush_color)
        ##brushRect = Rectangle(texture=self.brushTexture, pos=(atX-self.brushImage.center_x,atY-self.brushImage.center_y), size=(self.brushImage.size[0],self.brushImage.size[1]))
        #brushRect = Rectangle(texture=self.brushTexture, pos=(destX,destY), size=(self.brushImage.size[0],self.brushImage.size[1]))
        ##brushRect = Rectangle(source=self.brushFileName, pos=(touch.x,touch.y), size=(16,16))
        #self.fbo.add(brushRect)
        if self.IsDebugMode:
            print("debugPixelWriteCount:"+str(debugPixelWriteCount))
        
        
    def onSaveButtonClick(self,instance):
        #see C:\Kivy-1.8.0-py3.3-win32\kivy\kivy\tests\test_graphics.py
        #data = self.fbo.pixels
        #saveFileName = "Untitled1.png"
        self.viewImage.saveAs("Untitled1.png")
        if self.IsDebugMode:
            self.brushImage.saveAs("debug-save-brush.png")

    def onColorButtonClick(self,instance):
        self.paletteWidget.open()
    
#     def onEraserButtonClick(self, instance):
#         #TODO: finish this
#         print("eraser")

class ColorPopup(Popup):
    pickedColor = Color(1,1,1,1)
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
        
        self.buttonsLayout = BoxLayout(orientation='vertical', size_hint=(.1,1.0))
        self.mainWidget.add_widget(self.buttonsLayout)
        
        pixelWidget.paletteWidget = ColorPopup(size_hint=(.9,.5))
        
        self.saveButton = Factory.Button(text="Save", id="saveButton")
        self.buttonsLayout.add_widget(self.saveButton)
        self.saveButton.bind(on_press=pixelWidget.onSaveButtonClick)

        self.colorButton = Factory.Button(text="Color", id="colorButton")
        self.buttonsLayout.add_widget(self.colorButton)
        self.colorButton.bind(on_press=pixelWidget.onColorButtonClick)

#         self.eraserButton = Factory.Button(text="Eraser", id="eraserButton")
#         self.buttonsLayout.add_widget(self.eraserButton)
#         self.eraserButton.bind(on_press=pixelWidget.onEraserButtonClick)
        
        return self.mainWidget

    def saveBrush(self):
        self.brushImage.saveAs("debug save (brush).png")
#         normalSize = self.brushImage.get_norm_image_size()
#         self.brushImage.width = int(normalSize[0])
#         self.brushImage.height = int(normalSize[1])
#         data = bytes(self.brushImage.buffer) #convert from bytearray to bytes
#         surface = pygame.image.fromstring(data, (self.brushImage.width, self.brushImage.height), 'RGBA', True)
#         pygame.image.save(surface, "debug save (brush).png")


if __name__ == "__main__":
    KivySpriteTouchApp().run()
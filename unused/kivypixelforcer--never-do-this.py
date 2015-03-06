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
__all__ = ('PixelWidget', )

from kivy.graphics import Color, Rectangle, Canvas, ClearBuffers, ClearColor
from kivy.graphics import Line
#from kivy.graphics.fbo import Fbo
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty
from kivy.app import App
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.factory import Factory

from kivy.uix.widget import Widget
from kivy.graphics import Fbo, ClearColor, ClearBuffers, Ellipse
from kivy.uix.image import Image
import pygame
#from kivy.core.image import Image as CoreImage

import os
from pixelbuffer import PixelBuffer
from kivy.graphics import Point
import random
#TODO: implement resize

class FboWidgetSimple(Widget):
    texture = ObjectProperty(None, allownone=True)
    alpha = NumericProperty(1)
    def __init__(self, **kwargs):
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
        super(FboWidgetSimple, self).__init__(**kwargs)
        
    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value
        
    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_alpha(self, instance, value):
        self.fbo_color.rgba = (1, 1, 1, value)

class PixelWidget(Widget):

    texture = ObjectProperty(None, allownone=True)
    alpha = NumericProperty(1)
    pixelBuffer = None
    PIXELBUFFER_DEFAULT_BYTEDEPTH = 4
    #TOTALBYTECOUNT = None
    #TOTALPIXELCOUNT = None
    #STRIDE = None
    #pixelBuffer = None
    brushImage = None
    brushTexture = None
    assumed_fbo_byteDepth = 4
    assumed_fbo_stride = None
    
    brushFboWidgetSimple = None
    
    saveButton = None
    
    randColors = None
    redColor = None
    greenColor = None
    blueColor = None
    brushRandomIndex = None
    brushFileName = "brushTrianglePointingDown-25percent.png"
    brushColor = None
    brushSurface = None
    brushPixels = None
    
    def __init__(self, **kwargs):
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
        
        self.pixelBuffer = PixelBuffer(self.fbo.size[0],self.fbo.size[1],self.PIXELBUFFER_DEFAULT_BYTEDEPTH)
        print("width:"+str(self.pixelBuffer.width))
        print("height:"+str(self.pixelBuffer.height))
        #print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
        #print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))
        self.brushImage = Image(source=self.brushFileName, keep_data=True)
        #self.brushImage = CoreImage(self.brushFileName)
        
        self.brushTexture = self.brushImage.texture
        
        self.redColor = Color(1,0,0,1)
        self.greenColor = Color(0,1,0,1)
        self.blueColor = Color(0,0,1,1)
        self.randColors = list()
        self.randColors.append(self.redColor)
        self.randColors.append(self.greenColor)
        self.randColors.append(self.blueColor)
        
        #self.brushFboWidgetSimple = FboWidgetSimple()
        #self.add_widget(self.brushFboWidgetSimple)
        #self.brushFboWidgetSimple.width = self.brushImage.width
        #self.brushFboWidgetSimple.height = self.brushImage.height
        self.brushSurface = pygame.image.load(self.brushFileName)
        self.brushPixels = pygame.image.tostring(self.brushSurface, 'RGBA', False)
        #TODO: see if Kivy app can use pygame.sprite.Sprite
        #self.brushPixels = self.brushSurface.tostring()
        
        #brushFboRectangle = Rectangle(texture=self.brushTexture, pos=(0,0), size=(self.brushImage.width,self.brushImage.height))
        #self.brushFboWidgetSimple.fbo.add(brushFboRectangle)
        

        super(PixelWidget, self).__init__(**kwargs)


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

    def UpdatePixelBufferSize(self):
        newPixelBuffer = PixelBuffer(self.fbo.size[0],self.fbo.size[1],self.PIXELBUFFER_DEFAULT_BYTEDEPTH)
        newPixelBuffer.DrawToSelf_AtTopLeft_FillRestWithTransparent_1operationPerLine(self.pixelBuffer)
        self.pixelBuffer = newPixelBuffer
        
        print("width:"+str(self.pixelBuffer.width))
        print("height:"+str(self.pixelBuffer.height))
        #print("TOTALBYTECOUNT:"+str(self.TOTALBYTECOUNT))
        #print("TOTALPIXELCOUNT:"+str(self.TOTALPIXELCOUNT))
        
        
    def on_size(self, instance, value):
        self.fbo.size = value
        self.texture = self.fbo.texture
        self.fbo_rect.size = value
        
        if (self.saveButton is not None):
            self.saveButton.width=self.fbo_rect.size[0]/5
            self.saveButton.height=self.fbo_rect.size[1]/10
        if (self.brushImage is not None):
            pass
            #self.brushImage.width=self.fbo_rect.size[0]/10
            #self.brushImage.height=self.brushImage.width

    def on_pos(self, instance, value):
        self.fbo_rect.pos = value

    def on_texture(self, instance, value):
        self.fbo_rect.texture = value

    def on_alpha(self, instance, value):
        self.fbo_color.rgba = (1, 1, 1, value)

    def on_touch_down(self, touch):
        #self.brushRandomIndex = random.randrange(0,len(self.randColors))
        if (self.brushRandomIndex is None):
            self.brushRandomIndex = 0
        else:
            self.brushRandomIndex += 1
        if (self.brushRandomIndex>=len(self.randColors)):
            self.brushRandomIndex=0
        self.brushColor = self.randColors[self.brushRandomIndex]
        self.brushAt(touch.x, touch.y, self.brushColor)
        super(PixelWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if (self.brushColor is not None):
            self.brushAt(touch.x, touch.y, self.brushColor)
        super(PixelWidget, self).on_touch_move(touch)
        
    def brushAt(self, centerX, centerY, brushColor):
        
        normalSize = self.brushImage.get_norm_image_size()
        brushNormalW = normalSize[0]
        brushNormalH = normalSize[1]
        
        #self.pixelBuffer.set_at(touch.x, touch.y, self.brushColor) #dont' uncomment, since size of this is only set at Save now (not on_size)
        
        self.assumed_fbo_stride = int(self.fbo.size[0]) * self.assumed_fbo_byteDepth
        #self.pixelBuffer.array_set_at_GRBA(self.fbo.pixels, assumed_fbo_stride, assumed_fbo_byteDepth, touch.x, touch.y, brushColor)
        #self.fbo.add(self.brushColor)
        #brushPoint = Point(points=(atX, atY))
        #self.fbo.add(brushPoint)
        #brushLine = Line(points=[centerX, centerY, centerX+1, centerY], width=1)
        #self.fbo.add(brushLine)
        
        #destX = centerX - self.brushImage.center_x
        #destY = centerY - self.brushImage.center_y

        destX = centerX - self.brushImage.width/2
        destY = centerY - self.brushImage.height/2
        destLineStartX = destX
        
        bOffset=0
        gOffset=1
        rOffset=2
        aOffset=3
        
        assumed_texture_bytedepth = 4
        #assumed_texture_stride = int(self.brushImage.texture_size[0]) * assumed_texture_bytedepth
        assumed_texture_stride = int(brushNormalW) * assumed_texture_bytedepth
        thisColorChannelList = None
        thisColor = None
        debugColor = None
        #set one pixel at a time: 
        for sourceY in range(0,int(brushNormalH)):
            destX = destLineStartX
            for sourceX in range(0,int(brushNormalW)):
                sourceByteIndex = sourceY*assumed_texture_stride + sourceX*assumed_texture_bytedepth
                #thisColor = self.brushImage.read_pixel(sourceX, sourceY)
                #thisColor = self.brushImage.pixels[sourceByteIndex]
                #thisColorChannelList = self.brushFboWidgetSimple.fbo.get_pixel_color(sourceX, sourceY)
                #thisBuffer = self.brushFboWidgetSimple.fbo.pixels
                thisBuffer = self.brushPixels
                #thisColor = Color(thisColorChannelList[0]/255,thisColorChannelList[1]/255,thisColorChannelList[2]/255,thisColorChannelList[3]/255)
                #thisColor = Color(self.brushImage.data[sourceByteIndex+rOffset], self.brushImage.data[sourceByteIndex+gOffset], self.brushImage.data[sourceByteIndex+bOffset], self.brushImage.data[sourceByteIndex+aOffset])
                thisColor = Color(thisBuffer[sourceByteIndex+rOffset]/255.0, thisBuffer[sourceByteIndex+gOffset]/255.0, thisBuffer[sourceByteIndex+bOffset]/255.0, thisBuffer[sourceByteIndex+aOffset]/255.0)
                #thisColor = Color(self.brushImage.image[sourceByteIndex+rOffset], self.brushImage.image[sourceByteIndex+gOffset], self.brushImage.image[sourceByteIndex+bOffset], self.brushImage.image[sourceByteIndex+aOffset])
                if (thisColor.a != 0.0):
                    #debugColor = thisColor
                    self.fbo.add(thisColor)
                    brushLine = Line(points=[destX, destY, destX+1, destY], width=1)
                    self.fbo.add(brushLine)
                destX += 1
            destY += 1
#         if (debugColor is not None):
#             print("debugColor:"+str(debugColor.b)+","+str(debugColor.g)+","+str(debugColor.r)+","+str(debugColor.a))
#         else:
#             print("debugColor:None")
        #self.fbo.add(self.brushColor)
        ##brushRect = Rectangle(texture=self.brushTexture, pos=(atX-self.brushImage.center_x,atY-self.brushImage.center_y), size=(self.brushImage.size[0],self.brushImage.size[1]))
        #brushRect = Rectangle(texture=self.brushTexture, pos=(destX,destY), size=(self.brushImage.size[0],self.brushImage.size[1]))
        ##brushRect = Rectangle(source=self.brushFileName, pos=(touch.x,touch.y), size=(16,16))
        #self.fbo.add(brushRect)
        
        
    def SaveButtonClick(self,instance):
        #see C:\Kivy-1.8.0-py3.3-win32\kivy\kivy\tests\test_graphics.py
        import pygame
        #data = self.fbo.pixels
        saveFileName = "Untitled1.png"
        print("Saving \"" + os.path.join(os.getcwd(), saveFileName) + "\"")
        
        #Since in kivy's pygame.image.fromstring(data, (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True)
        # saves with odd (errant??) byte order,
        # channel offsets are:
        bOffset = 1 #bOffset = 0 #blue comes from green channel
        gOffset = 0 #gOffset = 1 #green comes from blue channel
        rOffset = 2 #rOffset = 2 
        aOffset = 3 #aOffset = 3
        self.UpdatePixelBufferSize()
        self.assumed_fbo_stride = int(self.fbo.size[0]) * self.assumed_fbo_byteDepth
        #self.pixelBuffer.array_DrawToSelf_AtTopLeft_FillRestWithTransparent_1operationPerLine(self.fbo.pixels, self.assumed_fbo_stride, self.assumed_fbo_byteDepth, self.fbo.size[0], self.fbo.size[1])
        #self.pixelBuffer.array_DrawToSelf_AtTopLeft_FillRestWithTransparent_ToGRBA(self.fbo.pixels, self.assumed_fbo_stride, self.assumed_fbo_byteDepth, self.fbo.size[0], self.fbo.size[1])
        self.pixelBuffer.array_DrawToSelf_AtTopLeft_FillRestWithTransparent_ToCustomByteOrder(self.fbo.pixels, self.assumed_fbo_stride, self.assumed_fbo_byteDepth, self.fbo.size[0], self.fbo.size[1], bOffset, gOffset, rOffset, aOffset)
        data = bytes(self.pixelBuffer.buffer) #convert from bytearray to bytes
        surface = pygame.image.fromstring(data, (self.fbo.size[0], self.fbo.size[1]), 'RGBA', True)
        pygame.image.save(surface, saveFileName)


class KivyPixelForcerApp(App):
    def build(self):

        thisFboWidget = PixelWidget()
        thisFboWidget.saveButton = Factory.Button(text="Save", size_hint=(None, None), id="saveButton")
        thisFboWidget.add_widget(thisFboWidget.saveButton)

        #def anim_btn(*args):
        #    if saveButton.pos[0] == 0:
        #        Animation(x=thisFboWidget.width - saveButton.width).start(saveButton)
        #    else:
        #        Animation(x=0).start(saveButton)
        #saveButton.bind(on_press=anim_btn)
        thisFboWidget.saveButton.bind(on_press=thisFboWidget.SaveButtonClick)

        return thisFboWidget


if __name__ == "__main__":
    KivyPixelForcerApp().run()
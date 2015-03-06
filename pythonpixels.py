import math
from _winapi import NULL

class PPAnimationMetaFrame:
    travel = None
    seconds = None
    passedSeconds = None
    index = None
    
    def __init__(self):
        self.travel = (0.0,0.0)
        #seconds = .0166 #60fps
        self.seconds = .0333 #30fps default
        self.index = 0 #index in a frame array
        self.passedSeconds = 0.0
        
    def advanceByTime(self, relative_seconds):
        self.passedSeconds += relative_seconds
        
    def getRemainingSeconds(self):
        return self.seconds - self.passedSeconds

    def getOvertime(self):
        return self.passedSeconds - self.seconds

    def getOvertimeAndReset(self):
        overtime = self.passedSeconds - self.seconds
        self.resetTime()
        return overtime
    
    def resetTime(self):
        self.passedSeconds = 0.0
        
    def getIsFinished(self):
        returnFinished = None
        if (self.seconds is not None) and (self.seconds > 0.0):
            returnFinished = self.passedSeconds > self.seconds
        else:
            returnFinished = False
        return returnFinished

#PPAnimation is ONLY a list of indeces (metaframe objects)--Sprite stores actual images
class PPAnimation:
    #list of PPAnimationMetaFrame objects
    frames = None
    metaframeIndex = None
    
    def __init__(self):
        self.frames = list()
        self.frames.append(PPAnimationMetaFrame())
        self.metaframeIndex = 0
        
    def getFrameIndex(self):
        return self.frames[self.metaframeIndex].index
        
    def advanceByFrames(self, frameCount):
        self.metaframeIndex += frameCount
        while (self.metaframeIndex < 0):
            self.metaframeIndex += len(self.frames)
        while (self.metaframeIndex >= len(self.frames)):
            self.metaframeIndex -= len(self.frames)
    
    def getCurrentFrameObject(self):
        return self.frames[self.metaframeIndex]
    
    def advanceByTime(self, seconds):
        while (seconds>0):
            currentFrame = self.getCurrentFrameObject()
            currentFrame.advanceByTime(seconds)
            previousSeconds = seconds
            seconds = currentFrame.getOvertime()
            if (currentFrame.getIsFinished()):
                currentFrame.resetTime()
                self.advanceByFrames(1)
                currentFrame = self.getCurrentFrameObject()
            elif (seconds-previousSeconds < .0001):
                #prevent infinite loop (and stay on current frame if currentFrame.seconds==0.0 (nonmoving frame)
                break

class PPSpriteAbstract:
    tau = math.pi * 2.0
    eighthOfTau = math.pi / 4.0
    
    ANIM_Angle0 = 0
    ANIM_Angle45 = 10
    ANIM_Angle90 = 20
    ANIM_Angle135 = 30
    ANIM_Angle180 = 40
    ANIM_Angle225 = 50
    ANIM_Angle270 = 60
    ANIM_Angle315 = 70

    ANIM_StyleArmed = 0
    ANIM_StyleUnarmed = 100
    
    ANIM_ActionStand = 0
    ANIM_ActionWalk = 1
    ANIM_ActionRun = 2
    ANIM_ActionStrike = 3
    ANIM_ActionDeath = 4
    
    def getAnimIndex_Deg(self, angleDegrees, actionConstant, styleConstant):
        angleIndex = self.getAngleIndex(angleDegrees)
        return styleConstant + angleIndex + actionConstant

    def getAnimIndex_Rad(self, angleRadians, actionConstant, styleConstant):
        angleIndex = self.getAngleIndex(angleRadians)
        return styleConstant + angleIndex + actionConstant
    
    def getAngleIndex_Deg(self, angleDegrees):
        while angleDegrees < 0:
            angleDegrees += 360
        #while angleDegrees >= 360:
        #    angleDegrees -= 360
        angleIndex = int((angleDegrees / 45.0) + .5) #+.5 for rounding
        while angleIndex > 7:
            angleIndex -= 8

    def getAngleIndex_Rad(self, angleRadians):
        while angleRadians < 0:
            angleRadians += PPSpriteAbstract.tau
        #while angleRadians >= PPSprite.tau:
        #    angleRadians -= PPSprite.tau
        angleIndex = int((angleRadians / PPSpriteAbstract.eighthOfTau) + .5) #+.5 for rounding
        while angleIndex > 7:
            angleIndex -= 8
    
class PPUnscaledSprite:
    worldPos = None
    screenPos = None
    sourceOriginalRect = None
    sourceCroppedRect = None
    destRenderRect = None
    #list of PPAnimations:
    animations = None
    ANIM = None
    images = None
    #offset within current animation:
    frameOffset = None
    
    def __init__(self):
        self.animations = list()
        self.animations.append(PPAnimation())
        self.ANIM = 0 #PPSpriteAbstract.ANIM_Default
        self.images = list()
        self.worldPos = (0.0,0.0)
        self.screenPos = (0.0,0.0)
        
    def getImageIndex(self):
        return self.animations(self.ANIM).getFrameIndex()
    
    def addFrame(self, newPPImage):
        self.images.append(newPPImage)
    
    #uses screenPos to calculate destRenderRect (cropped) and sourceCroppedRect
    def crop(self, screenRect):
        selfX = int(self.screenPos[0])
        selfY = int(self.screenPos[1])
        self.sourceCroppedRect.left = 0
        self.sourceCroppedRect.top = 0
        self.sourceCroppedRect.width = self.sourceOriginalRect.width
        self.sourceCroppedRect.height = self.sourceOriginalRect.height
        self.destRenderRect.left = selfX
        self.destRenderRect.top = selfY
        self.destRenderRect.width = self.sourceOriginalRect.width
        self.destRenderRect.height = self.sourceOriginalRect.height
        pastLeftCount = screenRect.left - selfX #itemRect.left
        if pastLeftCount > 0:
            self.sourceCroppedRect.left += pastLeftCount
            self.sourceCroppedRect.width -= pastLeftCount
            self.destRenderRect.left += pastLeftCount
            self.destRenderRect.height -= pastLeftCount
        pastRightCount = (self.destRenderRect.left+self.sourceOriginalRect.width) - (screenRect.left+screenRect.width)
        if (pastRightCount>0):
            self.sourceCroppedRect.width -= pastRightCount
        #if (self.sourceCroppedRect.width<0):
        #    self.sourceCroppedRect.width = 0
        #if (self.destRenderRect.width<0):
        #    self.destRenderRect.width = 0
        #NOTE: for speed, let renderer deal with skipping negative-sized sprites
            
        pastTopCount = screenRect.top - selfY
        if pastTopCount > 0:
            self.sourceCroppedRect.top += pastTopCount
            self.sourceCroppedRect.height -= pastTopCount
            self.destRenderRect.top += pastTopCount
            self.destRenderRect.height -= pastTopCount
        pastBottomCount = (self.sourceOriginalRect.top+self.sourceOriginalRect.height) - (screenRect.top+screenRect.height)
        if (pastBottomCount>0):
            self.sourceCroppedRect.height -= pastBottomCount
            self.destRenderRect.height -= pastBottomCount
        #if (self.sourceCroppedRect.width<0):
        #    self.sourceCroppedRect.width = 0
        #if (self.destRenderRect.width<0):
        #    self.destRenderRect.width = 0
        #NOTE: for speed, let renderer deal with skipping negative-sized sprites


class PPRect:
    top = None
    left = None
    width = None
    height = None
    
    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
    
        
        
    def clamp(self, screenRect):
        #clamp self TO the given screenRect and return that copy of self (like pygame.screenRect clamp)
        itemRect = PPRect(self.top, self.left, self.width. self.height)

        pastLeftCount = screenRect.left - itemRect.left
        if pastLeftCount > 0:
            itemRect.left += pastLeftCount
            itemRect.width -= pastLeftCount
        pastRightCount = (itemRect.left+itemRect.width) - (screenRect.left+screenRect.width)
        if (pastRightCount>0):
            itemRect.width -= pastRightCount
        if (itemRect.width<0):
            itemRect.width = 0
            
        pastTopCount = screenRect.top - itemRect.top
        if pastTopCount > 0:
            itemRect.top += pastTopCount
            itemRect.height -= pastTopCount
        pastBottomCount = (itemRect.top+itemRect.height) - (screenRect.top+screenRect.height)
        if (pastBottomCount>0):
            itemRect.height -= pastBottomCount        
        if (itemRect.width<0):
            itemRect.width = 0
            
        return itemRect

class PPColor:
    byteDepth = None
    channels = None
    bOffset = None
    gOffset = None
    rOffset = None
    aOffset = None
    
    def __init__(self):
        self.bOffset = 0
        self.gOffset = 1
        self.rOffset = 2
        self.aOffset = 3
        self.byteDepth = 4
        self.channels = bytearray([0,0,0,255])
    
    def getA(self):
        returnByte = None
        if (self.aOffset is not None):
            returnByte = self.channels[self.aOffset]
        return returnByte

    def getR(self):
        returnByte = None
        if (self.rOffset is not None):
            returnByte = self.channels[self.rOffset]
        return returnByte

    def getG(self):
        returnByte = None
        if (self.gOffset is not None):
            returnByte = self.channels[self.gOffset]
        return returnByte
    
    def getB(self):
        returnByte = None
        if (self.bOffset is not None):
            returnByte = self.channels[self.bOffset]
        return returnByte
    
    def setBytesFromRGBA(self, r, g, b, a):
        if self.rOffset is not None:
            self.channels[self.rOffset] = b''+r
        if self.gOffset is not None:
            self.channels[self.gOffset] = b''+g
        if self.bOffset is not None:
            self.channels[self.bOffset] = b''+b
        if self.aOffset is not None:
            self.channels[self.aOffset] = b''+a

def bufferToTupleStyleString(buffer, start, count):
    openerString = "("
    returnString = openerString
    for index in range(start,start+count):
        if returnString==openerString:
            returnString += str(buffer[index])
        else:
            returnString += "," + str(buffer[index])
        #returnString+="@"+str(index)
    returnString += ")"
    return returnString

class PPImage:
    #static variables
    defaultByteDepth = 4
    
    #member variables
    stride = None
    width = None
    height = None
    byteDepth = None
    buffer = None
    byteCount = None
    bOffset = None
    gOffset = None
    rOffset = None
    aOffset = None
    lastUsedFileName = None
    IsDebugMode = False
    
    def __init__(self, set_width, set_height, set_byteDepth):
            self.init(set_width, set_height, set_byteDepth, None)
                        
    def init(self, set_width, set_height, set_byteDepth, setBufferReferenceElseNone):
        previousByteCount = None
        if (self.buffer is not None):
            previousByteCount = len(self.buffer)
        
        self.width = int(set_width)
        self.height = int(set_height)
        self.byteDepth = int(set_byteDepth)
        self.stride = self.width * self.byteDepth
        self.byteCount = self.stride * self.height
        if (setBufferReferenceElseNone is None):
            if (previousByteCount is None) or (self.byteCount != previousByteCount):
                self.buffer = bytearray(self.byteCount) #debug leaves dirty data on purpose for speed
        else:
            self.buffer = setBufferReferenceElseNone
        
        if (set_byteDepth>3):
            self.bOffset = 0
            self.gOffset = 1
            self.rOffset = 2
            self.aOffset = 3
        elif (set_byteDepth==1):
            self.bOffset = None
            self.gOffset = None
            self.rOffset = None
            self.aOffset = 0
        elif (set_byteDepth==3):
            self.bOffset = 0
            self.gOffset = 1
            self.rOffset = 2
            self.aOffset = None
        else:
            print("ERROR: unknown byteDepth "+str(set_byteDepth)+" in PPImage init")
        
    
    def set_at_from_float_color(self, atX, atY, brushColor):
        self.static_set_at_from_float_color_ToCustomByteOrder(self.buffer, self.stride, self.byteDepth, atX, atY, brushColor, self.bOffset, self.gOffset, self.rOffset, self.aOffset)

    def static_set_at_from_float_color_ToCustomByteOrder(self, destArray, destStride, destByteDepth, atX, atY, brushColor, bOffset, gOffset, rOffset, aOffset):
        xCenter = int(atX)
        yCenter = int(atY)
        pixelByteIndex = destStride*yCenter + xCenter*destByteDepth
        #print ("pixelByteIndex:"+str(pixelByteIndex))
        #print ("len(pixelBuffer):"+str(len(destArray)))
        #print("writing bytes...")
        destArray[pixelByteIndex + bOffset] = int(brushColor.b*255.0+.5)
        destArray[pixelByteIndex + gOffset] = int(brushColor.g*255.0+.5)
        destArray[pixelByteIndex + rOffset] = int(brushColor.r*255.0+.5)
        if (aOffset is not None) and (aOffset<self.byteDepth):
            destArray[pixelByteIndex + aOffset] = int(brushColor.a*255.0+.5)

        
    #def DrawFromWithAlpha(self, sourceVariableImage, atX, atY):
        
    def getMaxChannelValueNotIncludingAlpha(self):
        destByteIndex = 0
        destLineByteIndex = destByteIndex
        returnMax = 0
        for thisY in range(0,self.height):
            destByteIndex = destLineByteIndex
            for thisX in range(0,self.width):
                #if self.buffer[destByteIndex+self.bOffset]>returnMax:
                #    returnMax = self.buffer[destByteIndex+self.bOffset]
                #if self.buffer[destByteIndex+self.gOffset]>returnMax:
                #    returnMax = self.buffer[destByteIndex+self.gOffset]
                #if self.buffer[destByteIndex+self.rOffset]>returnMax:
                #    returnMax = self.buffer[destByteIndex+self.rOffset]
                #destByteIndex += self.byteDepth
                for channelIndex in range(0,self.byteDepth):
                    if self.buffer[destByteIndex]>returnMax:
                        returnMax = self.buffer[destByteIndex]
                    destByteIndex += 1
            destLineByteIndex += self.stride
        return returnMax

    def getMaxAlphaValue(self):
        destByteIndex = 0
        destLineByteIndex = destByteIndex
        returnMax = None
        if (self.aOffset is not None):
            returnMax = 0
            for thisY in range(0,self.height):
                destByteIndex = destLineByteIndex
                for thisX in range(0,self.width):
                    if self.buffer[destByteIndex+self.aOffset]>returnMax:
                        returnMax = self.buffer[destByteIndex+self.aOffset]
                    destByteIndex += self.byteDepth
                destLineByteIndex += self.stride
        return returnMax
    
    def FillAllDestructivelyUsingByteColor(self, brushByteColor):
        self.FillAllDestructivelyUsingColorBytes(brushByteColor.getR(),brushByteColor.getG(),brushByteColor.getB(),brushByteColor.getA())
        
    def FillAllDestructivelyUsingColorBytes(self, setRByte, setGByte, setBByte, setAByte):
        destByteIndex = 0
        destLineByteIndex = destByteIndex
        setBytes = bytes([setBByte, setGByte, setRByte, setAByte])
        for thisY in range(0,self.height):
            destByteIndex = destLineByteIndex
            for thisX in range(0,self.width):
                self.buffer[destByteIndex+self.bOffset] = setBytes[0]
                self.buffer[destByteIndex+self.gOffset] = setBytes[1]
                self.buffer[destByteIndex+self.rOffset] = setBytes[2]
                self.buffer[destByteIndex+self.aOffset] = setBytes[3]
                destByteIndex += self.byteDepth
            destLineByteIndex += self.stride


    def static_PixelFill_CustomByteOrders(self, destImage, arrayDestStartByteIndex, arrayDestEndExByteIndex, sourceImage, arraySourceStartByteIndex, arraySourceEndExByteIndex):
        sourceByteDepth = sourceImage.byteDepth
        destByteDepth = destImage.byteDepth
        destArray = destImage.buffer
        sourceArray = sourceImage.buffer
        bOffset = sourceImage.bOffset
        gOffset = sourceImage.gOffset
        rOffset = sourceImage.rOffset
        aOffset = sourceImage.aOffset
        maxByteDepth = destImage.byteDepth
        if (sourceImage.byteDepth < maxByteDepth):
            maxByteDepth = sourceImage.byteDepth
        #if (sourceByteDepth == destByteDepth):
            #if (sourceByteDepth == 4):
        sourceIndex = arraySourceStartByteIndex
        destIndex = arrayDestStartByteIndex
        destRegionByteCount = arrayDestEndExByteIndex - arrayDestStartByteIndex
        sourceRegionByteCount = arraySourceEndExByteIndex - arraySourceStartByteIndex
        destRegionPixelCount = int(destRegionByteCount/destByteDepth)
        sourceRegionPixelCount = int(sourceRegionByteCount/sourceByteDepth)
        minPixelCount = destRegionPixelCount
        if (sourceRegionPixelCount<minPixelCount):
            minPixelCount = sourceRegionPixelCount
        #if (destRegionPixelCount<=sourceRegionPixelCount):
        if (maxByteDepth>=4):
            for relativeIndex in range(0,minPixelCount):
                destArray[destIndex + destImage.bOffset] = sourceArray[sourceIndex + bOffset]
                destArray[destIndex + destImage.gOffset] = sourceArray[sourceIndex + gOffset]
                destArray[destIndex + destImage.rOffset] = sourceArray[sourceIndex + rOffset]
                destArray[destIndex + destImage.aOffset] = sourceArray[sourceIndex + aOffset]
                destIndex += destByteDepth
                sourceIndex += sourceByteDepth
        elif (maxByteDepth==3):
            for relativeIndex in range(0,minPixelCount):
                destArray[destIndex + destImage.bOffset] = sourceArray[sourceIndex + bOffset]
                destArray[destIndex + destImage.gOffset] = sourceArray[sourceIndex + gOffset]
                destArray[destIndex + destImage.rOffset] = sourceArray[sourceIndex + rOffset]
                destIndex += destByteDepth
                sourceIndex += sourceByteDepth
        elif (maxByteDepth==1):
            destLastByte = destByteDepth - 1
            sourceLastByte = sourceByteDepth - 1
            destIndex += destLastByte
            sourceIndex += sourceLastByte
            #offset by byteDepth-1 so that gray will be written to RGBA image's alpha or vice versa
            for relativeIndex in range(0,minPixelCount):
                #destArray[destIndex + destImage.bOffset] = sourceArray[sourceIndex + bOffset]
                destArray[destIndex] = sourceArray[sourceIndex]
                destIndex += destByteDepth
                sourceIndex += sourceByteDepth
        else:
            print("Not Yet Implemented in ")    
    
    
    def drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder(self, input_buffer, input_stride, input_byteDepth, input_width, input_height, input_bOffset, input_gOffset, input_rOffset, input_aOffset):
        #this is much like LineCopy version, except instead of using python array slicing it uses static_PixelFill_CustomByteOrders
        input_stride = int(input_stride)
        input_width = int(input_width)
        input_height = int(input_height)
        input_byteDepth = int(input_byteDepth)
        IsToFillRestWithZeroes = True
        destByteIndex = 0
        sourceByteIndex = 0
        
        #force colorspace conversion:
        if (self.byteDepth>=3):
            if ((input_aOffset is not None) and (input_bOffset is None) and (input_gOffset is None) and (input_rOffset is None)):
                input_bOffset = input_aOffset
                input_gOffset = input_aOffset
                input_rOffset = input_aOffset
        
        
        if self.byteDepth>=3 and (input_byteDepth>=3 or input_byteDepth==1):
            destLineOfZeroes = None
            if (input_height<self.height):
                destLineOfZeroes = bytearray(self.stride)
            if (input_width==self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                for destY in range(0,self.height):
                    destByteIndex = destLinePixelIndex
                    sourceByteIndex = sourceLinePixelIndex
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    #NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        #self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndex]
                        #self.static_PixelFill_CustomByteOrders(self.buffer, destLinePixelIndex, NextDestLinePixelIndex, input_buffer, sourceLinePixelIndex, NextSourceLinePixelIndex, input_bOffset, input_gOffset, input_rOffset, input_aOffset)
                        if (self.byteDepth==3):
                            for destX in range(0,self.width):
                                self.buffer[destByteIndex + self.bOffset] = input_buffer[sourceByteIndex + input_bOffset]
                                self.buffer[destByteIndex + self.gOffset] = input_buffer[sourceByteIndex + input_gOffset]
                                self.buffer[destByteIndex + self.rOffset] = input_buffer[sourceByteIndex + input_rOffset]
                                destByteIndex += self.byteDepth
                                sourceByteIndex += input_byteDepth
                        elif (self.byteDepth>=4):
                            for destX in range(0,self.width):
                                self.buffer[destByteIndex + self.bOffset] = input_buffer[sourceByteIndex + input_bOffset]
                                self.buffer[destByteIndex + self.gOffset] = input_buffer[sourceByteIndex + input_gOffset]
                                self.buffer[destByteIndex + self.rOffset] = input_buffer[sourceByteIndex + input_rOffset]
                                self.buffer[destByteIndex + self.aOffset] = input_buffer[sourceByteIndex + input_aOffset]
                                destByteIndex += self.byteDepth
                                sourceByteIndex += input_byteDepth
                        elif (self.byteDepth==1):
                            for destX in range(0,self.width):
                                self.buffer[destByteIndex + self.aOffset] = input_buffer[sourceByteIndex + input_aOffset]
                                destByteIndex += self.byteDepth
                                sourceByteIndex += input_byteDepth
                            #if (destX<input_width):
                            #for destChannel in range(0,self.byteDepth):
                            #else:
                            #    break
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                        #static_PixelFill_CustomByteOrders(self.buffer, destLinePixelIndex, NextDestLinePixelIndex, destLineOfZeroes, 0, self.stride, input_bOffset, input_gOffset, input_rOffset, input_aOffset)
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
            elif (input_width>self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                for destY in range(0,self.height):
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    #NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    NextSourceLinePixelIndexLIMITED = sourceLinePixelIndex + self.stride #intentionally self.stride, to limit how much to get
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        #self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndexLIMITED]
                        self.static_PixelFill_CustomByteOrders(self.buffer, destLinePixelIndex, NextDestLinePixelIndex, input_buffer, sourceLinePixelIndex, NextSourceLinePixelIndexLIMITED, input_bOffset, input_gOffset, input_rOffset, input_aOffset)
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
            else: #elif (input_width<self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                PartialDestLineOfZeroes = bytearray(self.stride-input_stride)
                for destY in range(0,self.height):
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    NextDestLinePixelIndexLIMITED = destLinePixelIndex + input_stride #intentially input stride to limit self stride since source is smaller
                    NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    #NextSourceLinePixelIndexLIMITED = sourceLinePixelIndex + self.stride #intentionally self.stride, to limit how much to get
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        #self.buffer[destLinePixelIndex:NextDestLinePixelIndexLIMITED] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndex]
                        self.static_PixelFill_CustomByteOrders(self.buffer, destLinePixelIndex, NextDestLinePixelIndexLIMITED, input_buffer, sourceLinePixelIndex, NextSourceLinePixelIndex, input_bOffset, input_gOffset, input_rOffset, input_aOffset)
                        if IsToFillRestWithZeroes:
                            self.buffer[NextDestLinePixelIndexLIMITED:NextDestLinePixelIndex] = PartialDestLineOfZeroes[:]
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
        else:
            print("Byte depth combination not implemented in drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder: input_byteDepth="+str(input_byteDepth)+" to self.byteDepth"+str(self.byteDepth))
    
    def drawToSelfTopLeft_LineCopy_FillRestWithTransparent(self, input_PPImage):
        self.static_DrawToArray_ToTopLeft_LineCopy_FillRestWithTransparent(input_PPImage.buffer, input_PPImage.stride, input_PPImage.byteDepth, input_PPImage.width, input_PPImage.height)
        
    def static_DrawToArray_ToTopLeft_LineCopy_FillRestWithTransparent(self, input_buffer, input_stride, input_byteDepth, input_width, input_height):
        IsToFillRestWithZeroes = True
        if self.byteDepth == input_byteDepth:
            destLineOfZeroes = None
            if (input_height<self.height):
                destLineOfZeroes = bytearray(self.stride)
            if (input_width==self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                for destY in range(0,self.height):
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndex]
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
            elif (input_width>self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                for destY in range(0,self.height):
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    #NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    NextSourceLinePixelIndexLIMITED = sourceLinePixelIndex + self.stride #intentionally self.stride, to limit how much to get
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndexLIMITED]
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
            else: #elif (input_width<self.width):
                destLinePixelIndex = 0
                sourceLinePixelIndex = 0
                PartialDestLineOfZeroes = bytearray(self.stride-input_stride)
                for destY in range(0,self.height):
                    NextDestLinePixelIndex = destLinePixelIndex + self.stride
                    NextDestLinePixelIndexLIMITED = destLinePixelIndex + input_stride #intentially input stride to limit self stride since source is smaller
                    NextSourceLinePixelIndex = sourceLinePixelIndex + input_stride
                    #NextSourceLinePixelIndexLIMITED = sourceLinePixelIndex + self.stride #intentionally self.stride, to limit how much to get
                    if (destY<input_height):
                        #NOTE: width difference is already handled in outer "if" statement, for speed.
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndexLIMITED] = input_buffer[sourceLinePixelIndex:NextSourceLinePixelIndex]
                        if IsToFillRestWithZeroes:
                            self.buffer[NextDestLinePixelIndexLIMITED:NextDestLinePixelIndex] = PartialDestLineOfZeroes[:]
                    elif IsToFillRestWithZeroes:
                        self.buffer[destLinePixelIndex:NextDestLinePixelIndex] = destLineOfZeroes[:]
                    else:
                        break
                    destLinePixelIndex += self.stride
                    sourceLinePixelIndex += input_stride
        else:
            print("Not Yet Implemented: different byte depth in DrawToSelfAtTopLeft")
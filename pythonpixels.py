import math

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

# PPAnimation is ONLY a list of indeces (metaframe objects)--
# Sprite stores actual images
class PPAnimation:
    # list of PPAnimationMetaFrame objects
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
                # prevent infinite loop (and stay on current frame if
                # currentFrame.seconds==0.0 (nonmoving frame)
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

    def getAnimIndex_Deg(self, angleDegrees, actionConstant,
            styleConstant):
        angleIndex = self.getAngleIndex(angleDegrees)
        return styleConstant + angleIndex + actionConstant

    def getAnimIndex_Rad(self, angleRadians, actionConstant,
            styleConstant):
        angleIndex = self.getAngleIndex(angleRadians)
        return styleConstant + angleIndex + actionConstant

    def getAngleIndex_Deg(self, angleDegrees):
        while angleDegrees < 0:
            angleDegrees += 360
        #while angleDegrees >= 360:
        #    angleDegrees -= 360
        angleIndex = int((angleDegrees / 45.0) + .5)  # +.5 for rounding
        while angleIndex > 7:
            angleIndex -= 8

    def getAngleIndex_Rad(self, angleRadians):
        while angleRadians < 0:
            angleRadians += PPSpriteAbstract.tau
        # while angleRadians >= PPSprite.tau:
            # angleRadians -= PPSprite.tau
        angleIndex = int((angleRadians / PPSpriteAbstract.eighthOfTau) +
                         .5) #+.5 for rounding
        while angleIndex > 7:
            angleIndex -= 8

class PPUnscaledSprite:
    sourceOriginalRect = None
    sourceCroppedRect = None
    destRenderRect = None
    #offset within current animation:
    frameOffset = None

    def __init__(self):
        # list of PPAnimations:
        self.animations = []
        self.animations.append(PPAnimation())
        self.ANIM = 0 #PPSpriteAbstract.ANIM_Default
        self.images = []
        self.worldPos = (0.0,0.0)
        self.screenPos = (0.0,0.0)

    def getImageIndex(self):
        return self.animations(self.ANIM).getFrameIndex()

    def addFrame(self, newPPImage):
        self.images.append(newPPImage)

    # uses screenPos to calculate destRenderRect (cropped) and
    # sourceCroppedRect
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
        pastLeftCount = screenRect.left - selfX  # itemRect.left
        if pastLeftCount > 0:
            self.sourceCroppedRect.left += pastLeftCount
            self.sourceCroppedRect.width -= pastLeftCount
            self.destRenderRect.left += pastLeftCount
            self.destRenderRect.height -= pastLeftCount
        pastRightCount = ((self.destRenderRect.left +
                           self.sourceOriginalRect.width) -
                          (screenRect.left + screenRect.width))
        if (pastRightCount>0):
            self.sourceCroppedRect.width -= pastRightCount
        #if (self.sourceCroppedRect.width<0):
        #    self.sourceCroppedRect.width = 0
        #if (self.destRenderRect.width<0):
        #    self.destRenderRect.width = 0
        # NOTE: for speed, let renderer deal with skipping
        # negative-sized sprites

        pastTopCount = screenRect.top - selfY
        if pastTopCount > 0:
            self.sourceCroppedRect.top += pastTopCount
            self.sourceCroppedRect.height -= pastTopCount
            self.destRenderRect.top += pastTopCount
            self.destRenderRect.height -= pastTopCount
        pastBottomCount = ((self.sourceOriginalRect.top +
                            self.sourceOriginalRect.height) -
                           (screenRect.top+screenRect.height))
        if (pastBottomCount>0):
            self.sourceCroppedRect.height -= pastBottomCount
            self.destRenderRect.height -= pastBottomCount
        # if (self.sourceCroppedRect.width<0):
            # self.sourceCroppedRect.width = 0
        # if (self.destRenderRect.width<0):
            # self.destRenderRect.width = 0
        # NOTE: for speed, let renderer deal with skipping
        # negative-sized sprites


class PPRect:

    def __init__(self, top, left, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def clamp(self, screenRect):
        # clamp self TO the given screenRect and return that copy of
        # self (like pygame.screenRect clamp)
        itemRect = PPRect(self.top, self.left, self.width. self.height)

        pastLeftCount = screenRect.left - itemRect.left
        if pastLeftCount > 0:
            itemRect.left += pastLeftCount
            itemRect.width -= pastLeftCount
        pastRightCount = ((itemRect.left+itemRect.width) -
                          (screenRect.left+screenRect.width))
        if (pastRightCount>0):
            itemRect.width -= pastRightCount
        if (itemRect.width<0):
            itemRect.width = 0

        pastTopCount = screenRect.top - itemRect.top
        if pastTopCount > 0:
            itemRect.top += pastTopCount
            itemRect.height -= pastTopCount
        pastBottomCount = ((itemRect.top+itemRect.height) -
                           (screenRect.top+screenRect.height))
        if (pastBottomCount>0):
            itemRect.height -= pastBottomCount
        if (itemRect.width<0):
            itemRect.width = 0

        return itemRect

hex_ints = {'0':0,   '1':1, '2':2,  '3':3,
            '4':4,   '5':5, '6':6,  '7':7,
            '8':8,   '9':9, 'A':10, 'B':11,
            'C':12, 'D':13, 'E':14, 'F':15}

def hex2_int(svec2):
    ret = None
    if len(svec2)==2:
        ret = hex_ints[svec2[0]] * 256 + hex_ints[svec2[1]]
    else:
        print("ERROR In hex2_int: length of s is " + str(len(svec2)) +
              " (should be 2)")
    return ret

def vec4_from_vec3(vec3, fourth):
    return vec3[0], vec3[1], vec3[2], fourth

def vec3_from_hex(hexString):
    if hexString[0] == "#":
        hexString = hexString[1:]
    elif hexString[:2] == "0x":
        hexString = hexString[2:]
    hexes = None
    ret = None
    if len(hexString) == 3:
        hexes = [hexString[0], hexString[1], hexString[2]]
        ret = (float(hex_ints(hexes[0]))/15.0,
               float(hex_ints(hexes[1]))/15.0,
               float(hex_ints(hexes[2]))/15.0)
    elif len(hexString) >= 6:
        hexes = [hexString[:2], hexString[2:4], hexString[4:6]]
        ret = (float(hex2_int(hexes[0]))/255.0,
               float(hex2_int(hexes[1]))/255.0,
               float(hex2_int(hexes[2]))/255.0)
    else:
        print("hexString has bad format: " + str(hexString))
    return ret

def vec3_div(vec, divisor):
    return vec[0]/divisor, vec[1]/divisor, vec[2]/divisor

def bgr_from_hex(hexString):
    rgb = vec3_from_hex(hexString)
    # divide all 3 by 255:
    return vec3_div((rgb[2], rgb[1], rgb[0]), 255.0)

def rgb_from_hex(hexString):
    # divide all 3 by 255:
    return vec3_div(vec3_from_hex(hexString), 255.0)

class PPColor:

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

def bufferToTupleStyleString(data, start, count):
    openerString = "("
    returnString = openerString
    for index in range(start,start+count):
        if returnString==openerString:
            returnString += str(data[index])
        else:
            returnString += "," + str(data[index])
        #returnString+="@"+str(index)
    returnString += ")"
    return returnString

# formerly static_PixelFill_CustomByteOrders
def range_copy_with_bo(self, destImage,
        arrayDestStartByteIndex, arrayDestEndExByteIndex,
        sourceImage, arraySourceStartByteIndex,
        arraySourceEndExByteIndex):
    sourceByteDepth = sourceImage.byteDepth
    destByteDepth = destImage.byteDepth
    destArray = destImage.data
    sourceArray = sourceImage.data
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
    destRegionByteCount = (arrayDestEndExByteIndex -
                           arrayDestStartByteIndex)
    sourceRegionByteCount = (arraySourceEndExByteIndex -
                             arraySourceStartByteIndex)
    destRegionPixelCount = int(destRegionByteCount /
                               destByteDepth)
    sourceRegionPixelCount = int(sourceRegionByteCount /
                                 sourceByteDepth)
    minPixelCount = destRegionPixelCount
    if (sourceRegionPixelCount<minPixelCount):
        minPixelCount = sourceRegionPixelCount
    #if (destRegionPixelCount<=sourceRegionPixelCount):
    if (maxByteDepth>=4):
        for relativeIndex in range(0,minPixelCount):
            destArray[destIndex + destImage.bOffset] = \
                sourceArray[sourceIndex + bOffset]
            destArray[destIndex + destImage.gOffset] = \
                sourceArray[sourceIndex + gOffset]
            destArray[destIndex + destImage.rOffset] = \
                sourceArray[sourceIndex + rOffset]
            destArray[destIndex + destImage.aOffset] = \
                sourceArray[sourceIndex + aOffset]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    elif (maxByteDepth==3):
        for relativeIndex in range(0,minPixelCount):
            destArray[destIndex + destImage.bOffset] = \
                sourceArray[sourceIndex + bOffset]
            destArray[destIndex + destImage.gOffset] = \
                sourceArray[sourceIndex + gOffset]
            destArray[destIndex + destImage.rOffset] = \
                sourceArray[sourceIndex + rOffset]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    elif (maxByteDepth==1):
        destLastByte = destByteDepth - 1
        sourceLastByte = sourceByteDepth - 1
        destIndex += destLastByte
        sourceIndex += sourceLastByte
        # offset by byteDepth-1 so that gray will be written to RGBA
        # image's alpha or vice versa
        for relativeIndex in range(0,minPixelCount):
            # destArray[destIndex + destImage.bOffset] = \
                # sourceArray[sourceIndex + bOffset]
            destArray[destIndex] = sourceArray[sourceIndex]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    else:
        print("Not Yet Implemented in ")

def set_at_from_fvec_with_bo(self,
        destArray, destStride, destByteDepth, atX, atY, brushColor,
        bOffset, gOffset, rOffset, aOffset):
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
        destArray[pixelByteIndex + aOffset] = int(brushColor.a *
                                                  255.0 + .5)

# static_DrawToArray_ToTopLeft_LineCopy_FillRestWithTransparent
def blit_copy(self, input_buffer, input_stride,
        input_byteDepth, input_width, input_height):
    IsToFillRestWithZeroes = True
    if self.byteDepth == input_byteDepth:
        dl_zeroes = None  # destLineOfZeroes
        if (input_height<self.height):
            dl_zeroes = bytearray(self.stride)
        if (input_width==self.width):
            d_lpi = 0
            s_lpi = 0
            for destY in range(0,self.height):
                d_nlpi = d_lpi + self.stride
                NextSourceLinePixelIndex = s_lpi + input_stride
                if (destY<input_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    self.data[d_lpi:d_nlpi] = input_buffer[
                        s_lpi:NextSourceLinePixelIndex]
                elif IsToFillRestWithZeroes:
                    self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += self.stride
                s_lpi += input_stride
        elif (input_width>self.width):
            d_lpi = 0
            s_lpi = 0
            for destY in range(0,self.height):
                d_nlpi = d_lpi + self.stride
                # NextSourceLinePixelIndex = s_lpi + input_stride
                s_nlpi_ltd = s_lpi + self.stride
                # intentionally self.stride, to limit how much to get
                if (destY<input_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    self.data[d_lpi:d_nlpi] = input_buffer[
                        s_lpi:s_nlpi_ltd]
                elif IsToFillRestWithZeroes:
                    self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += self.stride
                s_lpi += input_stride
        else:  # elif (input_width<self.width):
            d_lpi = 0
            s_lpi = 0
            # PartialDestLineOfZeroes:
            pdl_zeroes = bytearray(self.stride-input_stride)
            for destY in range(0,self.height):
                d_nlpi = d_lpi + self.stride
                d_nlpi_ltd = d_lpi + input_stride
                # intentially input stride to limit self stride since
                #     # source is smaller
                NextSourceLinePixelIndex = s_lpi + input_stride
                # s_nlpi_ltd = s_lpi + self.stride
                #     # intentionally self.stride, to limit what to get
                if (destY<input_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    self.data[d_lpi:d_nlpi_ltd] = input_buffer[
                        s_lpi:NextSourceLinePixelIndex]
                    if IsToFillRestWithZeroes:
                        self.data[d_nlpi_ltd:d_nlpi] = pdl_zeroes[:]
                elif IsToFillRestWithZeroes:
                    self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += self.stride
                s_lpi += input_stride
    else:
        print("Not Yet Implemented: different byte depth in blit_copy")


# blit_copy_with_bo
# (NOT static_set_at_from_fvec_with_bo)
# was formerly:
# drawFromArray_ToTopLeft_FillRestWithTransparent_CustomByteOrder
# drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder

# static_set_at_from_fvec_with_bo
# was formerly:
# static_set_at_from_float_color_ToCustomByteOrder

class PPImage:

    def __init__(self, size, byte_depth=4):
            self.init(size, byte_depth, bufferAsRef=None)

    def init(self, size, byte_depth=4, bufferAsRef=None):
        self.name = None
        self.data = None
        self.bOffset = None
        self.gOffset = None
        self.rOffset = None
        self.aOffset = None
        self.lastUsedFileName = None
        self.debugEnabled = False

        previousByteCount = None
        if (self.data is not None):
            previousByteCount = len(self.data)
        self.size = (int(size[0]), int(size[1]))
        # self.width = int(size[0])
        # self.height = int(size[1])
        self.byteDepth = int(byte_depth)
        self.stride = self.size[0] * self.byteDepth
        self.byteCount = self.stride * self.size[1]
        if (bufferAsRef is None):
            if ((previousByteCount is None) or
                    (self.byteCount != previousByteCount)):
                self.data = bytearray(self.byteCount)
                    # debug leaves dirty data on purpose for speed
        else:
            self.data = bufferAsRef

        if (byte_depth>3):
            self.bOffset = 0
            self.gOffset = 1
            self.rOffset = 2
            self.aOffset = 3
        elif (byte_depth==1):
            self.bOffset = None
            self.gOffset = None
            self.rOffset = None
            self.aOffset = 0
        elif (byte_depth==3):
            self.bOffset = 0
            self.gOffset = 1
            self.rOffset = 2
            self.aOffset = None
        else:
            print("ERROR: unknown byte_depth " + str(byte_depth) +
                  " in PPImage init")

    def get_size(self):
        return (self.size[0], self.size[1])

    def print_dump(self):
        print(str(self.get_dict()), data_enable=False)

    def get_dict(self, data_enable=True):
        ret = {}
        ret['size'] = self.size
        ret['rOffset'] = self.rOffset
        ret['gOffset'] = self.gOffset
        ret['bOffset'] = self.bOffset
        ret['aOffset'] = self.aOffset
        if data_enable:
            ret['data'] = self.data
        ret['tmp'] = {}
        try:
            ret['tmp']['width'] = self.width
            print("WARNING: unknown property width was set.")
            ret['tmp']['height'] = self.height
            print("WARNING: unknown property height was set.")
        except:
            pass
        ret['tmp']['byteDepth'] = self.byteDepth
        ret['tmp']['stride'] = self.stride
        ret['tmp']['byteCount'] = self.byteCount
        ret['tmp']['debugEnabled'] = self.debugEnabled
        return ret

    # aka draw_line_horizontal
    def draw_line_ivec3_h(self, vec2, rgb_bytes, count):
        #self.set_ivec3_at(vec2, color)
        x, y = vec2
        b_i = self.stride*y + x*self.byteDepth + self.bOffset
        g_i = self.stride*y + x*self.byteDepth + self.gOffset
        r_i = self.stride*y + x*self.byteDepth + self.rOffset
        b = rgb_bytes[2]  # int(color.b*255.0+.5)
        g = rgb_bytes[1]  # int(color.g*255.0+.5)
        r = rgb_bytes[0]  # int(color.r*255.0+.5)
        if b_i > len(self.data):
            self.print_dump()
            raise IndexError("Could not finish in draw_line_ivec3_h--" +
                             " Tried to write at " + str(b_i))
        for i in range(count):
            self.data[b_i] = b
            self.data[g_i] = g
            self.data[r_i] = r
            b_i += self.byteDepth
            g_i += self.byteDepth
            r_i += self.byteDepth

    # aka draw_line_vertical
    def draw_line_ivec3_v(self, vec2, rgb_bytes, count):
        #self.set_ivec3_at(vec2, color)
        x, y = vec2
        b_i = self.stride*y + x*self.byteDepth + self.bOffset
        g_i = self.stride*y + x*self.byteDepth + self.gOffset
        r_i = self.stride*y + x*self.byteDepth + self.rOffset
        b = rgb_bytes[2]  # int(color.b*255.0+.5)
        g = rgb_bytes[1]  # int(color.g*255.0+.5)
        r = rgb_bytes[0]  # int(color.r*255.0+.5)
        for i in range(count):
            self.data[b_i] = b
            self.data[g_i] = g
            self.data[r_i] = r
            b_i += self.stride
            g_i += self.stride
            r_i += self.stride

    def set_ivec3_at(self, vec2, rgb_bytes):
        # destPixelByteIndex:
        d_p_bi = self.stride*vec2[1] + vec2[0]*self.byteDepth
        # destArray[d_p_bi + self.bOffset] = int(color.b*255.0+.5)
        # destArray[d_p_bi + self.gOffset] = int(color.g*255.0+.5)
        # destArray[d_p_bi + self.rOffset] = int(color.r*255.0+.5)
        self.data[d_p_bi + self.bOffset] = int(rgb_bytes[2]*255.0+.5)
        self.data[d_p_bi + self.gOffset] = int(rgb_bytes[1]*255.0+.5)
        self.data[d_p_bi + self.rOffset] = int(rgb_bytes[0]*255.0+.5)


    def set_at_from_fvec(self, atX, atY, brushColor):
        set_at_from_fvec_with_bo(self.data,
            self.stride, self.byteDepth, atX, atY, brushColor,
            self.bOffset, self.gOffset, self.rOffset, self.aOffset)

    # def DrawFromWithAlpha(self, sourceVariableImage, atX, atY):

    def getMaxChannelValueNotIncludingAlpha(self):
        d_bi = 0  # destByteIndex
        d_lbi = d_bi  # destLineByteIndex
        returnMax = 0
        for thisY in range(0, self.size[1]):
            d_bi = d_lbi
            for thisX in range(0, self.size[0]):
                #if self.data[d_bi+self.bOffset]>returnMax:
                #    returnMax = self.data[d_bi+self.bOffset]
                #if self.data[d_bi+self.gOffset]>returnMax:
                #    returnMax = self.data[d_bi+self.gOffset]
                #if self.data[d_bi+self.rOffset]>returnMax:
                #    returnMax = self.data[d_bi+self.rOffset]
                #d_bi += self.byteDepth
                for channelIndex in range(0,self.byteDepth):
                    if self.data[d_bi]>returnMax:
                        returnMax = self.data[d_bi]
                    d_bi += 1
            d_lbi += self.stride
        return returnMax

    def getMaxAlphaValue(self):
        d_bi = 0
        d_lbi = d_bi
        returnMax = None
        if (self.aOffset is not None):
            returnMax = 0
            for thisY in range(0, self.size[1]):
                d_bi = d_lbi
                for thisX in range(0, self.size[0]):
                    if self.data[d_bi+self.aOffset]>returnMax:
                        returnMax = self.data[d_bi +
                                              self.aOffset]
                    d_bi += self.byteDepth
                d_lbi += self.stride
        return returnMax

    def FillAllDestructivelyUsingByteColor(self, brushByteColor):
        self.FillAllDestructivelyUsingColorBytes(brushByteColor.getR(),
            brushByteColor.getG(), brushByteColor.getB(),
            brushByteColor.getA())

    def FillAllDestructivelyUsingColorBytes(self, setRByte, setGByte,
            setBByte, setAByte):
        d_bi = 0
        d_lbi = d_bi
        setBytes = bytes([setBByte, setGByte, setRByte, setAByte])
        for thisY in range(0,self.size[1]):
            d_bi = d_lbi
            for thisX in range(0,self.size[0]):
                self.data[d_bi+self.bOffset] = setBytes[0]
                self.data[d_bi+self.gOffset] = setBytes[1]
                self.data[d_bi+self.rOffset] = setBytes[2]
                self.data[d_bi+self.aOffset] = setBytes[3]
                d_bi += self.byteDepth
            d_lbi += self.stride
    def blit_copy_with_bo(self, input_buffer, input_stride,
            input_byteDepth, input_width, input_height, input_bOffset,
            input_gOffset, input_rOffset, input_aOffset):
        # this is much like LineCopy version, except instead of using
        # python array slicing it uses static_range_copy_with_bo
        input_stride = int(input_stride)
        input_width = int(input_width)
        input_height = int(input_height)
        input_byteDepth = int(input_byteDepth)
        IsToFillRestWithZeroes = True
        d_bi = 0
        s_bi = 0  # sourceByteIndex

        # force colorspace conversion:
        if (self.byteDepth>=3):
            if ((input_aOffset is not None) and
                    (input_bOffset is None) and
                    (input_gOffset is None) and
                    (input_rOffset is None)):
                input_bOffset = input_aOffset
                input_gOffset = input_aOffset
                input_rOffset = input_aOffset


        if (self.byteDepth>=3 and
                (input_byteDepth>=3 or input_byteDepth==1)):
            dl_zeroes = None
            if (input_height<self.height):
                dl_zeroes = bytearray(self.stride)
            if (input_width==self.size[0]):
                d_lpi = 0  # dest line pixel index
                s_lpi = 0  # sourceLinePixelIndex
                for destY in range(0, self.size[1]):
                    d_bi = d_lpi
                    s_bi = s_lpi
                    d_nlpi = d_lpi + self.stride
                        # NextDestLinePixelIndex
                    # NextSourceLinePixelIndex = (s_lpi +
                    #                             input_stride)
                    if (destY<input_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:
                        #           d_nlpi] = \
                        #     input_buffer[s_lpi:
                        #                  NextSourceLinePixelIndex]
                        # range_copy_with_bo(self.data,
                        #     d_lpi,
                        #     d_nlpi,
                        #     input_buffer, s_lpi,
                        #     NextSourceLinePixelIndex, input_bOffset,
                        #     input_gOffset, input_rOffset,
                        #     input_aOffset)
                        if (self.byteDepth==3):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.bOffset] = \
                                    input_buffer[s_bi + input_bOffset]
                                self.data[d_bi + self.gOffset] = \
                                    input_buffer[s_bi + input_gOffset]
                                self.data[d_bi + self.rOffset] = \
                                    input_buffer[s_bi + input_rOffset]
                                d_bi += self.byteDepth
                                s_bi += input_byteDepth
                        elif (self.byteDepth>=4):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.bOffset] = \
                                    input_buffer[s_bi + input_bOffset]
                                self.data[d_bi + self.gOffset] = \
                                    input_buffer[s_bi + input_gOffset]
                                self.data[d_bi + self.rOffset] = \
                                    input_buffer[s_bi + input_rOffset]
                                self.data[d_bi + self.aOffset] = \
                                    input_buffer[s_bi + input_aOffset]
                                d_bi += self.byteDepth
                                s_bi += input_byteDepth
                        elif (self.byteDepth==1):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.aOffset] = \
                                    input_buffer[s_bi + input_aOffset]
                                d_bi += self.byteDepth
                                s_bi += input_byteDepth
                            # if (destX<input_width):
                            # for d_chan in range(0,self.byteDepth):
                            # else:
                            #     break
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                        # static_range_copy_with_bo(self.data,
                        #     d_lpi,
                        #     d_nlpi, dl_zeroes,
                        #     0, self.stride, input_bOffset,
                        #     input_gOffset, input_rOffset,
                        #     input_aOffset)
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += input_stride
            elif (input_width > self.size[0]):
                d_lpi = 0
                s_lpi = 0
                for destY in range(0,self.height):
                    d_nlpi = d_lpi + self.stride
                    # NextSourceLinePixelIndex = (s_lpi +
                    #                             input_stride)
                    # NextSourceLinePixelIndexLIMITED:
                    s_nlpi_ltd = s_lpi + self.stride
                        # intentionally self.stride,
                        # to limit how much to get
                    if (destY<input_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:d_nlpi] = \
                        #     input_buffer[s_lpi:s_nlpi_ltd]
                        range_copy_with_bo(self.data, d_lpi, d_nlpi,
                                           input_buffer, s_lpi,
                                           s_nlpi_ltd, input_bOffset,
                                           input_gOffset, input_rOffset,
                                           input_aOffset)
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += input_stride
            else:  # elif (input_width < self.size[0]):
                d_lpi = 0  # dest line pixel index
                s_lpi = 0
                pdl_zeroes = bytearray(self.stride-input_stride)
                for destY in range(0,self.height):
                    d_nlpi = d_lpi + self.stride
                    # NextDestLinePixelIndexLIMITED:
                    d_nlpi_ltd = d_lpi + input_stride
                        # intentially input stride to limit self stride
                        # since source is smaller
                    NextSourceLinePixelIndex = s_lpi + input_stride
                    # s_nlpi_ltd = \
                    #     s_lpi + self.stride
                    # intentionally self.stride, to limit what to get
                    if (destY<input_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:
                        #           d_nlpi_ltd] = \
                        #     input_buffer[s_lpi:
                        #                  NextSourceLinePixelIndex]
                        range_copy_with_bo(self.data,
                            d_lpi,
                            d_nlpi_ltd,
                            input_buffer, s_lpi,
                            NextSourceLinePixelIndex, input_bOffset,
                            input_gOffset, input_rOffset, input_aOffset)
                        if IsToFillRestWithZeroes:
                            self.data[d_nlpi_ltd:d_nlpi] = pdl_zeroes[:]
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += input_stride
        else:
            print("Byte depth combination not implemented in" +
                  " blit_copy_with_bo: input_byteDepth=" +
                  str(input_byteDepth) + " to self.byteDepth" +
                  str(self.byteDepth))

    # drawToSelfTopLeft_LineCopy_FillRestWithTransparent
    def blit_copy(self, input_PPImage):
        blit_copy(input_PPImage.data, input_PPImage.stride,
                              input_PPImage.byteDepth,
                              input_PPImage.width, input_PPImage.height)

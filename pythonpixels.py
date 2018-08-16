import math

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

class PPAnimationMetaFrame:
    travel = None
    seconds = None
    passedSeconds = None
    index = None

    def __init__(self):
        self.travel = (0.0,0.0)
        # seconds = .0166  # 60fps
        self.seconds = .0333  # 30fps default
        self.index = 0  # index in a frame array
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

tau = math.pi * 2.0
eighthOfTau = math.pi / 4.0

class PPSpriteAbstract:

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
        # TODO: test this
        angleIndex = self.getAngleIndex(angleDegrees)
        return styleConstant + angleIndex + actionConstant

    def getAnimIndex_Rad(self, angleRadians, actionConstant,
            styleConstant):
        angleIndex = self.getAngleIndex(angleRadians)
        return styleConstant + angleIndex + actionConstant

    def getAngleIndex_Deg(self, angleDegrees):
        angleDegrees %= 360
        # NOTE: -361 % 360 is 359
        angleIndex = int((angleDegrees / 45.0) + .5)  # +.5 for rounding
        return angleIndex % 8

    def getAngleIndex_Rad(self, angleRadians):
        angleRadians = math.fmod(angleRadians, tau)
        # NOTE: math.fmod(-3, 2) is -1
        if angleRadians < 0:
            # minus negative is positive:
            angleRadians += tau
        angleIndex = int(
            round((angleRadians / eighthOfTau)))
        while angleIndex > 7:
            angleIndex -= 8
        return angleIndex

class PPUnscaledSprite:
    sourceOriginalRect = None
    sourceCroppedRect = None
    destRenderRect = None
    # offset within current animation:
    frameOffset = None

    def __init__(self):
        # list of PPAnimations:
        self.animations = []
        self.animations.append(PPAnimation())
        self.ANIM = 0  # PPSpriteAbstract.ANIM_Default
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
        # if (self.sourceCroppedRect.width<0):
        #     self.sourceCroppedRect.width = 0
        # if (self.destRenderRect.width<0):
        #     self.destRenderRect.width = 0
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

    def __init__(self, left, top, width, height):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def clamp_ip(self, screenRect):
        # clamp self TO the given screenRect and return that copy of
        # self (like pygame.screenRect clamp)
        itemRect = PPRect(self.left, self.top, self.width, self.height)

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
        self.byte_depth = 4
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
        # returnString += "@" + str(index)
    returnString += ")"
    return returnString

# formerly static_PixelFill_CustomByteOrders
def range_copy_with_bo(destImage,
        arrayDestStartByteIndex, arrayDestEndExByteIndex,
        sourceImage, arraySourceStartByteIndex,
        arraySourceEndExByteIndex):
    sourceByteDepth = sourceImage.byte_depth
    destByteDepth = destImage.byte_depth
    dst = destImage.data
    src = sourceImage.data
    bOffset = sourceImage.bOffset
    gOffset = sourceImage.gOffset
    rOffset = sourceImage.rOffset
    aOffset = sourceImage.aOffset
    maxByteDepth = destImage.byte_depth
    if (sourceImage.byte_depth < maxByteDepth):
        maxByteDepth = sourceImage.byte_depth
    # if (sourceByteDepth == destByteDepth):
        # if (sourceByteDepth == 4):
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
    # if (destRegionPixelCount<=sourceRegionPixelCount):
    if (maxByteDepth>=4):
        for relativeIndex in range(0,minPixelCount):
            dst[destIndex + destImage.bOffset] = \
                src[sourceIndex + bOffset]
            dst[destIndex + destImage.gOffset] = \
                src[sourceIndex + gOffset]
            dst[destIndex + destImage.rOffset] = \
                src[sourceIndex + rOffset]
            dst[destIndex + destImage.aOffset] = \
                src[sourceIndex + aOffset]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    elif (maxByteDepth==3):
        for relativeIndex in range(0,minPixelCount):
            dst[destIndex + destImage.bOffset] = \
                src[sourceIndex + bOffset]
            dst[destIndex + destImage.gOffset] = \
                src[sourceIndex + gOffset]
            dst[destIndex + destImage.rOffset] = \
                src[sourceIndex + rOffset]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    elif (maxByteDepth==1):
        destLastByte = destByteDepth - 1
        sourceLastByte = sourceByteDepth - 1
        destIndex += destLastByte
        sourceIndex += sourceLastByte
        # offset by byte_depth-1 so that gray will be written to RGBA
        # image's alpha or vice versa
        for relativeIndex in range(0,minPixelCount):
            # dst[destIndex + destImage.bOffset] = \
                # src[sourceIndex + bOffset]
            dst[destIndex] = src[sourceIndex]
            destIndex += destByteDepth
            sourceIndex += sourceByteDepth
    else:
        print("Not Yet Implemented in ")

def set_at_from_ivec_with_bo(
        dst, destStride, destByteDepth, vec2, brushColor,
        bOffset, gOffset, rOffset, aOffset):
    xCenter = int(vec2[0])
    yCenter = int(vec2[1])
    pixelByteIndex = destStride*yCenter + xCenter*destByteDepth
    # print ("pixelByteIndex:" + str(pixelByteIndex))
    # print ("len(pixelBuffer):" + str(len(dst)))
    # print("writing bytes...")
    dst[pixelByteIndex + bOffset] = brushColor[2]
    dst[pixelByteIndex + gOffset] = brushColor[1]
    dst[pixelByteIndex + rOffset] = brushColor[0]
    if (aOffset is not None) and (aOffset<destByteDepth):
        dst[pixelByteIndex + aOffset] = brushColor[3]


def set_at_from_fvec_with_bo(
        dst, destStride, destByteDepth, vec2, brushColor,
        bOffset, gOffset, rOffset, aOffset):
    xCenter = int(vec2[0])
    yCenter = int(vec2[1])
    pixelByteIndex = destStride*yCenter + xCenter*destByteDepth
    # print ("pixelByteIndex:" + str(pixelByteIndex))
    # print ("len(pixelBuffer):" + str(len(dst)))
    # print("writing bytes...")
    dst[pixelByteIndex + bOffset] = int(round(brushColor[2]*255.0))
    dst[pixelByteIndex + gOffset] = int(round(brushColor[1]*255.0))
    dst[pixelByteIndex + rOffset] = int(round(brushColor[0]*255.0))
    if (aOffset is not None) and (aOffset<destByteDepth):
        dst[pixelByteIndex + aOffset] = int(round(brushColor[4]*255.0))

def set_at_from_fcolor_with_bo(
        dst, destStride, destByteDepth, vec2, brushColor,
        bOffset, gOffset, rOffset, aOffset):
    xCenter = int(vec2[0])
    yCenter = int(vec2[0])
    pixelByteIndex = destStride*yCenter + xCenter*destByteDepth
    # print ("pixelByteIndex:" + str(pixelByteIndex))
    # print ("len(pixelBuffer):" + str(len(dst)))
    # print("writing bytes...")
    dst[pixelByteIndex + bOffset] = int(round(brushColor.b*255.0))
    dst[pixelByteIndex + gOffset] = int(round(brushColor.g*255.0))
    dst[pixelByteIndex + rOffset] = int(round(brushColor.r*255.0))
    if (aOffset is not None) and (aOffset<destByteDepth):
        dst[pixelByteIndex + aOffset] = int(round(brushColor.a*255.0))

# static_DrawToArray_ToTopLeft_LineCopy_FillRestWithTransparent
def blit_copy(dst_data, dst_stride,
              dst_byteDepth, dst_size,
              src_data, src_stride,
              src_byteDepth, src_size):
    """Draw to array
    Draw to top left using line copy, and fill rest with transparent.
    see also PPImage.blit_copy
    """
    dst_width, dst_height = dst_size
    src_width, src_height = src_size
    IsToFillRestWithZeroes = True
    if dst_byteDepth == src_byteDepth:
        dl_zeroes = None  # destLineOfZeroes
        if (src_height<dst_size[1]):
            dl_zeroes = bytearray(dst_stride)
        if (src_width==dst_width):
            d_lpi = 0
            s_lpi = 0
            for destY in range(0, dst_height):
                d_nlpi = d_lpi + dst_stride
                # NextSourceLinePixelIndex:
                s_nlpi = s_lpi + src_stride
                if (destY<src_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    dst_data[d_lpi:d_nlpi] = src_data[
                        s_lpi:s_nlpi]
                elif IsToFillRestWithZeroes:
                    dst_data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += dst_stride
                s_lpi += src_stride
        elif (src_width>dst_width):
            d_lpi = 0
            s_lpi = 0
            for destY in range(0, dst_height):
                d_nlpi = d_lpi + dst_stride
                # s_nlpi = s_lpi + src_stride
                # Must ensure same size! Use dst_stride:
                s_nlpi_ltd = s_lpi + dst_stride # intentionally dst
                if (destY<src_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    dst_data[d_lpi:d_nlpi] = src_data[
                        s_lpi:s_nlpi_ltd]
                elif IsToFillRestWithZeroes:
                    dst_data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += dst_stride
                s_lpi += src_stride
        else:  # elif (src_width<dst_width):
            d_lpi = 0
            s_lpi = 0
            # PartialDestLineOfZeroes:
            pdl_zeroes = bytearray(dst_stride-src_stride)
            for destY in range(0, dst_height):
                d_nlpi = d_lpi + dst_stride
                d_nlpi_ltd = d_lpi + src_stride
                # intentially src stride to limit self stride since
                #     # source is smaller
                s_nlpi = s_lpi + dst_stride # indentionally src
                # s_nlpi_ltd = s_lpi + dst_stride
                #     # intentionally dst_stride, to limit what to get
                if (destY<src_height):
                    # NOTE: width difference is already handled in outer
                    # "if" statement, for speed.
                    dst_data[d_lpi:d_nlpi_ltd] = src_data[
                        s_lpi:s_nlpi]
                    if IsToFillRestWithZeroes:
                        dst_data[d_nlpi_ltd:d_nlpi] = pdl_zeroes[:]
                elif IsToFillRestWithZeroes:
                    dst_data[d_lpi:d_nlpi] = dl_zeroes[:]
                else:
                    break
                d_lpi += dst_stride
                s_lpi += src_stride
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
        self.byte_depth = int(byte_depth)
        self.stride = self.size[0] * self.byte_depth
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
        print(str(self.get_dict(data_enable=False)))

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
        ret['tmp']['byte_depth'] = self.byte_depth
        ret['tmp']['stride'] = self.stride
        ret['tmp']['byteCount'] = self.byteCount
        ret['tmp']['debugEnabled'] = self.debugEnabled
        return ret

    def draw_line_ivec3_h(self, vec2, rgb_bytes, count):
        # 0 is x or width, 1 is y or height
        # crop first, then call internal method:
        endbefore = vec2[0] + count
        if vec2[0] < 0:
            diff = 0 - vec2[0]
            count -= diff
            vec2 = (vec2[0] + diff, vec2[1])
        elif endbefore > self.size[0]:
            count -= (endbefore - self.size[0])
        if vec2[1] < 0:
            count = 0
        elif vec2[1] >= self.size[1]:
            count = 0
        if count > 0:
            self._draw_line_ivec3_h(vec2, rgb_bytes, count)

    # aka draw_line_horizontal
    def _draw_line_ivec3_h(self, vec2, rgb_bytes, count):
        #self.set_ivec3_at(vec2, color)
        x, y = vec2
        b_i = self.stride*y + x*self.byte_depth + self.bOffset
        g_i = self.stride*y + x*self.byte_depth + self.gOffset
        r_i = self.stride*y + x*self.byte_depth + self.rOffset
        b = rgb_bytes[2]  # int(color.b*255.0+.5)
        g = rgb_bytes[1]  # int(color.g*255.0+.5)
        r = rgb_bytes[0]  # int(color.r*255.0+.5)
        if b_i > len(self.data):
            self.print_dump()
            raise IndexError("Could not finish in draw_line_ivec3_h--" +
                             " Tried to write at index:" + str(b_i) +
                             " pos:" + str((vec2)) +
                             " size:" + str((self.size)) +
                             " byte_depth:" + str(self.byte_depth) +
                             " stride:" + str(self.stride) +
                             " byteCount:" + str(self.byteCount)
            )
        for i in range(count):
            self.data[b_i] = b
            self.data[g_i] = g
            self.data[r_i] = r
            b_i += self.byte_depth
            g_i += self.byte_depth
            r_i += self.byte_depth

    def draw_line_ivec3_v(self, vec2, rgb_bytes, count):
        # 0 is x or width, 1 is y or height
        # crop first, then call internal method:
        endbefore = vec2[1] + count
        if vec2[1] < 0:
            diff = 0 - vec2[1]
            count -= diff
            vec2 = (vec2[0], vec2[1] + diff)
        elif endbefore > self.size[1]:
            count -= (endbefore - self.size[1])
        if vec2[0] < 0:
            count = 0
        elif vec2[0] >= self.size[0]:
            count = 0
        if count > 0:
            self._draw_line_ivec3_v(vec2, rgb_bytes, count)

    # aka draw_line_vertical
    def _draw_line_ivec3_v(self, vec2, rgb_bytes, count):
        #self.set_ivec3_at(vec2, color)
        x, y = vec2
        b_i = self.stride*y + x*self.byte_depth + self.bOffset
        g_i = self.stride*y + x*self.byte_depth + self.gOffset
        r_i = self.stride*y + x*self.byte_depth + self.rOffset
        b = rgb_bytes[2]  # int(color.b*255.0+.5)
        g = rgb_bytes[1]  # int(color.g*255.0+.5)
        r = rgb_bytes[0]  # int(color.r*255.0+.5)
        if b_i > len(self.data):
            self.print_dump()
            raise IndexError("Could not finish in draw_line_ivec3_h--" +
                             " Tried to write at index:" + str(b_i) +
                             " pos:" + str((vec2)) +
                             " size:" + str((self.size)) +
                             " byte_depth:" + str(self.byte_depth) +
                             " stride:" + str(self.stride) +
                             " byteCount:" + str(self.byteCount)
            )
        for i in range(count):
            self.data[b_i] = b
            self.data[g_i] = g
            self.data[r_i] = r
            b_i += self.stride
            g_i += self.stride
            r_i += self.stride

    def set_ivec3_at(self, vec2, rgb_bytes):
        # destPixelByteIndex:
        d_p_bi = self.stride*vec2[1] + vec2[0]*self.byte_depth
        # dst[d_p_bi + self.bOffset] = int(color.b*255.0+.5)
        # dst[d_p_bi + self.gOffset] = int(color.g*255.0+.5)
        # dst[d_p_bi + self.rOffset] = int(color.r*255.0+.5)
        self.data[d_p_bi + self.bOffset] = int(rgb_bytes[2]*255.0+.5)
        self.data[d_p_bi + self.gOffset] = int(rgb_bytes[1]*255.0+.5)
        self.data[d_p_bi + self.rOffset] = int(rgb_bytes[0]*255.0+.5)

    def set_at_from_fcolor(self, vec2, brushColor):
        """set color (including alpha) using color object
        brushColor: must have .r, .g, .b,
                    and must have .a unless self.aOffset is None
        """
        set_at_from_fcolor_with_bo(self.data,
            self.stride, self.byte_depth, vec2, brushColor,
            self.bOffset, self.gOffset, self.rOffset, self.aOffset)

    def set_at_from_fvec(self, vec2, brushColor):
        """set color (including alpha) using color object
        brushColor: must be a list of floats, each 0.0 to 1.0
        """
        set_at_from_fvec_with_bo(self.data,
            self.stride, self.byte_depth, vec2, brushColor,
            self.bOffset, self.gOffset, self.rOffset, self.aOffset)

    def set_at_from_ivec(self, vec2, brushColor):
        """set color (including alpha) using color object
        brushColor: must be a list of integers, each 0 to 255
        """
        set_at_from_ivec_with_bo(self.data,
            self.stride, self.byte_depth, vec2, brushColor,
            self.bOffset, self.gOffset, self.rOffset, self.aOffset)

    # def DrawFromWithAlpha(self, sourceVariableImage, vec2):

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
                #d_bi += self.byte_depth
                for channelIndex in range(0,self.byte_depth):
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
                    d_bi += self.byte_depth
                d_lbi += self.stride
        return returnMax

    def FillAllDestructivelyUsingByteColor(self, brushByteColor):
        self.fill_icolor(brushByteColor.getR(),
            brushByteColor.getG(), brushByteColor.getB(),
            brushByteColor.getA())

    def clear(self):
        self.fill_ivec4((0, 0, 0, 0))

    def fill_ivec4(self, color):
        if self.byte_depth >= 4:
            self.fill_icolor(color[0], color[1], color[2], color[3])
        else:
            self.fill_icolor(color[0], color[1], color[2])

    # formerly FillAllDestructivelyUsingColorBytess
    def fill_icolor(self, setRByte, setGByte, setBByte, setAByte):
        d_bi = 0
        d_lbi = d_bi
        setBytes = bytes([setBByte, setGByte, setRByte, setAByte])
        dst = self.data
        for thisY in range(0,self.size[1]):
            d_bi = d_lbi
            for thisX in range(0,self.size[0]):
                dst[d_bi+self.bOffset] = setBytes[0]
                dst[d_bi+self.gOffset] = setBytes[1]
                dst[d_bi+self.rOffset] = setBytes[2]
                dst[d_bi+self.aOffset] = setBytes[3]
                d_bi += self.byte_depth
            d_lbi += self.stride

    def blit_copy_with_bo(self, src_data, src_stride,
            src_byteDepth, src_size, src_bOffset,
            src_gOffset, src_rOffset, src_aOffset):
        # this is much like LineCopy version, except instead of using
        # python array slicing it uses static_range_copy_with_bo
        src_stride = int(src_stride)
        src_width = int(src_size[0])
        src_height = int(src_size[1])
        src_byteDepth = int(src_byteDepth)
        # print("blit_copy_with_bo: self.byte_depth: " +
              # str(self.byte_depth))
        # print("blit_copy_with_bo: src_byteDepth: " +
              # str(src_byteDepth))
        IsToFillRestWithZeroes = True
        d_bi = 0
        s_bi = 0  # sourceByteIndex

        # force colorspace conversion:
        if (self.byte_depth>=3):
            if ((src_aOffset is not None) and
                    (src_bOffset is None) and
                    (src_gOffset is None) and
                    (src_rOffset is None)):
                src_bOffset = src_aOffset
                src_gOffset = src_aOffset
                src_rOffset = src_aOffset
        else:
            if src_bOffset < 0:
                print("ERROR in blit_copy_with_bo: src_bOffset is " +
                      str(src_bOffset))
        has_any = False
        msg = None
        try:
            v = src_data[0]
            has_any = True
        except:
            msg = ("FATAL ERROR in" +
                   " blit_copy_with_bo:" +
                   " src_data non-array or no values.")
            raise ValueError(msg)

        try:
            src_data[0].get(" ")
            msg = ("FATAL ERROR in" +
                   " blit_copy_with_bo:" +
                   " src_data contains dicts (should have values)")
            raise TypeError(msg)
        except:
            pass
        try:
            src_data[0].get(" ")
            msg = ("FATAL ERROR in" +
                   " blit_copy_with_bo:" +
                   " src_data contains dicts (should have values)")
            raise TypeError(msg)
        except:
            pass
        #if not isinstance(src_data[0], type(self.data[0])):
        if is_sequence(src_data[0]):
            msg = ("FATAL ERROR in" +
                   " blit_copy_with_bo:" +
                   str(type(src_data[0])) +
                   " data in src_data" +
                   " (each entry should be " +
                   str(type(self.data[0])) +
                   ")")
                  # " but value at" +
                  # str(s_bi + src_bOffset) +
                  # " is " +
                  # str(src_data[s_i]))
            raise TypeError(msg)
        # Allow other value types such as float in case of float
        # color.

        if (self.byte_depth>=3 and
                (src_byteDepth>=3 or src_byteDepth==1)):
            dl_zeroes = None
            if (src_height<self.size[1]):
                dl_zeroes = bytearray(self.stride)
            if (src_width==self.size[0]):
                d_lpi = 0  # dest line pixel index
                s_lpi = 0  # sourceLinePixelIndex
                for destY in range(0, self.size[1]):
                    d_bi = d_lpi
                    s_bi = s_lpi
                    d_nlpi = d_lpi + self.stride
                        # NextDestLinePixelIndex
                    # s_nlpi = (s_lpi +
                    #                             src_stride)
                    if (destY<src_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:
                        #           d_nlpi] = \
                        #     src_data[s_lpi:
                        #                  s_nlpi]
                        # range_copy_with_bo(self.data,
                        #     d_lpi,
                        #     d_nlpi,
                        #     src_data, s_lpi,
                        #     s_nlpi, src_bOffset,
                        #     src_gOffset, src_rOffset,
                        #     src_aOffset)
                        if (self.byte_depth==3):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.bOffset] = \
                                    src_data[s_bi + src_bOffset]
                                self.data[d_bi + self.gOffset] = \
                                    src_data[s_bi + src_gOffset]
                                self.data[d_bi + self.rOffset] = \
                                    src_data[s_bi + src_rOffset]
                                d_bi += self.byte_depth
                                s_bi += src_byteDepth
                        elif (self.byte_depth>=4):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.bOffset] = \
                                    src_data[s_bi + src_bOffset]
                                self.data[d_bi + self.gOffset] = \
                                    src_data[s_bi + src_gOffset]
                                self.data[d_bi + self.rOffset] = \
                                    src_data[s_bi + src_rOffset]
                                self.data[d_bi + self.aOffset] = \
                                    src_data[s_bi + src_aOffset]
                                d_bi += self.byte_depth
                                s_bi += src_byteDepth
                        elif (self.byte_depth==1):
                            for destX in range(0, self.size[0]):
                                self.data[d_bi + self.aOffset] = \
                                    src_data[s_bi + src_aOffset]
                                d_bi += self.byte_depth
                                s_bi += src_byteDepth
                            # if (destX<src_width):
                            # for d_chan in range(0,self.byte_depth):
                            # else:
                            #     break
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                        # static_range_copy_with_bo(self.data,
                        #     d_lpi,
                        #     d_nlpi, dl_zeroes,
                        #     0, self.stride, src_bOffset,
                        #     src_gOffset, src_rOffset,
                        #     src_aOffset)
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += src_stride
            elif (src_width > self.size[0]):
                d_lpi = 0
                s_lpi = 0
                for destY in range(0, self.size[1]):
                    d_nlpi = d_lpi + self.stride
                    # s_nlpi = (s_lpi +
                    #                             src_stride)
                    # NextSourceLinePixelIndexLIMITED:
                    s_nlpi_ltd = s_lpi + self.stride
                        # intentionally self.stride,
                        # to limit how much to get
                    if (destY<src_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:d_nlpi] = \
                        #     src_data[s_lpi:s_nlpi_ltd]
                        range_copy_with_bo(self.data, d_lpi, d_nlpi,
                                           src_data, s_lpi,
                                           s_nlpi_ltd, src_bOffset,
                                           src_gOffset, src_rOffset,
                                           src_aOffset)
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += src_stride
            else:  # elif (src_width < self.size[0]):
                d_lpi = 0  # dest line pixel index
                s_lpi = 0
                pdl_zeroes = bytearray(self.stride-src_stride)
                for destY in range(0, self.size[1]):
                    d_nlpi = d_lpi + self.stride
                    # NextDestLinePixelIndexLIMITED:
                    d_nlpi_ltd = d_lpi + src_stride
                        # intentially src stride to limit self stride
                        # since source is smaller
                    s_nlpi = s_lpi + src_stride
                    # s_nlpi_ltd = \
                    #     s_lpi + self.stride
                    # intentionally self.stride, to limit what to get
                    if (destY<src_height):
                        # NOTE: width difference is already handled in
                        # outer "if" statement, for speed.
                        # self.data[d_lpi:
                        #           d_nlpi_ltd] = \
                        #     src_data[s_lpi:
                        #                  s_nlpi]
                        range_copy_with_bo(self.data,
                            d_lpi,
                            d_nlpi_ltd,
                            src_data, s_lpi,
                            s_nlpi, src_bOffset,
                            src_gOffset, src_rOffset, src_aOffset)
                        if IsToFillRestWithZeroes:
                            self.data[d_nlpi_ltd:d_nlpi] = pdl_zeroes[:]
                    elif IsToFillRestWithZeroes:
                        self.data[d_lpi:d_nlpi] = dl_zeroes[:]
                    else:
                        break
                    d_lpi += self.stride
                    s_lpi += src_stride
        else:
            print("Byte depth combination not implemented in" +
                  " blit_copy_with_bo: src_byteDepth=" +
                  str(src_byteDepth) + " to self.byte_depth" +
                  str(self.byte_depth))

    # drawToSelfTopLeft_LineCopy_FillRestWithTransparent
    def blit_copy(self, src_PPImage):
        blit_copy(self.data, self.stride,
                  self.byte_depth, self.size,
                  src_PPImage.data, src_PPImage.stride,
                  src_PPImage.byte_depth, src_PPImage.size)

    def get_rect(self):
        return PPRect(0, 0, self.size[0], self.size[1])

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def _blit_from(self, ppimage, pprect, source_rect):
        if pprect.width != source_rect.width:
            print("ERROR in _blit_from: does not support scaling," +
                  " but width of dest is " + str(pprect.width) +
                  " and width of source is " + str(source_rect.width))
        if pprect.height != source_rect.height:
            print("ERROR in _blit_from: does not support scaling," +
                  " but height of dest is " + str(pprect.height) +
                  " and height of source is " + str(source_rect.height))
        src_x = source_rect.left
        src_start_x = src_x
        src_y = source_rect.top
        src_right = src_x + source_rect.width
        src_bottom = src_y + source_rect.height
        dst_x = pprect.left
        dst_start_x = dst_x
        dst_y = pprect.top
        dst_right = dst_x + pprect.width
        dst_bottom = dst_y + pprect.height
        src_bd = ppimage.byte_depth
        dst_bd = self.byte_depth
        dst = self.data
        src = ppimage.data
        dst_stride = self.stride
        src_stride = ppimage.stride
        dst_bo = self.bOffset
        dst_go = self.gOffset
        dst_ro = self.rOffset
        dst_ao = self.aOffset
        src_bo = ppimage.bOffset
        src_go = ppimage.gOffset
        src_ro = ppimage.rOffset
        src_ao = ppimage.aOffset


        while dst_y < dst_bottom:
            dst_x = dst_start_x
            src_x = src_start_x
            if src_bd >= 4:
                while dst_x < dst_right:
                    dst_i = dst_y*dst_stride + dst_x*dst_bd
                    src_i = src_y*src_stride + src_x*src_bd
                    a = float(src[src_i + src_ao]) / 255.0
                    ia = 1.0 - a
                    for chan in range(dst_bd):
                        dst[dst_i + dst_bo] = int(round(ia*dst[dst_i + dst_bo] + a*src[src_i + dst_bo]))
                        dst[dst_i + dst_go] = int(round(ia*dst[dst_i + dst_go] + a*src[src_i + dst_go]))
                        dst[dst_i + dst_ro] = int(round(ia*dst[dst_i + dst_ro] + a*src[src_i + dst_ro]))
                    dst_x += 1
                    src_x += 1
            else:
                while dst_x < dst_right:
                    dst_i = dst_y*dst_stride + dst_x*dst_bd
                    src_i = src_y*src_stride + src_x*src_bd
                    for chan in range(dst_bd):
                        dst[dst_i + dst_bo] = src[src_i + dst_bo]
                        dst[dst_i + dst_go] = src[src_i + dst_go]
                        dst[dst_i + dst_ro] = src[src_i + dst_ro]
                    dst_x += 1
                    src_x += 1
            dst_y += 1
            src_y += 1


    def blit_from(self, ppimage, pprect):
        source_rect = ppimage.get_rect()
        self_rect = self.get_rect()
        if pprect.left < self_rect.left:
            diff = self_rect.left - pprect.left
            source_rect.left += diff
            source_rect.width -= diff
        if pprect.top < self_rect.top:
            diff = self_rect.top - pprect.top
            source_rect.top += diff
            source_rect.height -= diff
        final_rect = PPRect(pprect.left, pprect.top, pprect.width,
                            pprect.height)
        final_rect.clamp_ip(self_rect)
        if (final_rect.width > 0) and (final_rect.height > 0):
            self._blit_from(ppimage, final_rect, source_rect)

if __name__ == "__main__":
    print("This module should be imported by your program.")
    print("  tests:")
    size = (128, 128)
    src_img = PPImage(size)
    dst_img = PPImage(size)
    print("blit_copy_with_bo...")
    dst_img.blit_copy_with_bo(src_img.data, src_img.stride,
        src_img.byte_depth, src_img.size, src_img.bOffset,
        src_img.gOffset, src_img.rOffset, src_img.aOffset)
    print("  done testing pythonpixels.")

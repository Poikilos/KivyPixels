# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased] - 2019-06-30
(Finish manually merging diff from accidentally missed from
local version on personal cloud based on first working version or so;
mostly in kivyspritetouch.py; some are * new, as in not from branch)
### Added
- * PPRect copy
- drawKivyImage (formerly
  `drawFromKivyImage_ToTopLeft_FillRestWithTransparent`)
- * `irgb_from_hex`, `ibgr_from_hex`, `ivec3_from_hex`
- * Implement alpha_flags (similar to Pygame-like special_flags but
  only affects alpha) PPImage.BLEND_MAX by default (formerly didn't
  change alpha dest alpha the same)
- * Use new method `updateColorNames` to maintain an ordered list of
  colors for cycling (instead of using static `names` list)
  - Rename `names` to `self.palettes["CGA"]` for future use
- * "Virtual" methods for PPImage (raise `NotImplementedError`
  except for `getNew`)
- Add more implementation to custom `ColorPopup` class (based on Popup
  not on kivy ColorPicker).

### Changed
- * Rename `blit_from` to `blit`.
- * Use duck typing in `blit` to mimic pygame (accepts point or rect as
  dest).
- * Rename `hex2_int` to `hex2ToInt`.
- * Rename `vec3_from_hex` to `ivec3_from_hex`,
    `bgr_from_hex` to `fbgr_from_hex`, and
    `rgb_from_hex` to `frgb_from_hex`
	for clarity.
- * Fix totally broken hex conversion including the above and
  `hex2ToInt`.
- Account for different (errant?) channel order in Kivy 1.8.0
  (using `viewImage_?Offset` variables in `PixelWidget`)
- * Rename `set_brush_color_to_next_in_palette` to
  `setBrushColorToNextInPalette`
- * (kivypixels) Rename `set_brush_color` to `setBrushColor`
- * (kivypixels) Rename `get_new` to `getNew`
- Only try to save brush if brushImage is not None
  
### Removed
- * unused loop `for chan in range(dstBD):` just causing slowness
- * unused kv code (see unused/*.kv)
- ColorPicker (has fatal bug in Kivy 1.9.0)

## [Unreleased e0cb077] - 2019-06-28
(Continue to manually merge diff from accidentally missed from
local version on personal cloud based on first working version or so;
mostly in kivypixels.py)
### ToDo
- audit use of init to ensure correct params
  (since deleted trailing ,KPImage.defaultByteDepth,None params)
### Added
- tintByColorInstruction (formerly tint_by_color_instruction)

### Changed
- In load_image, and load, detect Kivy 1.8 to 1.9 changes
- improvements to tintByColor (had been renamed tint_by_color_vec4 in
  ownCloud branch) 

## [Unreleased] - 2019-06-28
(Manually merge diff from accidentally missed from local
version on personal cloud based on first working version or so;
mostly in pythonpixels.py)
### ToDo
- use `view_traceback` from common.py
- optionally forcefully flip during save (workaround for Kivy
  not un-flipping flipped texture)

### Added
- add common.py
- `copy_flipped_v`, `get_flipped`, `get_at`,
  blitFromCenter (formerly `draw_using_alpha_from_center`),
  `brushAt``, `get_dump`

### Changed
- Start switching from underscores to camel hump to reduce RSI
  and errors retyping from tutorials.

## [Unreleased]
### Added
- fill_ivec4, clear, get_rect, get_width, get_height

### Changed
- Make paletteColors dict instead of list (and thereby eliminate
  redColor, blueColor, greenColor)
- use `ColorPicker` instead of `BoxLayout`
- Make static methods into global functions.
  - Rename `static_PixelFill_CustomByteOrders`
    to `range_copy_with_bo`.
  - Rename `static_set_at_from_float_color_ToCustomByteOrder`
    to `set_at_from_ivec_with_bo`.
    - Change `atX, atY` param to `vec2`.
  - Rename
    `drawFromArray_ToTopLeft_FillRestWithTransparent_FromCustomByteOrder`
    to `blit_copy_with_bo`.
  - Rename `drawToSelfTopLeft_LineCopy_FillRestWithTransparent`
    to `blit_copy` (still as a method of PPImage in this case).
  - Rename
    `static_DrawToArray_ToTopLeft_LineCopy_FillRestWithTransparent`
	to `blit_copy`.
  - Rename and split `draw_line_horizontal`
    to `draw_line_ivec3_h` and `_draw_line_ivec3_h`.
  - Rename and split `draw_line_vertical`
    to `draw_line_ivec3_v` and `_draw_line_ivec3_v`
  - Rename `set_at` to `set_ivec3_at`.
  - Rename `set_at_from_float_color` to `set_at_from_fvec`.
  - Rename `static_createFromImageFile` to `load_image`
- Rename `FillAllDestructivelyUsingColorBytes` to `fill_icolor`
- Account for more conversion situations in `blit_copy_with_bo`
- Rename may dynamic variables in many methods so they have shorter
  names.
- Run tests and show a warning if a module runs as `"__main__"`.
- Make `static_blit` non-static, rename, and split into `blit_from`
  (automatically cropping using destination range) and `_blit_from`.
  (must fit inside dest, so normally use blit_from instead)
- Move `set_brush_color` to `KPImage`
- Move `brushAt` to `PPImage`
- Create `setBrushPath` in `KPImage` instead of manually loading a
  brush image.
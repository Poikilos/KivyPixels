# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased] - 2019-06-28
(Manually merge diff from accidentally missed from local
version on personal cloud based on first working version or so)
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
- Rename `FillAllDestructivelyUsingColorBytes` to `fill_icolor`
- Account for more conversion situations in `blit_copy_with_bo`
- Rename may dynamic variables in many methods so they have shorter names
- Run tests and show message if PythonPixels runs as `"__main__"`.
- Make `static_blit` non-static, rename, and split into `blit_from` (automatically cropping using destination range) and `_blit_from`. (must fit inside dest, so normally use blit_from instead)
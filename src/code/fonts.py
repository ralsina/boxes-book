import harfbuzz as hb
import freetype2 as ft


def adjust_widths_by_letter(boxes):
    """Takes a list of boxes as arguments, and uses harfbuzz to
    adjust the width of each box to match the harfbuzz text shaping."""
    buf = hb.Buffer.create()
    buf.add_str(''.join(b.letter for b in boxes))
    buf.guess_segment_properties()
    font_lib = ft.get_default_lib()
    face = font_lib.find_face('Arial')
    face.set_char_size(size=1, resolution=64)
    font = hb.Font.ft_create(face)
    hb.shape(font, buf)
    # at this point buf.glyph_positions has all the data we need
    for box, position in zip(boxes, buf.glyph_positions):
        box.w = position.x_advance

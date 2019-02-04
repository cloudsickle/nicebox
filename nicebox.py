"""
NiceBox is convenient wrapper for wx.BoxSizer and wx.StaticBoxSizer.
"""
import wx


def NiceBox(orient, parent=None, label=None):
    """Generate a NiceBox sizer for wx widgets."""
    if label is None:
        sizer_parent = wx.BoxSizer
        args, kwargs = (), {'orient': orient}
    elif parent is not None:
        static_box = wx.StaticBox(parent, label=label)
        sizer_parent = wx.StaticBoxSizer
        args, kwargs = (static_box,), {'orient': orient}
    else:
        raise ValueError('NiceBox must have a parent if a label is provided!')

    class NiceBox(sizer_parent):
        def __init__(self, orient, parent, label):
            super(NiceBox, self).__init__(*args, **kwargs)

            self.orient = orient

        def add(self, widget, align=None, border=0, grow=(0, 0)):
            _validate_align(align)
            _validate_border(border)
            _validate_grow(grow)

            self.Add(widget,
                     flag=_get_flag(align, border, grow, self.orient),
                     border=_get_border(border),
                     proportion=_get_proportion(grow, self.orient))

            return self

        def pad(self, size):
            """Add fixed space in the the dimension of the sizer."""
            if not _validate_positive_int(size):
                raise ValueError('Size must be a positive integer!')

            x = size if self.orient == wx.HORIZONTAL else -1
            y = size if self.orient != wx.HORIZONTAL else -1

            self.Add((x, y))

            return self

        def space(self, grow=1):
            """Add space that grows in the dimension of the sizer."""
            self.Add((-1, -1), proportion=grow)

            return self

    return NiceBox(orient, parent, label)


def _get_border(border):
    """Return the border size."""
    border = border if type(border) == int else max(border)
    return border


def _get_flag(align, border, grow, orient):
    """Determine the flags for the widget."""
    flag = 0

    if align is not None:
        top, right, bottom, left = align

        if top and bottom:
            flag |= wx.ALIGN_CENTER_VERTICAL
        elif top:
            flag |= wx.ALIGN_TOP
        elif bottom:
            flag |= wx.ALIGN_BOTTOM

        if left and right:
            flag |= wx.ALIGN_CENTER_HORIZONTAL
        elif left:
            flag |= wx.ALIGN_LEFT
        elif right:
            flag |= wx.ALIGN_RIGHT

    if type(border) == int:
        if border > 0:
            flag |= wx.ALL
    else:
        for val, side in zip(border, (wx.TOP, wx.RIGHT, wx.BOTTOM, wx.LEFT)):
            if val > 0:
                flag |= side

    expand = grow[1] if orient == wx.HORIZONTAL else grow[0]
    if expand:
        flag |= wx.EXPAND

    return flag


def _get_proportion(grow, orient):
    """Return the wx.Sizer.Add proportion argument."""
    if orient == wx.HORIZONTAL:
        return grow[0]
    else:
        return grow[1]


def _validate_align(align):
    """Ensure align is a tuple of four 1's and 0's."""
    if align is None:
        return True

    if type(align) not in (list, tuple):
        raise TypeError('align must be a tuple of four 1\'s and 0\'s!')

    try:
        assert len(align) == 4
        assert _validate_positive_ints(align)
        assert 0 <= max(align) <= 1
        assert 0 <= min(align) <= 1
    except (AssertionError, TypeError):
        raise ValueError('align must be a tuple of four 1\'s and 0\'s!')

    return True


def _validate_border(border):
    """Ensure the border is an integer or four integer tuple."""
    if _validate_positive_int(border):
        return True

    # At this point, border is not a positive integer
    if type(border) not in (list, tuple):
        raise TypeError(
            'border must be a positive integer or four integer tuple!')

    try:
        assert len(border) == 4
        assert _validate_positive_ints(border)
    except AssertionError:
        raise ValueError(
            'border must be a positive integer or four integer tuple!')

    # At this point, border is a four element tuple
    non_zero = [size for size in border if size > 0]
    if not non_zero:
        return True

    try:
        assert max(non_zero) == min(non_zero)
    except AssertionError:
        raise ValueError('border sizes must be equal!')

    return True


def _validate_grow(grow):
    """Ensure grow is a two element tuple of positive integers."""
    if type(grow) not in (list, tuple):
        raise TypeError('grow must be a tuple of two positive integers!')

    try:
        assert len(grow) == 2
        assert _validate_positive_ints(grow)
    except (AssertionError, AttributeError):
        raise ValueError('grow must be a tuple of two positive integers!')

    return True


def _validate_positive_int(value):
    """Ensure a value is a positive integer."""
    return type(value) == int and value >= 0


def _validate_positive_ints(iterable):
    """Ensure every value in the iterable is a positive integer."""
    try:
        return all(map(_validate_positive_int, iterable))
    except TypeError:
        return False


if __name__ == '__main__':
    pass

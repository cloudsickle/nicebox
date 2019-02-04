# nicebox: Convenient Box Sizers for wx Widgets

The nicebox module provides a NiceBox sizer which can be used in place of
wx.BoxSizer and wx.StaticBoxSizer.

## Usage

### Initializing

Use a NiceBox in the sample place you would use a box sizer in wx. A NiceBox
can be initiated like so:

    # This NiceBox is equivalent to a wx.BoxSizer
    nb = NiceBox(orient=wx.VERTICAL)
    
    # This NiceBox is equivalent to a wx.StaticBoxSizer, and has a border
    nb = NiceBox(orient=wx.VERITCAL, parent=panel, label='Settings')
    
Note that including a label argument will cause the NiceBox to inherit from 
wx.StaticBoxSizer. The parent argument is only used if the label is not None.

### Adding Widgets

Widgets are added to the sizer with the add() method. This method takes 
slightly different parameters than the wx box sizers, which make it easier to
use.

    nb.add(widget, align=(0, 1, 0, 1), border=(0, 5, 5, 5), grow=(1, 1))
    
The only required argument is the widget being added. Optional arguments:
- align: a (N, E, S, W) tuple of 1 or 0 indicating where to align the widget
- border: a (N, E, S, W) tuple of an integer border size, or a single 
integer if all sides have the same border. Note that mixed sizes can not be 
used.
- grow: a (X, Y) tuple where a non-zero value in the opposite dimension of 
the sizer sets the expand flag, and a non-zero value in the dimension of the
sizer is the proportion.

### Adding Padding
Fixed space padding can be added with the pad method.

    nb.pad(15)
    
### Adding Growable Space
Growable space can be added with the space() method where the input is the 
proportion. The default value is 1.

    nb.space()
    
### Chaining Methods
The NiceBox methods implement the builder pattern which allows for chaining
method calls. Remember the \ is needed in Python for line continuation.

    nb = NiceBox(orient=wx.VERTICAL) \
        .add(widget, grow=(1, 1), border=10) \
        .pad(5) \
        .add(gadget, align=(0, 1, 0, 1), border=(10, 0, 10, 10)) \
        .add(whosit, grow=(1, 0))
        
## Advantages

Why use NiceBox? Here a couple reasons with accompanying examples.

### Separation of Concerns

The box sizers in wx take a "flag" argument that bundles together options 
for alignment, borders, and widget expansion in the dimension opposite that 
of the sizer's orientation. The border size and widget expansion in the same
dimension as the sizer are the separate border and proportion arguments.

    # Without NiceBox
    bx = wx.BoxSizer(orient=wx.VERTICAL)
    bx.Add(widget, flag=wx.EXPAND | wx.RIGHT | wx.ALIGN_CENTER_HORIZONTAL | wx.TOP,
           border=10, proportion=1)
    
    # With NiceBox
    nb = NiceBox(orient=wx.VERTICAL) \
        .add(widget, align=(0, 1, 0, 1), border=(1, 1, 0, 0), grow=(1, 1))
        
Notice how in the wx example the alignment argument ended up in between the 
wx.RIGHT and wx.TOP values which affect the border. Also, remember that the 
wx.RIGHT value doesn't align the widget to the right, it enables the border.

In NiceBox, the "flag" options are separated into arguments that are easy to
read and don't require additional formatting work to keep organized.
        
### Simplified Parameter Syntax

Using the | operator on every line of code is fun, but it's much easier to 
keep track of a simple (N, E, S, W) tuple.

Even more helpful, grow is always in width, height order. This puts an end 
to trying to remember if you need to set expand or proportion.

    # Without NiceBox
    vbx = wx.StaticBox(panel, label='Example 2')
    vbx = wx.StaticBoxSizer(bx, orient=wx.VERTICAL)
    vbx.Add(hbx, flag=wx.BOTTOM, border=10)
    vbx.Add(widget, flag=wx.EXPAND | wx.BOTTOM, border=10)
    vbx.Add((0, -1), proportion=1)
    vbx.Add(gadget, flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
    
    # With NiceBox
    vnb = NiceBox(orient=wx.VERTICAL, parent=panel, label='Example 2') \
        .add(hbx, border=(0, 0, 10, 0)) \
        .add(widget, border=(0, 0, 10, 0), grow=(0, 1) \
        .space() \
        .add(gadget, align=(0, 1, 1, 0), grow=(1, 1))

## Fuller-Fledged Example

The code below is taken from the zetcode tutorial on layout management in 
wxpython, which can be found [here](http://zetcode.com/wxpython/layout/).
Widget initialization and settings are removed, leaving only the layout
commands used for the box sizers.

    vbox = wx.BoxSizer(wx.VERTICAL)

    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    hbox1.Add(st1, flag=wx.RIGHT, border=8)
    hbox1.Add(tc, proportion=1)
    vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

    vbox.Add((-1, 10))

    hbox2 = wx.BoxSizer(wx.HORIZONTAL)
    hbox2.Add(st2)
    vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

    vbox.Add((-1, 10))

    hbox3 = wx.BoxSizer(wx.HORIZONTAL)
    hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
    vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
        border=10)

    vbox.Add((-1, 25))

    hbox4 = wx.BoxSizer(wx.HORIZONTAL)
    hbox4.Add(cb1)
    hbox4.Add(cb2, flag=wx.LEFT, border=10)
    hbox4.Add(cb3, flag=wx.LEFT, border=10)
    vbox.Add(hbox4, flag=wx.LEFT, border=10)

    vbox.Add((-1, 25))

    hbox5 = wx.BoxSizer(wx.HORIZONTAL)
    hbox5.Add(btn1)
    hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
    vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

Here is the same layout using NiceBox.

    hbox1 = NiceBox(wx.HORIZONTAL) \
        .add(st1, border=(0, 8, 0, 0)) \
        .add(tc, grow=(1, 0))
        
    hbox2 = NiceBox(wx.HORIZONTAL).add(st2)
    
    hbox3 = NiceBox(wx.HORIZONTAL).add(tc2, grow=(1, 1))
    
    hbox4 = NiceBox(wx.HORIZONTAL) \
        .add(cb1) \
        .add(cb2, border=(0, 0, 0, 10)) \
        .add(cb3, border=(0, 0, 0, 10))
    
    hbox5 = NiceBox(wx.HORIZONTAL) \
        .add(btn1) \
        .add(btn2, border=(0, 0, 5, 5))

    vbox = NiceBox(wx.VERTICAL) \
        .add(hbox1, border=(10, 10, 0, 10), grow=(1, 0)) \
        .pad(10) \
        .add(hbox2, border=(10, 0, 0, 10)) \
        .pad(10) \
        .add(hbox3, border=(0, 10, 0, 10), grow=(1, 1)) \
        .pad(25) \
        .add(hbox4, border=(0, 0, 0, 10)) \
        .pad(25) \
        .add(hbox5, align=(0, 1, 0, 0), border=(0, 10, 0, 0))
        
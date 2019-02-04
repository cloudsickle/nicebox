"""
Tests for the nicebox module.
"""
import unittest

import nicebox
import wx


class ArgumentConverters(unittest.TestCase):

    def test__get_border(self):
        self.assertEqual(nicebox._get_border(5), 5)
        self.assertEqual(nicebox._get_border((0, 10, 0, 10)), 10)

    def test__get_flag(self):
        # General test
        wx_flag = wx.ALIGN_CENTER | wx.ALL | wx.EXPAND
        nb_flag = nicebox._get_flag((1, 1, 1, 1), 10, (0, 1), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        # Alignments
        wx_flag = wx.ALIGN_CENTER_VERTICAL
        nb_flag = nicebox._get_flag((1, 0, 1, 0), 0, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT
        nb_flag = nicebox._get_flag((1, 0, 1, 1), 0, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.ALIGN_BOTTOM | wx.ALIGN_CENTER_HORIZONTAL
        nb_flag = nicebox._get_flag((0, 1, 1, 1), 0, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.ALIGN_LEFT
        nb_flag = nicebox._get_flag((0, 0, 0, 0), 0, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.ALIGN_LEFT
        nb_flag = nicebox._get_flag(None, 0, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        # Borders
        wx_flag = wx.ALL
        nb_flag = nicebox._get_flag(None, 5, (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.TOP | wx.BOTTOM
        nb_flag = nicebox._get_flag(None, (5, 0, 5, 0), (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.ALL & ~wx.BOTTOM
        nb_flag = nicebox._get_flag(None, (5, 5, 0, 5), (0, 0), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        # Expand
        wx_flag = wx.EXPAND
        nb_flag = nicebox._get_flag(None, 0, (0, 1), wx.HORIZONTAL)
        self.assertEqual(wx_flag, nb_flag)

        wx_flag = wx.EXPAND
        nb_flag = nicebox._get_flag(None, 0, (1, 0), wx.VERTICAL)
        self.assertEqual(wx_flag, nb_flag)

    def test__get_proportion(self):
        self.assertEqual(nicebox._get_proportion((5, 1), wx.HORIZONTAL), 5)
        self.assertEqual(nicebox._get_proportion((1, 5), wx.VERTICAL), 5)


class ArgumentValidators(unittest.TestCase):

    def test__validate_align(self):
        self.assertTrue(nicebox._validate_align(None))
        self.assertTrue(nicebox._validate_align((1, 0, 0, 1)))

        # Values not in (1, 0), and wrong lengths
        with self.assertRaises(ValueError):
            nicebox._validate_align((0, -1, -1, 0))
        with self.assertRaises(ValueError):
            nicebox._validate_align((0, 1, 11, 0))
        with self.assertRaises(ValueError):
            nicebox._validate_align((0, 1, 1))
        with self.assertRaises(ValueError):
            nicebox._validate_align((0, 0, 0, 0, 1))

        # Wrong input types
        with self.assertRaises(TypeError):
            nicebox._validate_align(1)
        with self.assertRaises(TypeError):
            nicebox._validate_align({1, 2, 3, 4})

    def test__validate_border(self):
        self.assertTrue(nicebox._validate_border(10))
        self.assertTrue(nicebox._validate_border((10, 0, 0, 0)))

        # Negative values and wrong lengths
        with self.assertRaises(ValueError):
            nicebox._validate_border((0, -1, -1, 0))
        with self.assertRaises(ValueError):
            nicebox._validate_border((1, 1, 1))
        with self.assertRaises(ValueError):
            nicebox._validate_border((1, 1, 1, 1, 1))

        # Wrong input types
        with self.assertRaises(TypeError):
            nicebox._validate_border(5.0)
        with self.assertRaises(TypeError):
            nicebox._validate_border({1, 2, 3, 4})

        # Unequal borders
        with self.assertRaises(ValueError):
            nicebox._validate_border((10, 5, 0, 0))

    def test__validate_grow(self):
        self.assertTrue(nicebox._validate_grow((1, 1)))

        # Negative values and wrong lengths
        with self.assertRaises(ValueError):
            nicebox._validate_grow((-1, 0))
        with self.assertRaises(ValueError):
            nicebox._validate_grow((1, 1, 1))

        # Wrong input types
        with self.assertRaises(TypeError):
            nicebox._validate_grow(1)
        with self.assertRaises(TypeError):
            nicebox._validate_grow(1.0)
        with self.assertRaises(TypeError):
            nicebox._validate_grow({1, 2})


class PositiveIntValidators(unittest.TestCase):

    def test__validate_positive_int(self):
        self.assertTrue(nicebox._validate_positive_int(1))
        self.assertTrue(nicebox._validate_positive_int(0))

        # Negative integer
        self.assertFalse(nicebox._validate_positive_int(-1))

        # Wrong types
        self.assertFalse(nicebox._validate_positive_int((1,)))
        self.assertFalse(nicebox._validate_positive_int('1'))
        self.assertFalse(nicebox._validate_positive_int(1.0))

    def test__validate_positive_ints(self):
        self.assertTrue(nicebox._validate_positive_ints((0, 1, 0, 1)))
        self.assertTrue(nicebox._validate_positive_ints((0, 0, 0, 0)))

        # Negative integer
        self.assertFalse(nicebox._validate_positive_ints((1, 1, -1, 1)))

        # Non-iterable types
        self.assertFalse(nicebox._validate_positive_ints(1))
        self.assertFalse(nicebox._validate_positive_ints(1.0))


class NiceBoxFactory(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.top = wx.Frame(None, title='Test')

    def test_NiceBox(self):
        nb = nicebox.NiceBox(wx.HORIZONTAL)
        self.assertIsInstance(nb, wx.BoxSizer)
        self.assertEqual(nb.GetOrientation(), wx.HORIZONTAL)

        nb = nicebox.NiceBox(wx.VERTICAL, parent=self.top, label='Test')
        self.assertIsInstance(nb, wx.StaticBoxSizer)
        self.assertEqual(nb.GetOrientation(), wx.VERTICAL)

        with self.assertRaises(ValueError):
            nicebox.NiceBox(wx.HORIZONTAL, label='Test')


class NiceBoxMethods(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.top = wx.Frame(None, title='Test')
        self.nb = nicebox.NiceBox(orient=wx.VERTICAL)
        self.btn = wx.Button(self.top, label='Button')

    def test_add(self):
        self.nb.Clear()
        self.nb.add(self.btn)
        self.assertEqual(self.nb.GetItem(0).GetWindow(), self.btn)

    def test_pad(self):
        self.nb.Clear()
        self.nb.pad(10)
        self.assertEqual(self.nb.GetItem(0).GetSpacer(), (-1, 10))

    def test_space(self):
        self.nb.Clear()
        self.nb.space(2)
        self.assertEqual(self.nb.GetItem(0).GetSpacer(), (-1, -1))
        self.assertEqual(self.nb.GetItem(0).GetProportion(), 2)


if __name__ == '__main__':
    unittest.main()

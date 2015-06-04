__author__ = 'Shumix'

from Lab1 import *
import unittest
import time
import cStringIO

class TestFunction (unittest.TestCase):


    def test_take_url(self):
        self.assertSequenceEqual(take_url("<url>http://prikol.bigmir.net/all/pictures/</url>",
                                              lambda x: cStringIO.StringIO(x)),
                                 [5, 16, 5], "fail get list url", list)
    def test_to_xml_file(self):
        res = '<root> <brightnees1> 5 </brightnees1>  <brightnees2> 16 </brightnees2>  <brightnees3> 5 </brightnees3>  <brightnees1> 6 </brightnees1>  <brightnees2> 8 </brightnees2>  <brightnees3> 4 </brightnees3>  <brightnees1> 5 </brightnees1>  <brightnees2> 17 </brightnees2>  <brightnees3> 4 </brightnees3>  <brightnees1> 5 </brightnees1>  <brightnees2> 9 </brightnees2>  <brightnees3> 4 </brightnees3> </root>'
        with open("result.xml", "r") as f:
            f = f.read()
        self.assertEqual(res, f, "fail writing to xml")

    def test_main(self):
        self.assertIsInstance(sync_main_function("base.xml"), float, "fail main sync")
        self.assertIsInstance(async_main_function("base"), float, "fail main async")
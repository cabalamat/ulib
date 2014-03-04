# test_istream.py = test <istream.py>

"""
History:

25-Nov-2006:
wrote code to test IStream:getLine()

2-May-2007: added code to test IStream:grabToBefore()

4-Sep-2008: added code to test functionality of FileWrapper class

"""

import os

import lintest
import butil

import istream # module under test

#---------------------------------------------------------------------

class T_ScanString(lintest.TestCase):

    def setUp(self):
        s = "this is a string"
        self.ss = istream.ScanString(s)

    def test_getChar(self):
        r = self.ss.get()
        self.assertEqual(r, "t", "got char from ss")
        r = self.ss.get()
        self.assertEqual(r, "h", "got char from ss")
        r = self.ss.get()
        self.assertEqual(r, "i", "got char from ss")

    def test_getChars(self):
        r = self.ss.getChars(1)
        self.assertEqual(r, "t", "got char from ss")
        r = self.ss.getChars(3)
        self.assertEqual(r, "his", "got chars from ss")
        r = self.ss.getChars(0)
        self.assertEqual(r, "", "got no chars from ss")
        r = self.ss.getChars(0)
        self.assertEqual(r, "", "got no chars from ss")
        r = self.ss.getChars(-1)
        self.assertEqual(r, " is a string",
           "got all remaining  chars from ss")
        r = self.ss.getChars(4)
        self.assertEqual(r, "", "got no chars from ss")

    def test_peek(self):
        """ test ScanString's methods peekChar() and peekStr() """
        r = self.ss.peek(0)
        self.assertEqual(r, "t", "peeked char from ss")
        r = self.ss.peek(0)
        self.assertEqual(r, "t", "peeked same char from ss")
        r = self.ss.peek(0)
        self.assertEqual(r, "t", "peeked same char from ss")
        r = self.ss.get()
        self.assertEqual(r, "t", "got 0th char")
        r = self.ss.peekStr(5)
        self.assertEqual(r, "his i", "peeked 5 chars from ss")
        r = self.ss.get()
        self.assertEqual(r, "h", "got 1st char")


#---------------------------------------------------------------------

class T_PeekStream(lintest.TestCase):

    def setUp(self):
        s = "this is a string"
        self.ss = istream.ScanString(s)

    def test_isNext(self):
        r = self.ss.isNext("hello")
        self.assertEqual(r, False, "'hello' isn't next")
        r = self.ss.isNext("this")
        self.assertEqual(r, True, "'this' is next")
        r = self.ss.isNext("this")
        self.assertEqual(r, True, "'this' is still next")

        r = self.ss.get()
        self.assertEqual(r, "t", "got 0th char")
        r = self.ss.isNext("this")
        self.assertEqual(r, False, "'this' isn't next any more")
        r = self.ss.isNext("his i")
        self.assertEqual(r, True, "'his i' is next")

    def test_isNextSkip(self):
        r = self.ss.isNextSkip("hello")
        self.assertEqual(r, False, "'hello' isn't next")
        r = self.ss.isNextSkip("this")
        self.assertEqual(r, True, "'this' is next")
        r = self.ss.isNextSkip("this")
        self.assertEqual(r, False, "'this' isn't still next")

    def test_skipPastSet(self):
        r = self.ss.peek(0)
        self.assertEqual(r, "t", "peeked char from ss")
        self.ss.skipPastSet("hist")
        r = self.ss.get()
        self.assertEqual(r, " ")
        self.ss.skipPastSet("hist")
        r = self.ss.getChars()
        self.assertEqual(r, " a string")

    def test_word(self):
        """ isNextWord(), grabWord() """
        r = self.ss.isNextWord()
        self.assertEqual(r, True, "'this' is a word")
        r = self.ss.grabWord()
        self.assertEqual(r, 'this')
        r = self.ss.grabWord()
        self.assertEqual(r, 'is')
        r = self.ss.grabWord()
        self.assertEqual(r, 'a')
        r = self.ss.grabWord()
        self.assertEqual(r, 'string')
        r = self.ss.grabWord()
        self.assertEqual(r, '')
        r = self.ss.grabWord()
        self.assertEqual(r, '')


#---------------------------------------------------------------------

class T_IStream(lintest.TestCase):

    def setUp(self):
        s = "this is a string\nwith\n3 lines"
        self.ss = istream.ScanString(s)

    def test_getLine(self):
        r = self.ss.getLine()
        self.assertEqual(r, "this is a string\n")

        r = self.ss.getLine()
        self.assertEqual(r, "with\n")
        self.assertFalse(self.ss.eof(), "not at end of (ss)")

        r = self.ss.getLine()
        self.assertEqual(r, "3 lines")

        r = self.ss.getLine()
        self.assertTrue(self.ss.eof(), "at end of (ss)")
        self.assertEqual(r, "")

        r = self.ss.getLine()
        self.assertEqual(r, "")
        self.assertTrue(self.ss.eof(), "at end of (ss)")

    def test_getLines(self):
        r = self.ss.getLines()
        sb = [ "this is a string\n", "with\n", "3 lines"]
        self.assertEqual(r, sb)

    def test_getLines_2(self):
        r = self.ss.getLine()
        self.assertEqual(r, "this is a string\n")
        r = self.ss.getLines()
        sb = [ "with\n", "3 lines"]
        self.assertEqual(r, sb)

    def test_getAll(self):
        r = self.ss.getAll()
        sb = "this is a string\nwith\n3 lines"
        self.assertEqual(r, sb)

    def test_getChars(self):
        r = self.ss.getChars(2)
        sb = "th"
        self.assertEqual(r, sb, "got 1st 2 chars")
        r = self.ss.getChars(1)
        sb = "i"
        self.assertEqual(r, sb, "got next 1 char")
        r = self.ss.getChars(0)
        sb = ""
        self.assertEqual(r, sb, "got next 0 chars")
        r = self.ss.getChars()
        sb = "s is a string\nwith\n3 lines"
        self.assertEqual(r, sb, "got the rest of the string")

    def test_peekStr(self):
        r = self.ss.peekStr(0)
        sb = ""
        self.assertEqual(r, sb)
        r = self.ss.peekStr(0, 5)
        sb = ""
        self.assertEqual(r, sb)
        r = self.ss.peekStr(3)
        sb = "thi"
        self.assertEqual(r, sb)
        r = self.ss.peekStr(4, 3)
        sb = "s is"
        self.assertEqual(r, sb)
        r = self.ss.peekStr(4, 27)
        sb = "es"
        self.assertEqual(r, sb)
        r = self.ss.peekStr(4, 29)
        sb = ""
        self.assertEqual(r, sb)
        r = self.ss.peekStr(4, 30)
        sb = ""
        self.assertEqual(r, sb)

    def test_grabToString(self):
        r = self.ss.grabToString("")
        sb = ""
        self.assertEqual(r, sb)

        r = self.ss.grabToString("is")
        sb = "this"
        self.assertEqual(r, sb)

        r = self.ss.grabToString("is")
        sb = " is"
        self.assertEqual(r, sb)

        r = self.ss.grabToString("ing\n")
        sb = " a string\n"
        self.assertEqual(r, sb)

        r = self.ss.grabToString("xxx")
        sb = "with\n3 lines"
        self.assertEqual(r, sb)

        r = self.ss.grabToString("xxx")
        sb = ""
        self.assertEqual(r, sb)

    def test_grabToBefore(self):
        """ test the IStream:grabToBefore() method """
        r = self.ss.grabToBefore("is")
        sb = "th"
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore("is")
        sb = ""
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore("")
        sb = ""
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore(" a ")
        sb = "is is"
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore("nes")
        sb = " a string\nwith\n3 li"
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore("zap")
        sb = "nes"
        self.assertEqual(r, sb)

        r = self.ss.grabToBefore("zap")
        sb = ""
        self.assertEqual(r, sb)



#---------------------------------------------------------------------

class T_IFile(lintest.TestCase):
    """ test IFile class """

    def setUpAll(self):
        """ do once -- create file to put date in """
        butil.writeFile("test_for_IFile", "data")
        self.assertFileExists("test_for_IFile")

    def tearDownAll(self):
        """ do once -- delete file """
        os.remove("test_for_IFile")
        self.assertFileDoesNotExist("test_for_IFile")

    def test_create_IFile(self):
        f = open("test_for_IFile")
        fw = istream.IFile(file=f)
        ch = fw.get()
        self.assertSame(ch, "d", "1st char is 'd'")
        b = fw.eof()
        self.assertFalse(b, "not at end of file")
        ch = fw.get()
        self.assertSame(ch, "a")
        ch = fw.get()
        self.assertSame(ch, "t")
        ch = fw.get()
        self.assertSame(ch, "a")
        b = fw.eof()
        self.assertTrue(b, "at end of file")
        ch = fw.get()
        self.assertSame(ch, "")
        b = fw.eof()
        self.assertTrue(b, "at end of file")

#---------------------------------------------------------------------

class T_FileWrapper(lintest.TestCase):

    def setUpAll(self):
        """ do once -- create file to put date in """
        butil.writeFile("test_for_FileWrapper", "data")
        self.assertFileExists("test_for_FileWrapper")

    def tearDownAll(self):
        """ do once -- delete file """
        os.remove("test_for_FileWrapper")
        self.assertFileDoesNotExist("test_for_FileWrapper")

    def test_create_FileWrapper(self):
        f = open("test_for_FileWrapper")
        fw = istream.FileWrapper(file=f)
        ch = fw.get()
        self.assertSame(ch, "d", "1st char is 'd'")

#---------------------------------------------------------------------

group = lintest.TestGroup()
group.add(T_ScanString)
group.add(T_PeekStream)
group.add(T_IStream)
group.add(T_IFile)
#group.add(T_FileWrapper)

if __name__=="__main__": group.run()


#end

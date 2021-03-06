import os, sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import numheader

class TestNumHeader(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_encode16(self):
      result=numheader.encode16(0)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0]))

      result=numheader.encode16(127)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([127]))

      result=numheader.encode16(128)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0x80,0x80]))

      result=numheader.encode16(32767)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0xFF,0xFF]))

      result=numheader.encode16(32768)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0x80,0x00]))

      result=numheader.encode16(32895)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0x80,0x7F]))
      
      with self.assertRaises(ValueError):
         numheader.encode16(32896)
   
   def test_decode16(self):
      data = bytearray([0])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 1)
      self.assertEqual( value, 0)

      data = bytearray([127])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 1)
      self.assertEqual( value, 127)
   
      data = bytearray([0x80,0x80])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 2)
      self.assertEqual( value, 128)

      data = bytearray([0xFF,0xFF])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 2)
      self.assertEqual( value, 32767)

      data = bytearray([0x80,0x00])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 2)
      self.assertEqual( value, 32768)

      data = bytearray([0x80,0x7F])
      bytesParsed,value=numheader.decode16(data)
      self.assertEqual( bytesParsed, 2)
      self.assertEqual( value, 32895)
      
      
      
   
   def test_encode32(self):
      result=numheader.encode32(0)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0]))

      result=numheader.encode32(127)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([127]))

      result=numheader.encode32(128)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0x80,0x00,0x00,0x80]))

      data = bytearray()
      result=numheader.encode32( 2147483647)
      self.assertIsInstance(result, bytes)      
      self.assertEqual(result, bytes([0xFF,0xFF,0xFF,0xFF]))
      
      with self.assertRaises(ValueError):
         numheader.encode32(2147483648)

   def test_decode32(self):
      data = b"\x00"
      bytesParsed,value=numheader.decode32(data,0)
      self.assertEqual( bytesParsed, 1)
      self.assertEqual( value, 0)

      data = b"\x7F"
      bytesParsed,value=numheader.decode32(data,0)
      self.assertEqual( bytesParsed, 1)
      self.assertEqual( value, 127)
   
      data = b"\x80\x80"
      bytesParsed,value=numheader.decode32(data,0)
      self.assertEqual( bytesParsed, 0)      

      data = b"\x80\x00\x00\x80"
      bytesParsed,value=numheader.decode32(data,0)
      self.assertEqual( bytesParsed, 4)
      self.assertEqual( value, 128)

      data = b"\xFF\xFF\xFF\xFF"
      bytesParsed,value=numheader.decode32(data,0)
      self.assertEqual( bytesParsed, 4)
      self.assertEqual( value, 2147483647)
      
      data = b"\x00\x00\xFF\xFF\xFF\xFF"
      bytesParsed,value=numheader.decode32(data,2)
      self.assertEqual( bytesParsed, 4)
      self.assertEqual( value, 2147483647)

if __name__ == '__main__':
    unittest.main()
import unittest
import os
from PIL import Image
import toPDF

class TestImagesToPdf(unittest.TestCase):

    def setUp(self):
        self.input_directory_without_images = "/Users/f/Desktop/botik-v3/without_image/"
        self.input_directory_with_images = "/Users/f/Desktop/botik-v3/with_image/"
        self.input_directory_with_unreadable_images = "directory_path"
        self.non_existent_directory = "directory_path"

    def test_no_images(self):
        with self.assertRaises(Exception):
            toPDF.images_to_pdf(self.input_directory_without_images)

    def test_with_images(self):
        toPDF.images_to_pdf(self.input_directory_with_images)
        self.assertTrue(os.path.isfile(os.path.join(self.input_directory_with_images, "1.pdf")))

    def test_unreadable_images(self):
        with self.assertRaises(Exception):
            toPDF.images_to_pdf(self.input_directory_with_unreadable_images)

    def test_non_existent_directory(self):
        with self.assertRaises(Exception):
            toPDF.images_to_pdf(self.non_existent_directory)

if __name__ == "__main__":
    unittest.main()

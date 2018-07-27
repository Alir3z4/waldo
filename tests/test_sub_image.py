import io
import subprocess
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

import cv2
import numpy as np

from subimage import SubImage

BASE_DIR: Path = Path(__name__).parent
IMAGES_DIR: Path = BASE_DIR.joinpath('images')


class TestSubImage(TestCase):
    """Unit testing SubImage"""
    ORIGINAL_IMAGE_FILE_PATH: str = str(IMAGES_DIR.joinpath('puzzle.png'))
    CROPPED_IMAGE_FILE_PATH: str = str(IMAGES_DIR.joinpath('waldo.png'))

    @classmethod
    def setUpClass(cls):
        cls.ORIGINAL_IMAGE: np.ndarray = cv2.imread(cls.ORIGINAL_IMAGE_FILE_PATH)
        cls.CROPPED_IMAGE: np.ndarray = cv2.imread(cls.CROPPED_IMAGE_FILE_PATH)

    def test_get_images_in_order_upon_initializing(self) -> None:
        """Should return the images in order of original and cropped upon class initialization."""
        sub_image = SubImage(
            first_image_path=self.CROPPED_IMAGE_FILE_PATH,
            second_image_path=self.ORIGINAL_IMAGE_FILE_PATH
        )

        self.assertTrue(np.array_equal(sub_image.original_image, self.ORIGINAL_IMAGE))
        self.assertTrue(np.array_equal(sub_image.cropped_image, self.CROPPED_IMAGE))

    def test_get_images_in_order(self) -> None:
        """Should return the images in order of original and cropped."""
        first, second = SubImage.get_images_in_order(self.ORIGINAL_IMAGE, self.CROPPED_IMAGE)

        self.assertTrue(np.array_equal(first, self.ORIGINAL_IMAGE))
        self.assertTrue(np.array_equal(second, self.CROPPED_IMAGE))

        # Passing out of order images
        first, second = SubImage.get_images_in_order(self.CROPPED_IMAGE, self.ORIGINAL_IMAGE)

        self.assertTrue(np.array_equal(first, self.ORIGINAL_IMAGE))
        self.assertTrue(np.array_equal(second, self.CROPPED_IMAGE))

    def test_find_match(self) -> None:
        """Should find the match of the images."""
        sub_image = SubImage(self.ORIGINAL_IMAGE_FILE_PATH, self.CROPPED_IMAGE_FILE_PATH)

        self.assertIsNone(sub_image.find_match())
        self.assertEqual(sub_image.max_loc, (291, 1680))
        self.assertEqual(sub_image.min_loc, (1300, 852))
        self.assertEqual(sub_image.cropped_image.shape[:2], (sub_image.match_height, sub_image.match_width))

    def test_tell_top_left(self) -> None:
        """Should tell top left position of the cropped image from the original image."""
        capture_output = io.StringIO()
        sys.stdout = capture_output
        sub_image = SubImage(self.ORIGINAL_IMAGE_FILE_PATH, self.CROPPED_IMAGE_FILE_PATH)
        sub_image.find_match()
        sub_image.tell_top_left()

        self.assertEqual(capture_output.getvalue(), f'Top Left: {sub_image.min_loc}\n')

        sys.stdout = sys.__stdout__

    @patch('subimage.cv2.imshow')
    @patch('subimage.cv2.waitKey')
    def test_display(self, mock_wait_key: MagicMock, mock_imshow: MagicMock) -> None:
        """Should display the result in graphical view."""
        sub_image = SubImage(self.ORIGINAL_IMAGE_FILE_PATH, self.CROPPED_IMAGE_FILE_PATH)
        sub_image.find_match()

        capture_output = io.StringIO()
        sys.stdout = capture_output
        sub_image.display()
        sys.stdout = sys.__stdout__

        self.assertEqual(capture_output.getvalue(), 'Exit with pressing 0 (zero).\n')
        self.assertTrue(mock_wait_key.called)
        self.assertEqual(mock_wait_key.call_count, 1)
        self.assertEqual(mock_wait_key.call_args_list[0][0], (0, ))

        self.assertTrue(mock_imshow.called)
        self.assertEqual(mock_imshow.call_count, 2)
        self.assertEqual(mock_imshow.call_args_list[0][0][0], 'Original')
        self.assertEqual(mock_imshow.call_args_list[1][0][0], 'Cropped')
        self.assertTrue(np.array_equal(mock_imshow.call_args_list[1][0][1], self.CROPPED_IMAGE))

    def test_wrong_file_paths(self) -> None:
        """Should print out an error and stop the process."""
        expected_exc = None

        try:
            SubImage('yellow', self.CROPPED_IMAGE_FILE_PATH)
        except FileNotFoundError as exc:
            expected_exc = exc

        self.assertEqual(expected_exc.args, ('Image file yellow cannot be found.', ))

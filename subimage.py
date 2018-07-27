import sys
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


class SubImage:
    """
    SubImage.

    Finding a cropped image in its original.
    """
    def __init__(self, first_image_path: str, second_image_path: str):
        for file_name in [first_image_path, second_image_path]:
            if not Path(file_name).exists():
                raise FileNotFoundError(f'Image file {file_name} cannot be found.')

        self.original_image, self.cropped_image = self.get_images_in_order(
            first_image=cv2.imread(first_image_path),
            second_image=cv2.imread(second_image_path)
        )
        self.match_width: int = None
        self.match_height: int = None
        self.max_loc: Tuple[int] = None
        self.min_loc: Tuple[int] = None

    @staticmethod
    def get_images_in_order(first_image: np.ndarray, second_image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get the image in order.

        It should always return the original image as first and cropped one as second.
        """
        if sum(first_image.shape[:2]) > sum(second_image.shape[:2]):
            return first_image, second_image

        return second_image, first_image

    def find_match(self) -> None:
        """Find the cropped image in the original."""
        (self.match_height, self.match_width) = self.cropped_image.shape[:2]

        # find the waldo in the puzzle
        result: np.ndarray = cv2.matchTemplate(self.original_image, self.cropped_image, cv2.TM_CCOEFF_NORMED)
        (_, _, self.min_loc, self.max_loc) = cv2.minMaxLoc(result)

    def tell_top_left(self) -> None:
        """Print out the Top Left position of the image to stdout."""
        print(f'Top Left: {self.min_loc}')

    def display(self) -> None:
        """Will Display the cropped image on the original."""
        # Grab the bounding box of cropped image and extract it
        # from the original image
        top_left: Tuple[int] = self.max_loc
        bottom_right: Tuple[int] = (top_left[0] + self.match_width, top_left[1] + self.match_height)
        region_of_interest: np.ndarray = self.original_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # construct a darkened transparent 'layer' to darken everything
        # in the original image except for cropped image.
        mask: np.ndarray = np.zeros(self.original_image.shape, dtype="uint8")
        original: np.ndarray = cv2.addWeighted(self.original_image, 0.25, mask, 0.75, 0)
        original[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = region_of_interest

        # display the images
        cv2.imshow("Original", cv2.resize(original, (800, 600)))
        cv2.imshow("Cropped", self.cropped_image)

        print('Exit with pressing 0 (zero).')

        cv2.waitKey(0)


# Excluded from the code coverage report because the tests for this part
# are run in different process using subsprocess.check_output.
# Coverage is possible, but it's out of the scope of this task.
def main() -> None:  # pragma: no cover
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print('Usage: {0} image1.jpeg image2.jpeg --display[Optional]'.format(sys.argv[0]))
        exit()

    can_display: bool = sys.argv[3] == '--display' if len(sys.argv) >= 4 else False

    try:
        sub_image = SubImage(sys.argv[1], sys.argv[2])
    except FileNotFoundError as exc:
        print(exc.args[0])
        exit()

    sub_image.find_match()
    sub_image.tell_top_left()

    if can_display:
        sub_image.display()


if __name__ == '__main__':
    main()

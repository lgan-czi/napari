import matplotlib.pyplot as plt
import numpy as np

from napari._vispy.thumbnail import VispyThumbnail

# from napari._vispy.utils.visual import create_vispy_visual
from napari.layers import Image


def test_image():
    # np.random.seed(0)
    data = np.random.randint(255, size=(32, 32, 4), dtype=np.uint8)
    data = 255 * np.ones((32, 32, 4), dtype=np.uint8)
    plt.imshow(data)
    plt.show()
    # data = 255 * np.ones((32, 32, 4), dtype=np.uint8)
    data[:, :, 3] = 255
    layer = Image(data, rgb=True)
    thumbnail = VispyThumbnail(layer)

    thumbnail_image = thumbnail.get_image()

    plt.imshow(thumbnail_image)
    plt.show()
    # plt.imshow(data)
    # plt.show()

    np.testing.assert_array_equal(data, thumbnail_image)

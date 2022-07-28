import numpy as np

from napari._vispy.thumbnail import VispyThumbnail
from napari.layers import Image


def test_image(make_napari_viewer):
    data = np.random.randint(255, size=(32, 32, 4))
    print(data)
    layer = Image(data)
    thumbnail = VispyThumbnail(layer)

    thumbnail_image = thumbnail.get_image()

    np.testing.assert_array_equal(data, thumbnail_image)

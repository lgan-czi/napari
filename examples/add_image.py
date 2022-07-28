"""
Add image
=========

Display one image using the ``add_image`` API.
"""

from skimage import data
from skimage.io import imsave
import numpy as np
import napari


# create the viewer with an image
viewer = napari.view_image(data.astronaut(), rgb=True)
viewer.add_points(np.random.rand(10, 2) * 512)
qt_viewer = viewer.window.qt_viewer
thumb = qt_viewer.canvas.make_thumbnail(qt_viewer.layer_to_visual[viewer.layers[0]])
imsave('~/Desktop/test2.png', thumb)

if __name__ == '__main__':
    napari.run()

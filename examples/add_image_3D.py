"""
Display one image using the add_image API.
"""

from skimage import data
import napari


viewer = napari.view_image(data.binary_blobs(length=64, n_dim=3))

napari.run()

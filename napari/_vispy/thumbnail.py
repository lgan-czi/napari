import numpy as np
from vispy.scene import SceneCanvas

from napari._vispy import create_vispy_visual

THUMBNAIL_SIZE = (32, 32)


class VispyThumbnail(SceneCanvas):
    """Vispy canvas for drawing a thumbnail of a layer."""

    def __init__(self, layer):
        # We hide the canvas upon creation.
        super().__init__(show=False, size=THUMBNAIL_SIZE, resizable=False)

        # Unfreeze to add extra attributes/state.
        self.unfreeze()

        # Create a visual around the given layer, then attach it to a
        # central view.
        self.view = self.central_widget.add_view()
        self.visual = create_vispy_visual(layer)
        self.visual.node.parent = self.view

        # Modify the scale of the transform to make the thumbnail capture
        # the entire field of view.
        extent = layer._extent_world[:, :2]
        # print('extent', extent)
        size = extent[1] - extent[0]
        # print('size', size)
        scale = np.array(THUMBNAIL_SIZE) / size
        # print('scale', scale)
        self.visual.node.transform.scale(scale)

    def get_image(self):
        # Need to take a copy to ensure that QImage is properly constructed
        # (otherwise it can return None).
        return self.render().copy()

import numpy as np
from vispy.scene import SceneCanvas

from napari._vispy import create_vispy_visual

# from vispy.scene.cameras import PanZoomCamera


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
        self.view = self.central_widget.add_view(border_width=0)
        self.visual = create_vispy_visual(layer)
        self.visual.node.parent = self.view

        # Modify the scale of the transform to make the thumbnail capture
        # the entire field of view.
        extent = layer._extent_world[:, :2]
        size = extent[1] - extent[0]
        scale = np.array(THUMBNAIL_SIZE) / size
        # center = extent[0] + (size / 2)
        # print(scale)
        # print(center)
        # Modifying the node's transform seems to actually changed what is
        # rendered whereas changing the view's camera does not.
        self.visual.node.transform.scale(scale)
        # self.visual.node.transform.scale(scale, (0, 0))
        # self.visual.node.update()
        # camera_rect = list(extent[0]) + list(size)
        # self.view.camera = PanZoomCamera(aspect=1)
        # self.view.camera.flip = (0, 1, 0)
        # self.view.camera.rect = (-0.5, -0.5, 32, 32)
        # self.view.camera.view_changed()
        # self.update()

    def get_image(self):
        # Need to take a copy to ensure that QImage is properly constructed
        # (otherwise it can return None).
        return self.render().copy()

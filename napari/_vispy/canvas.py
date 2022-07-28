"""VispyCanvas class.
"""
from weakref import WeakSet

import numpy as np
from qtpy.QtCore import QSize
from vispy import gloo
from vispy.scene import SceneCanvas, Widget
from vispy.visuals.transforms import MatrixTransform

from ..utils.colormaps.standardize_color import transform_color
from .layers.base import VispyBaseLayer
from .utils.gl import get_max_texture_sizes


class VispyCanvas(SceneCanvas):
    """SceneCanvas for our QtViewer class.

    Add two features to SceneCanvas. Ignore mousewheel events with
    modifiers, and get the max texture size in __init__().

    Attributes
    ----------
    max_texture_sizes : Tuple[int, int]
        The max textures sizes as a (2d, 3d) tuple.

    """

    _instances = WeakSet()

    def __init__(self, *args, **kwargs):

        # Since the base class is frozen we must create this attribute
        # before calling super().__init__().
        self.max_texture_sizes = None
        self._last_theme_color = None
        self._background_color_override = None
        super().__init__(*args, **kwargs)
        self._instances.add(self)

        # Call get_max_texture_sizes() here so that we query OpenGL right
        # now while we know a Canvas exists. Later calls to
        # get_max_texture_sizes() will return the same results because it's
        # using an lru_cache.
        self.max_texture_sizes = get_max_texture_sizes()

        self.events.ignore_callback_errors = False
        self.native.setMinimumSize(QSize(200, 200))
        self.context.set_depth_func('lequal')

    def make_thumbnail(self, vispy_layer: VispyBaseLayer) -> np.ndarray:
        shape = (600, 800, 4)
        texture = gloo.Texture2D(shape=shape)
        fbo = gloo.FrameBuffer(texture, gloo.RenderBuffer(shape[:2]))
        self.push_fbo(fbo, offset=(0, 0), csize=shape[:2])
        self.context.clear(color='green', depth=True)
        node = vispy_layer.node
        transform = node.transform
        node.transform = MatrixTransform()
        extent = vispy_layer.layer._extent_world[:, 1::-1]
        size = extent[1] - extent[0]
        scales = np.array(shape[:2]) / size
        scale = [np.min(scales)] * 2
        center = extent[0] + (size / 2)
        node.transform.scale(scale, center)
        node.update()
        self.draw_visual(node)
        im = fbo.read()
        self.pop_fbo()
        node.transform = transform
        return im

    @property
    def destroyed(self):
        return self._backend.destroyed

    @property
    def background_color_override(self):
        return self._background_color_override

    @background_color_override.setter
    def background_color_override(self, value):
        self._background_color_override = value
        self.bgcolor = value or self._last_theme_color

    def _on_theme_change(self, event):
        self._set_theme_change(event.value)

    def _set_theme_change(self, theme: str):
        from ..utils.theme import get_theme

        # Note 1. store last requested theme color, in case we need to reuse it
        # when clearing the background_color_override, without needing to
        # keep track of the viewer.
        # Note 2. the reason for using the `as_hex` here is to avoid
        # `UserWarning` which is emitted when RGB values are above 1
        self._last_theme_color = transform_color(
            get_theme(theme, False).canvas.as_hex()
        )[0]
        self.bgcolor = self._last_theme_color

    @property
    def bgcolor(self):
        SceneCanvas.bgcolor.fget(self)

    @bgcolor.setter
    def bgcolor(self, value):
        _value = self._background_color_override or value
        SceneCanvas.bgcolor.fset(self, _value)

    @property
    def central_widget(self):
        """Overrides SceneCanvas.central_widget to make border_width=0"""
        if self._central_widget is None:
            self._central_widget = Widget(
                size=self.size, parent=self.scene, border_width=0
            )
        return self._central_widget

    def _process_mouse_event(self, event):
        """Ignore mouse wheel events which have modifiers."""
        if event.type == 'mouse_wheel' and len(event.modifiers) > 0:
            return
        super()._process_mouse_event(event)

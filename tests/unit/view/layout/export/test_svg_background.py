"""Unit tests for the SVG background (white by default, or transparent)."""

from typing import cast

import pytest
from defusedxml import ElementTree as ET

from src.pyArchimate import ArchiType
from src.pyArchimate.model import Model
from src.pyArchimate.view import View
from src.pyArchimate.view.layout.export import SVGExportService

SVG_NS = "{http://www.w3.org/2000/svg}"


@pytest.fixture
def view():
    m = Model("Test")
    v = cast(View, m.add(ArchiType.View, "V"))
    v.add(m.add(ArchiType.ApplicationComponent, "MyApp"), x=10, y=10, w=120, h=55)
    return v


def _background(svg_string: str):
    """Return the background rectangle (first rect child of the root), or None."""
    root = ET.fromstring(svg_string)
    first_rect = root.find(f"{SVG_NS}rect")
    return first_rect if first_rect is not None and first_rect.get("stroke") == "none" else None


def test_svg_export_service_transparent_background_defaults_false():
    assert SVGExportService().transparent_background is False


def test_white_background_by_default(view):
    background = _background(SVGExportService().to_svg(view))
    assert background is not None
    assert background.get("fill") == "white"


def test_no_background_when_transparent(view):
    assert _background(SVGExportService(transparent_background=True).to_svg(view)) is None


def test_view_to_svg_passes_transparent_background(view):
    assert _background(view.to_svg()) is not None
    assert _background(view.to_svg(transparent_background=True)) is None

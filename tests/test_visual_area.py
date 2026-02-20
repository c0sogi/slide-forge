"""Tests for VisualArea auto-layout container."""

from unittest.mock import MagicMock, patch

import pytest
from pptx.util import Emu

from slide_forge.default import get_presentation
from slide_forge.default.slide import (
    VisualArea,
    _CAPTION_BOX_HEIGHT,
    _CAPTION_GAP,
    _CONTENT_HEIGHT,
    _CONTENT_LEFT,
    _CONTENT_TOP,
    _CONTENT_WIDTH,
    _VISUAL_BOTTOM_MARGIN,
    _VISUAL_GAP,
    _VISUAL_TOP_GAP,
    add_chart,
    add_slide_title,
    add_table,
    create_slide,
    visual_area,
)


@pytest.fixture
def slide():
    prs = get_presentation()
    return create_slide(prs)


# ── factory defaults ────────────────────────────────────────


class TestVisualAreaDefaults:
    def test_default_top(self, slide):
        area = visual_area(slide)
        expected = int(_CONTENT_TOP) + int(_CONTENT_HEIGHT) + int(_VISUAL_TOP_GAP)
        assert area._top == expected

    def test_default_height(self, slide):
        area = visual_area(slide)
        expected_top = int(_CONTENT_TOP) + int(_CONTENT_HEIGHT) + int(_VISUAL_TOP_GAP)
        expected_height = 6_858_000 - int(_VISUAL_BOTTOM_MARGIN) - expected_top
        assert area._height == expected_height

    def test_default_left_width(self, slide):
        area = visual_area(slide)
        assert area._left == int(_CONTENT_LEFT)
        assert area._width == int(_CONTENT_WIDTH)

    def test_default_gap(self, slide):
        area = visual_area(slide)
        assert area._gap == int(_VISUAL_GAP)

    def test_custom_overrides(self, slide):
        area = visual_area(slide, left=100, top=200, width=300, height=400, gap=50)
        assert area._left == 100
        assert area._top == 200
        assert area._width == 300
        assert area._height == 400
        assert area._gap == 50


# ── empty / edge cases ──────────────────────────────────────


class TestEdgeCases:
    def test_empty_render(self, slide):
        area = visual_area(slide)
        result = area.render()
        assert result == []

    def test_double_render_raises(self, slide):
        area = visual_area(slide)
        area.render()
        with pytest.raises(RuntimeError, match="한 번만"):
            area.render()

    def test_add_after_render_raises(self, slide):
        area = visual_area(slide)
        area.render()
        with pytest.raises(RuntimeError, match="render\\(\\) 호출 후"):
            area.add_chart("column", categories=["A"], series={"S": [1]})

    def test_add_table_after_render_raises(self, slide):
        area = visual_area(slide)
        area.render()
        with pytest.raises(RuntimeError, match="render\\(\\) 호출 후"):
            area.add_table([["a"]])

    def test_add_figure_after_render_raises(self, slide):
        area = visual_area(slide)
        area.render()
        with pytest.raises(RuntimeError, match="render\\(\\) 호출 후"):
            area.add_figure("x.png")

    def test_add_shape_after_render_raises(self, slide):
        area = visual_area(slide)
        area.render()
        with pytest.raises(RuntimeError, match="render\\(\\) 호출 후"):
            area.add_shape("rectangle")

    def test_zero_weight_raises(self, slide):
        area = visual_area(slide)
        with pytest.raises(ValueError, match="weight"):
            area.add_chart("column", weight=0, categories=["A"], series={"S": [1]})

    def test_negative_weight_raises(self, slide):
        area = visual_area(slide)
        with pytest.raises(ValueError, match="weight"):
            area.add_table([["a"]], weight=-1)

    def test_chaining(self, slide):
        area = visual_area(slide)
        result = area.add_shape("rectangle")
        assert result is area


# ── layout: single element ──────────────────────────────────


class TestSingleElement:
    def test_single_chart_full_width(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]})
            results = area.render()

            assert len(results) == 1
            _, kwargs = mock.call_args
            assert kwargs["left"] == 0
            assert kwargs["width"] == 9000000
            assert kwargs["height"] == 2000000
            assert kwargs["top"] == 4000000

    def test_single_table_full_width(self, slide):
        with patch("slide_forge.default.slide.add_table", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_table([["H"], ["v"]])
            area.render()

            _, kwargs = mock.call_args
            assert kwargs["left"] == 0
            assert kwargs["width"] == 9000000
            # Table: height is NOT passed (auto-size)
            assert "height" not in kwargs

    def test_single_figure_full_width(self, slide):
        with patch("slide_forge.default.slide.add_figure", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_figure("img.png")
            area.render()

            _, kwargs = mock.call_args
            assert kwargs["left"] == 0
            assert kwargs["width"] == 9000000
            # Figure: height is NOT passed (auto aspect ratio)
            assert "height" not in kwargs


# ── layout: two elements ────────────────────────────────────


class TestTwoElements:
    def test_equal_weight_no_gap(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]})
            area.add_chart("column", categories=["B"], series={"S": [2]})
            area.render()

            assert mock.call_count == 2
            call1 = mock.call_args_list[0]
            call2 = mock.call_args_list[1]
            assert call1.kwargs["left"] == 0
            assert call1.kwargs["width"] == 4500000
            assert call2.kwargs["left"] == 4500000
            assert call2.kwargs["width"] == 4500000  # last absorbs remainder

    def test_equal_weight_with_gap(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=200000)
            area.add_chart("column", categories=["A"], series={"S": [1]})
            area.add_chart("column", categories=["B"], series={"S": [2]})
            area.render()

            # available = 9000000 - 200000 = 8800000, each = 4400000
            call1 = mock.call_args_list[0]
            call2 = mock.call_args_list[1]
            assert call1.kwargs["left"] == 0
            assert call1.kwargs["width"] == 4400000
            assert call2.kwargs["left"] == 4600000  # 4400000 + 200000 gap
            assert call2.kwargs["width"] == 4400000  # remainder: 9000000 - 4600000

    def test_weighted_2_1(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]}, weight=2)
            area.add_chart("column", categories=["B"], series={"S": [2]}, weight=1)
            area.render()

            call1 = mock.call_args_list[0]
            call2 = mock.call_args_list[1]
            assert call1.kwargs["width"] == 6000000  # 9M * 2/3
            assert call2.kwargs["left"] == 6000000
            assert call2.kwargs["width"] == 3000000  # remainder


# ── layout: three / four elements ───────────────────────────


class TestMultipleElements:
    def test_three_equal(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            for _ in range(3):
                area.add_chart("column", categories=["A"], series={"S": [1]})
            area.render()

            assert mock.call_count == 3
            assert mock.call_args_list[0].kwargs["width"] == 3000000
            assert mock.call_args_list[1].kwargs["left"] == 3000000
            assert mock.call_args_list[1].kwargs["width"] == 3000000
            assert mock.call_args_list[2].kwargs["left"] == 6000000
            assert mock.call_args_list[2].kwargs["width"] == 3000000

    def test_four_elements(self, slide):
        with patch("slide_forge.default.slide.add_shape", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=8000000, height=2000000, gap=0)
            for _ in range(4):
                area.add_shape("rectangle")
            area.render()

            assert mock.call_count == 4
            assert mock.call_args_list[0].kwargs["width"] == 2000000
            assert mock.call_args_list[3].kwargs["left"] == 6000000
            assert mock.call_args_list[3].kwargs["width"] == 2000000


# ── rounding fix ────────────────────────────────────────────


class TestRoundingFix:
    def test_last_element_absorbs_remainder(self, slide):
        """When weights don't divide cleanly, the last element absorbs the remainder."""
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            # 10000 / 3 = 3333.33... → int truncates to 3333
            area = visual_area(slide, left=0, top=4000000, width=10000, height=2000000, gap=0)
            for _ in range(3):
                area.add_chart("column", categories=["A"], series={"S": [1]})
            area.render()

            w1 = mock.call_args_list[0].kwargs["width"]
            w2 = mock.call_args_list[1].kwargs["width"]
            w3 = mock.call_args_list[2].kwargs["width"]
            # First two: int(10000 * 1/3) = 3333
            assert w1 == 3333
            assert w2 == 3333
            # Last absorbs remainder: 10000 - 3333 - 3333 = 3334
            assert w3 == 3334
            assert w1 + w2 + w3 == 10000


# ── caption budgeting ───────────────────────────────────────


class TestCaptionBudgeting:
    CAPTION_RESERVE = int(_CAPTION_GAP) + int(_CAPTION_BOX_HEIGHT)

    def test_chart_with_caption_reduces_height(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]}, caption="Fig 1")
            area.render()

            _, kwargs = mock.call_args
            assert kwargs["height"] == 2000000 - self.CAPTION_RESERVE

    def test_chart_without_caption_full_height(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]})
            area.render()

            _, kwargs = mock.call_args
            assert kwargs["height"] == 2000000

    def test_mixed_captions_per_element(self, slide):
        """Only elements WITH captions get reduced height."""
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock_chart:
            with patch("slide_forge.default.slide.add_shape", return_value=MagicMock()) as mock_shape:
                area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
                area.add_chart("column", categories=["A"], series={"S": [1]}, caption="Fig 1")
                area.add_shape("rectangle")
                area.render()

                # Chart has caption → reduced height
                assert mock_chart.call_args.kwargs["height"] == 2000000 - self.CAPTION_RESERVE
                # Shape has no caption → full height
                assert mock_shape.call_args.kwargs["height"] == 2000000

    def test_table_ignores_height_regardless(self, slide):
        """Table never gets explicit height (auto-size), even with caption."""
        with patch("slide_forge.default.slide.add_table", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_table([["H"], ["v"]], caption="Table 1")
            area.render()

            assert "height" not in mock.call_args.kwargs

    def test_figure_ignores_height_regardless(self, slide):
        """Figure never gets explicit height (aspect ratio preserved), even with caption."""
        with patch("slide_forge.default.slide.add_figure", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_figure("img.png", caption="Fig 1")
            area.render()

            assert "height" not in mock.call_args.kwargs


# ── per-kind height strategy ────────────────────────────────


class TestPerKindHeightStrategy:
    def test_chart_gets_container_height(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart("column", categories=["A"], series={"S": [1]})
            area.render()
            assert mock.call_args.kwargs["height"] == 2000000

    def test_shape_gets_container_height(self, slide):
        with patch("slide_forge.default.slide.add_shape", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_shape("rectangle")
            area.render()
            assert mock.call_args.kwargs["height"] == 2000000

    def test_table_gets_no_height(self, slide):
        with patch("slide_forge.default.slide.add_table", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_table([["H"], ["v"]])
            area.render()
            assert "height" not in mock.call_args.kwargs

    def test_figure_gets_no_height(self, slide):
        with patch("slide_forge.default.slide.add_figure", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_figure("img.png")
            area.render()
            assert "height" not in mock.call_args.kwargs


# ── kwargs forwarding ───────────────────────────────────────


class TestKwargsForwarding:
    def test_chart_kwargs_forwarded(self, slide):
        with patch("slide_forge.default.slide.add_chart", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_chart(
                "line_markers",
                categories=["Q1", "Q2"],
                series={"Rev": [100, 200]},
                title="Revenue",
                legend=False,
                number_format="0.0%",
            )
            area.render()

            kw = mock.call_args.kwargs
            assert kw["title"] == "Revenue"
            assert kw["legend"] is False
            assert kw["number_format"] == "0.0%"
            assert kw["categories"] == ["Q1", "Q2"]

    def test_table_kwargs_forwarded(self, slide):
        with patch("slide_forge.default.slide.add_table", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_table(
                [["H1", "H2"], ["a", "b"]],
                first_row=False,
                first_col=True,
                header_size=16,
                body_size=10,
            )
            area.render()

            kw = mock.call_args.kwargs
            assert kw["first_row"] is False
            assert kw["first_col"] is True
            assert kw["header_size"] == 16
            assert kw["body_size"] == 10

    def test_shape_kwargs_forwarded(self, slide):
        with patch("slide_forge.default.slide.add_shape", return_value=MagicMock()) as mock:
            area = visual_area(slide, left=0, top=4000000, width=9000000, height=2000000, gap=0)
            area.add_shape(
                "oval",
                fill="FF0000",
                transparency=50,
                text="Hello",
                bold=True,
            )
            area.render()

            kw = mock.call_args.kwargs
            assert kw["fill"] == "FF0000"
            assert kw["transparency"] == 50
            assert kw["text"] == "Hello"
            assert kw["bold"] is True


# ── integration test ────────────────────────────────────────


class TestIntegration:
    def test_chart_and_table_side_by_side(self, slide):
        """Real (non-mocked) integration: chart + table placed without error."""
        add_slide_title(slide, "Integration Test")
        area = visual_area(slide)
        area.add_chart(
            "column",
            categories=["A", "B", "C"],
            series={"S1": [10, 20, 30]},
            title="Test Chart",
        )
        area.add_table(
            [["Col1", "Col2"], ["x", "y"]],
            first_row=True,
        )
        results = area.render()
        assert len(results) == 2

    def test_render_returns_placed_objects(self, slide):
        """render() returns a list of the placed PPTX objects."""
        area = visual_area(slide)
        area.add_chart(
            "column",
            categories=["A", "B"],
            series={"S": [1, 2]},
        )
        results = area.render()
        assert len(results) == 1
        # add_chart returns a Chart object
        from pptx.chart.chart import Chart

        assert isinstance(results[0], Chart)

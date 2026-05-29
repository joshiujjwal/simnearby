"""Smoke test — verifies the reconstruction package is importable."""


def test_pipeline_package_importable() -> None:
    """The reconstruction pipeline package must be importable without errors."""
    import importlib

    pipeline = importlib.import_module("src.reconstruction.pipeline")
    assert pipeline is not None


def test_utils_package_importable() -> None:
    """The reconstruction utils package must be importable without errors."""
    import importlib

    utils = importlib.import_module("src.reconstruction.utils")
    assert utils is not None

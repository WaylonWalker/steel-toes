"""Main Testing Module.

Makes assertions based on each fixture from the ./conftest.py module
"""
import pytest
from kedro.framework.context import KedroContext

from steel_toes import SteelToes, whos_protected


def is_hooked(context: KedroContext, branch: str = "") -> None:
    """Assert that context has a SteelToes hook."""
    assert context.branch == branch
    assert len(context.hooks) == 1
    assert isinstance(context.hooks[0], SteelToes)


def is_empty(context: KedroContext, branch: str = "") -> None:
    """Empty pipelines should not swap filepaths on init.

    filepaths are only swapped after_catalog_created if they exist

    """
    assert context.branch == branch
    for dataset in context.catalog.list():
        try:
            d = getattr(context.catalog.datasets, dataset)
        except AttributeError:
            return
        assert ~hasattr(d, "_filepath_swapped")
        assert ~d.exists()


def is_protected(context: KedroContext, branch: str = "") -> None:
    """Ensure that the right datasets get protected."""
    assert context.branch == branch
    protected = whos_protected(context.catalog)
    assert len(protected) == len(
        context.pipeline.all_inputs().union(context.pipeline.all_outputs())
    )
    assert sorted(protected) == sorted(
        context.pipeline.all_inputs().union(context.pipeline.all_outputs())
    )


def is_swapped(context: KedroContext, branch: str = "") -> None:
    """Test that protected filepaths are swapped after test."""
    assert context.branch == branch
    for dataset in context.catalog.list():
        try:
            d = getattr(context.catalog.datasets, dataset)
        except AttributeError:
            return
        if dataset in context.pipeline.inputs() or "param" in dataset:
            assert ~hasattr(d, "_filepath_swapped")
        else:
            assert hasattr(d, "_filepath_swapped")
        assert d.exists()


def is_dry_cleaned(context: KedroContext, branch: str = "") -> None:
    """Ensure properly dry cleaned."""
    assert context.branch == branch
    for dataset in context.catalog.list():
        try:
            d = getattr(context.catalog.datasets, dataset)
        except AttributeError:
            return
        if dataset in context.pipeline.inputs() or "param" in dataset:
            assert ~hasattr(d, "_filepath_swapped")
        else:
            assert hasattr(d, "_filepath_swapped")
            assert "bob" in str(d._filepath)
        assert d.exists()


def is_cleaned(context: KedroContext, branch: str = "") -> None:
    """Ensure properly cleaned."""
    assert context.branch == "bob"
    for dataset in context.catalog.list():
        try:
            d = getattr(context.catalog.datasets, dataset)
        except AttributeError:
            return
        assert ~hasattr(d, "_filepath_swapped")
        if "param" not in dataset and "bob" not in dataset:
            assert "bob" not in str(d._filepath.stem)


@pytest.mark.usefixtures("config_dir")
class TestKedroContext:
    """Test class for testing core steel-toes functionality."""

    def test_hooked(self, dummy_context):
        """Dummy context should have a SteelToes hook."""
        is_hooked(dummy_context)

    def test_branched_hooked(self, branched_dummy_context):
        """Dummy context should have a SteelToes hook."""
        is_hooked(branched_dummy_context, "bob")

    def test_branched_announce_hooked(self, branched_announce_dummy_context):
        """Dummy context should have a SteelToes hook."""
        is_hooked(branched_announce_dummy_context, "bob")

    def test_empty_datasets(self, dummy_context):
        """Dummy context should be empty before running."""
        is_empty(dummy_context)

    def test_empty_datasets_branched(self, branched_dummy_context):
        """Dummy context should be empty before running."""
        is_empty(branched_dummy_context, branch="bob")

    def test_empty_datasets_branched_announce(self, branched_announce_dummy_context):
        """Dummy context should be empty before running."""
        is_empty(branched_announce_dummy_context, branch="bob")

    def test_after_run(self, ran_dummy_context):
        """Test that protected datasets get swapped after run."""
        is_swapped(ran_dummy_context)

    def test_after_branched_run(self, ran_branched_dummy_context):
        """Test that protected datasets get swapped after run."""
        is_swapped(ran_branched_dummy_context, "bob")

    def test_whos_protected(self, ran_dummy_context):
        """Test whos protected."""
        is_protected(ran_dummy_context)

    def test_branched_whos_protected(self, ran_branched_dummy_context):
        """Test whos protected."""
        is_protected(ran_branched_dummy_context, "bob")

    def test_after_dry_cleaned(self, dry_cleaned_dummy_context):
        """Ensure properly dry cleaned."""
        is_dry_cleaned(dry_cleaned_dummy_context, "bob")

    def test_after_cleaned(self, cleaned_dummy_context):
        """Ensures properly cleaned."""
        is_cleaned(cleaned_dummy_context)

"""Steel Toes Kedro Hook.

A hook that changes the filepath of your data based on current working git branch.

Example:
Since steel_toes requires access to the project_context to work properly you will
need to use a bit of an unconventional method to initialize your hooks.

    >>> from steel_toes import SteelToes
    >>> class ProjectContext(KedroContext):
    ...    project_name = "kedro0160"
    ...    project_version = "0.16.1"
    ...    package_name = "kedro0160"
    >>> @property
    >>> def hooks(self):
    ...    self._hooks = [ SteelToes(self) ]
    ...    return self._hooks

"""


from typing import Any, Dict, Union

from kedro.framework.context import KedroContext
from kedro.framework.hooks import hook_impl
from kedro.io.data_catalog import DataCatalog
from kedro.pipeline import Pipeline

from .core import announce_protection, get_current_branch, inject_branch


class SteelToes:
    """Steel Toes Kedro Hook.

    A hook that changes the filepath of your data based on current working git branch.

    Arguments:
        context (KedroContext): ProjectContext for your kedro project
        announce (bool): Announces protected datasets on startup. Default False
    Example:

    since steel_toes requires access to the project_context to work properly you will
    need to use a bit of an unconventional method to initialize your hooks.

        >>> from steel_toes import SteelToes
        >>> class ProjectContext(KedroContext):
        ...    project_name = "kedro0160"
        ...    project_version = "0.16.1"
        ...    package_name = "kedro0160"
        >>> @property
        >>> def hooks(self):
        ...    self._hooks = [ SteelToes(self) ]
        ...    return self._hooks

    """

    def __init__(
        self,
        context: KedroContext,
        branch: Union[str, None] = None,
        announce: bool = False,
    ) -> None:
        """Initialize a steel_toes kedro hook instance."""
        self.context = context
        project_path = str(self.context.project_path)
        if branch is None:
            branch = get_current_branch(
                project_path
                # self.context.project_path
            )  # pragma: no cover
        if branch is None:  # pragma: no cover
            # branch is not mocked
            self.branch = ""
        else:
            self.branch = branch
        self.announce = announce

    @hook_impl
    def before_pipeline_run(self, pipeline: Pipeline, catalog: DataCatalog) -> None:
        """Inject branch information `before_pipeline_run` if the dataset exists."""
        for dataset in pipeline.all_inputs():
            inject_branch(self.branch, catalog, dataset)

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog) -> None:
        """Inject branch information `after_catalog_created` if the dataset exists."""
        for dataset in catalog.list():
            inject_branch(self.branch, catalog, dataset)
        if self.announce:
            announce_protection(catalog)

    @hook_impl
    def after_node_run(self, catalog: DataCatalog, outputs: Dict[str, Any]) -> None:
        """Inject branch information `after_node_run`.

        On first run of a branch it will create this will create the dataset
        """
        for output in outputs:
            inject_branch(self.branch, catalog, output, save_mode=True)

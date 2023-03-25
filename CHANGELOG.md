## 0.3.0

* FEATURE - steel toes now allows you to specify ignore_types

### ignore_types

Some datasets have a `_filepath` attribute that is not meant for saving
datasets to and is not needed to be "branched", and should be ignored from
steel_toes, for example `SQLQueryDataSet`.

``` python
# settings.py
from kedro.extras.datasets.pandas.sql_dataset import SQLQueryDataSet, SQLTableDataSet

HOOKS = (SteelToes(ignore_types=[SQLQueryDataSet, SQLTableDataSet]),)
```

## 0.2.0

* FEATURE - steel toes will now prefer `STEEL_TOES_BRANCH` environment variable
    if it exists
* moved `.flake8` to `setup.cfg`
* `bump2version` now used for versioning

## 0.1.2

* FIX - `colorama` was not reset on announce and caused terminal color to remain red or green.

## 0.1.1
Now works with all filesystems

* FIX - use underlying _exists method from datasts so that it works with non local files

## 0.1.0

🎉 Initial release

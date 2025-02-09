from __future__ import annotations

from .consts import consts
from .data_fetchers import data_fetchers
from .eda import eda
from .forecasting import forecasting
from .preprocessing import preprocessing
from .statistics import statistics
from .utils import utils
from .workflow import workflow

__all__ = []
__all__ += consts.__all__
__all__ += utils.__all__
__all__ += data_fetchers.__all__
__all__ += forecasting.__all__
__all__ += eda.__all__
__all__ += statistics.__all__
__all__ += workflow.__all__
__all__ += preprocessing.__all__
__all__ += forecasting.__all__
__all__ += workflow.__all__
__all__ += ["cli"]


if __name__ == "__main__":
    from .workflow.entrypoint import cli

    cli()

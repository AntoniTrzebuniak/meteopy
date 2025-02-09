from __future__ import annotations

from .consts import *
from .data_fetchers import *
from .eda import eda
from .forecasting import *
from .preprocessing import *
from .statistics import *
from .utils import *
from .workflow import *

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

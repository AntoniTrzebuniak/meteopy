from __future__ import annotations

from meteopy.consts.dirs import Dirs
from meteopy.statistics.imgw_stats import IMGWStats

"""
fetcher = KODataFetcher()
fetcher.fetch(2019, 2020, 1)
handler = IMGWDataHandler()
handler.divide_downloaded()
handler.preprocess(2)"""

stats = IMGWStats()
typ = "synop"
stats.calculate_correlation([], "synop", Dirs.PARAMETER_MAP[typ][0], Dirs.PARAMETER_MAP[typ][1])

from __future__ import annotations

from meteopy.consts.dirs import Dirs
from meteopy.statistics.imgw_stats import IMGWStats
from meteopy.eda.imgw_eda_visualizer import IMGWDataVisualizer
from meteopy.data_fetchers.imgw_fetcher import KODataFetcher, SynopDataFetcher
from meteopy.preprocessing.imgw_handler import IMGWDataHandler
from meteopy.forecasting.imgw_simple_forecaster import IMGWSimpleForecaster

fetcher = KODataFetcher()
fetcher.fetch(2011, 2012, 2)
handler = IMGWDataHandler()
handler.divide_downloaded()
handler.preprocess(3)

stats = IMGWStats()
typ = "klimat"

#stats.calculate_correlation([], "synop", Dirs.PARAMETER_MAP[typ][0], Dirs.PARAMETER_MAP[typ][1])
visual = IMGWDataVisualizer()
fetcher = SynopDataFetcher()
fore = IMGWSimpleForecaster()




#fore.plot_forecast("klimat", "2000-01-01", "2001-12-31", "2002-12-31", ["249180010"], Dirs.PARAMETER_MAP["klimat"][2])
#stats.calculate_basic_stat("opad", Dirs.PARAMETER_MAP["opad"] )
#visual.plot_time_series(typ, [], "2007-01-01", "2007-12-31")

#stats.calculate_basic_stat([], typ, [])


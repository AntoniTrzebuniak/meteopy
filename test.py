from meteopy.data_fetchers.imgw_fetcher import IMGWDataFetcher
from meteopy.utils.log_module import get_logger
from meteopy.consts.dirs import Dirs

dir = Dirs()
print("\n", dir.get_root_path(), '\n')
print("\n", dir.get_data_path(), '\n')


fetcher=IMGWDataFetcher()
fetcher.fetch()
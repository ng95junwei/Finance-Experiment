import pandas as pd
import os
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = pd.Timestamp(os.environ.get('START_HISTORY'), tz='utc')
end_session = pd.Timestamp(os.environ.get('END_HISTORY'), tz='utc')

# register the bundle
register(
    os.environ.get('BUNDLE_NAME'),  # name we select for the bundle
    csvdir_equities(
        # name of the directory as specified above (named after data frequency)
        ['daily'],
        # path to directory containing the
        './',
    ),
    calendar_name='XNYS',  # NYSE
    start_session=start_session,
    end_session=end_session
)

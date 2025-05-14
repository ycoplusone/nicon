import lib.util as w2ji
import datetime
import time
from pytz import timezone
from datetime import datetime


exc_time = datetime(2025, 1, 23, 14, 50, 0) # 처리 시간
print( exc_time , type(exc_time) )

print( w2ji.get1HourOver( exc_time ) )
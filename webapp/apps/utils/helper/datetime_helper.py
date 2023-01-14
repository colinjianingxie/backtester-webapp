import pandas as pd

def trading_day_range(bday_start=None,bday_end=None,bday_freq='B', open_time='09:30',close_time='16:00',iday_freq='15T',weekmask=None):

	if bday_start is None: bday_start = pd.Timestamp.today()
	if bday_end is None: bday_end = bday_start + pd.Timedelta(days=1)

	daily = []

	for d in pd.bdate_range(start=bday_start,end=bday_end,freq=bday_freq,weekmask=weekmask):
		topen = pd.Timestamp(open_time)
		d1 = d.replace(hour=topen.hour,minute=topen.minute)
		tclose = pd.Timestamp(close_time)
		d2 = d.replace(hour=tclose.hour,minute=tclose.minute+1)
		daily.append(pd.date_range(d1,d2,freq=iday_freq))

	index = daily[0].union_many(daily[1:])

	return index

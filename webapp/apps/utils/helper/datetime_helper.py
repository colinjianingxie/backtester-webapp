def tz_to_naive(datetime_index):
    """Converts a tz-aware DatetimeIndex into a tz-naive DatetimeIndex,
    effectively baking the timezone into the internal representation.

    Parameters
    ----------
    datetime_index : pandas.DatetimeIndex, tz-aware

    Returns
    -------
    pandas.DatetimeIndex, tz-naive
    """
    # Calculate timezone offset relative to UTC
    timestamp = datetime_index[0]
    tz_offset = (timestamp.replace(tzinfo=None) -
                 timestamp.tz_convert('UTC').replace(tzinfo=None))
    tz_offset_td64 = np.timedelta64(tz_offset)

    # Now convert to naive DatetimeIndex
    return pd.DatetimeIndex(datetime_index.values + tz_offset_td64)

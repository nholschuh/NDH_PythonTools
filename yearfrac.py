from datetime import datetime as dt
import time
import numpy as np

def yearfrac(dates):
    """
    % (C) Nick Holschuh - Penn State University - 2015 (Nick.Holschuh@gmail.com)
    % This function takes a datetime object and converts it to a decimal year
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    %    date -- datetime object or list of datetime objects
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    %    date_output -- date as decimal year
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """    
    ##def sinceEpoch(tempdate): # returns seconds since epoch
    ##    return time.mktime(tempdate.timetuple())    
    ##
    ##if len(date) > 1:
    ##    date_output = []
    ##    for i in date:
    ##        s = sinceEpoch(i)

    ##        year = i.year
    ##        startOfThisYear = dt(year=year, month=1, day=1)
    ##        startOfNextYear = dt(year=year+1, month=1, day=1)

    ##        yearElapsed = s(i) - s(startOfThisYear)
    ##        yearDuration = s(startOfNextYear) - s(startOfThisYear)
    ##        fraction = yearElapsed/yearDuration
    ##        date_output.append(i.year+fraction)
    ##    
    ##else:
    ##    s = sinceEpoch(date)

    ##    year = date.year
    ##    startOfThisYear = dt(year=year, month=1, day=1)
    ##    startOfNextYear = dt(year=year+1, month=1, day=1)

    ##    yearElapsed = s(date) - s(startOfThisYear)
    ##    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    ##    fraction = yearElapsed/yearDuration

    ##    return date.year + fraction
    
    fracyears = []
    for date in dates:
        year = date.astype('datetime64[Y]').astype(int) + 1970  # numpy datetime64 years start from 1970
        
        # Calculate the start of the year and the start of the next year
        start_of_year = np.datetime64(f'{year}-01-01')
        start_of_next_year = np.datetime64(f'{year + 1}-01-01')
        
        # Calculate total days in the year and days elapsed
        days_in_year = (start_of_next_year - start_of_year).astype('timedelta64[D]').astype(int)
        days_elapsed = (date - start_of_year).astype('timedelta64[D]').astype(int)
        
        # Calculate the fractional year
        fracyears.append(year + days_elapsed / days_in_year)

    fractional_year = np.array(fracyears)
    return fractional_year
            
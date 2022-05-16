from datetime import datetime as dt
import time
import numpy as np

def yearfrac(date):
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
    
    if len(date) > 1:
        date_output = []
        for i in date:
            years = i.astype('datetime64[Y]').astype(int) + 1970
            months = i.astype('datetime64[M]').astype(int) % 12 + 1
            days = i - i.astype('datetime64[M]') + 1
            days = (days*1.15741e-14).astype('int')
            
            date_output.append(float(years)+float(months)/12+float(days)/365.25)
            
    return date_output
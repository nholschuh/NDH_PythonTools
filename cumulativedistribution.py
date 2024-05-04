import numpy as np

def cumulativedistribution(input_data,bins=50):
    """
    % (C) Nick Holschuh - Amherst College -- 2024 (Nick.Holschuh@gmail.com)
    % This function an input dataset and calculates a cumulative distribution function
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are as follows:
    %
    % input_data -- the array of values to use to calculate the cdf
    % bins -- the number of bins to assume in calculating the cdf.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are as follows:
    %
    % bin_vals -- These are the x coordinates on the cumulative distribution, 
    %             that correspond to the values on the right edge of each bin
    % cdf -- This is the cumulative distribution
    % pdf -- [NOT STRICTLY CORRECT] This is the percentage of the distribution
    %        that falls within each bin. This changes with bin size, so it is
    %        not a true pdf (which, in principle, has infinite bins)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%
    """
    # getting data of the histogram 
    count,bins_vals = np.histogram(input_data, bins=bins)
    # finding the PDF of the histogram using count values 
    pdf=count/sum(count)
    # using numpy np.cumsum to calculate the CDF
    # We can also find using the PDF values by looping and adding 
    cdf=np.cumsum(pdf)
    return bins_vals[1:],cdf,pdf
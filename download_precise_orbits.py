import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import gzip
import shutil
import os

def download_precise_orbits(date,outdir='./',debug_flag=0):

    ######### This handles typical GPS Files
    if isinstance(date,str):
        date_str = date.split('_')[-1].split('.')[0]
        date = datetime.strptime(date_str, '%Y%m%d%H%M')

    year = date.year
    doy = date.timetuple().tm_yday
    start_time_str = f"{year}{doy:03d}0000"  # Always start at 00:00 for daily product
    
    gps_epoch = datetime(1980, 1, 6)
    gps_week = int((date - gps_epoch).days / 7)

    # Duration and sampling interval (standard for final IGS products)
    duration = "01D"
    interval_clk = "30S"
    interval_sp3 = "05M"
    center='JPL'

    orbit_qual = ['ULT','FIN','RAP']

    for qual in orbit_qual:
        # Center code: JPL, IGS, etc.
        center_tag = '%s0OPS%s' % (center,qual)  # Assumes standard OPS RAPID format

        base_url = 'https://cddis.nasa.gov/archive/gnss/products/%0.4d/' % gps_week
        
        # File names
        clk_filename = '%s_%s_%s_%s_CLK.CLK.gz' % (center_tag,start_time_str,duration,interval_clk)
        sp3_filename = '%s_%s_%s_%s_ORB.SP3.gz' % (center_tag,start_time_str,duration,interval_sp3)
    
        session = requests.Session()
        session.auth = HTTPBasicAuth('', '')  # Leave empty to trigger .netrc usage
        session.trust_env = True              # Use system-level credentials

        files = [clk_filename,sp3_filename]

        success = 0
        try:
            for file in files:
                url = base_url + file
                response = session.get(url)
                if debug_flag == 1:
                    print('Attempting to download %s...' % url)
                if response.status_code == 200:
                    with open(file, 'wb') as f:
                        f.write(response.content)
                    success = 1
                else:
                    raise ValueError("No Data to Download")
                    
            print('Successfully downloaded %s orbit and clock type' % qual)
            break
        except:
            pass

    if os.path.isdir(outdir) == 0:
        os.mkdir(outdir)

    out_files = []
    for file in files:
        unzip_gz(file,outdir+file)
        out_files.append(outdir+file)
        os.remove(file)

    return(out_files)

def unzip_gz(file_path, out_path=None):
    if out_path is None:
        out_path = file_path.rstrip('.gz')  # Remove .gz extension
    if out_path[-2:] == 'gz':
        out_path = out_path.rstrip('.gz')
        
    with gzip.open(file_path, 'rb') as f_in:
        with open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    return out_path
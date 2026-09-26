import os
import re
import subprocess
import tempfile
import threading

################## NDH Tools self imports
###########################################################
from .cresis_season import cresis_season
###########################################################

def transfer_cresis_data(products,day_seg_frms=None,season=None,radar='rds',
                         host='nholschuh_sta@ssh.cresis.ku.edu',port=443,
                         src_root='/kucresis/scratch/dataproducts/opr_data',
                         dst_root='/mnt/data01/Data/RadarData/CReSIS_Filestructure/ct_data',
                         n_parallel=4,dry_run=True,skip_existing=False,verbose=True):
    """
    % (C) Nick Holschuh - Amherst College -- 2026 (Nick.Holschuh@gmail.com)
    %
    %     This function pulls merged (whole-frame) CReSIS/OPR data products
    %     from the processing machine to this one, with rsync over ssh. Only
    %     Data_YYYYMMDD_SS_FFF.mat files are transferred; the per-image
    %     Data_img_II_YYYYMMDD_SS_FFF.mat files, and anything else in the
    %     product directories, are left behind.
    %
    %     Paths are mirrored below the two roots:
    %       <src_root>/<radar>/<season>/CSARP_<product>/<day_seg>/Data_*.mat
    %       -> <dst_root>/<radar>/<season>/CSARP_<product>/<day_seg>/Data_*.mat
    %     so a product keeps its directory name (CSARP_standard3D_ndh stays
    %     CSARP_standard3D_ndh and never lands on the posted CSARP_standard).
    %
    %     The files are listed once, then split by size across n_parallel
    %     rsync streams that run at the same time, the way FileZilla runs
    %     several transfers at once. Files already present with the same size
    %     and modification time are skipped, an interrupted transfer resumes
    %     where it stopped (--partial), and files deleted at the source are
    %     never deleted here.
    %
    %     LOGIN. Python cannot answer a password prompt (ssh reads it from a
    %     terminal, which a notebook does not have), so one of these must be
    %     in place, and the function says which it is using:
    %       1. An ssh key accepted by the host (set up once, in a terminal):
    %            ssh-copy-id -p 443 nholschuh_sta@ssh.cresis.ku.edu
    %          Each stream then opens its own connection, which is fastest.
    %       2. A shared connection opened in a terminal, which lasts 8 hours:
    %            ssh -p 443 -fN -o ControlMaster=yes -o ControlPersist=8h
    %                -o ControlPath=~/.ssh/cm-%r@%h-%p nholschuh_sta@ssh.cresis.ku.edu
    %          The streams then share that one login.
    %     If neither is available the function stops and prints both commands.
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The inputs are:
    %
    %     products - product name or list of names, with or without the
    %                CSARP_ prefix (e.g. 'standard3D_ndh', ['music3D_ndh',
    %                'surfData_music3D_ndh','dd_surf_ndh'])
    %     day_seg_frms - None for every frame of every segment in the season,
    %                or a string / list of 'YYYYMMDD_SS' (whole segment) and
    %                'YYYYMMDD_SS_FFF' (one frame) entries
    %     season - season name (e.g. '2018_Antarctica_DC8'). If None, it is
    %                looked up from the first day_seg with cresis_season, so
    %                all entries must then be from one season.
    %     radar - radar directory under the roots (default 'rds')
    %     host - user@host of the processing machine; '' or None copies from
    %                a local src_root instead (for testing)
    %     port - ssh port (KU's ssh.cresis.ku.edu answers on 443, not 22)
    %     src_root, dst_root - the roots above <radar>
    %     n_parallel - number of rsync streams run at once (default 4)
    %     dry_run - True (default) lists what would move without moving it
    %     skip_existing - True never replaces a file that already exists here,
    %                even if the source copy has changed (rerun products)
    %     verbose - print the file list and progress
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     result - dictionary with
    %        'files': relative paths (CSARP_<product>/<day_seg>/Data_*.mat)
    %                 transferred, or that would be in a dry run
    %        'bytes': their total size
    %        'returncode': worst rsync exit status (0 is success)
    %        'commands': the rsync commands run, as lists
    %
    % Example:
    %     ndh.transfer_cresis_data(['standard3D_ndh','mvdr3D_ndh','music3D_ndh'],
    %                              ['20181010_02_006','20181018_01'])
    %     (check the list it prints, then run again with dry_run=False)
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    ############### Normalize the inputs
    if isinstance(products,str):
        products = [products]
    products = [p if p.startswith('CSARP_') else 'CSARP_'+p for p in products]

    if isinstance(day_seg_frms,str):
        day_seg_frms = [day_seg_frms]

    ############### Which files: merged frames only, per segment
    # seg_frms maps each day_seg to a list of frame numbers, or None for all
    seg_frms = {}
    if day_seg_frms is not None:
        for entry in day_seg_frms:
            m = re.fullmatch(r'(\d{8}_\d{2})(?:_(\d{3}))?',entry.strip())
            if m is None:
                raise ValueError(f'"{entry}" is not YYYYMMDD_SS or YYYYMMDD_SS_FFF')
            seg,frm = m.group(1),m.group(2)
            if frm is None:
                seg_frms[seg] = None
            elif seg not in seg_frms:
                seg_frms[seg] = [frm]
            elif seg_frms[seg] is not None:
                seg_frms[seg].append(frm)

    if season is None:
        if not seg_frms:
            raise ValueError('Give the season when day_seg_frms is None.')
        season = cresis_season(list(seg_frms)[0])['season']

    ############### rsync filter rules, anchored at the season directory
    # A directory has to be included for rsync to descend into it; the final
    # exclude drops everything not named, including every Data_img_* file
    merged = '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9]_[0-9][0-9][0-9].mat'
    rules = []
    for prod in products:
        rules.append(f'--include=/{prod}/')
        if not seg_frms:
            rules.append(f'--include=/{prod}/*/')
            rules.append(f'--include=/{prod}/*/Data_{merged}')
        for seg,frms in seg_frms.items():
            rules.append(f'--include=/{prod}/{seg}/')
            if frms is None:
                rules.append(f'--include=/{prod}/{seg}/Data_{seg}_[0-9][0-9][0-9].mat')
            else:
                for frm in sorted(set(frms)):
                    rules.append(f'--include=/{prod}/{seg}/Data_{seg}_{frm}.mat')
    rules.append('--exclude=*')

    src = f'{src_root.rstrip("/")}/{radar}/{season}/'
    if host:
        src = f'{host}:{src}'
    dst = os.path.join(dst_root,radar,season,'')

    ############### How to log in without a prompt
    base = ['rsync','-a','--partial']
    if skip_existing:
        base.append('--ignore-existing')
    if host:
        ssh = f'ssh -p {port} -o BatchMode=yes -o ConnectTimeout=20'
        control = '~/.ssh/cm-%r@%h-%p'
        key_ok = subprocess.run(ssh.split()+[host,'true'],stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL).returncode == 0
        if key_ok:
            login = 'ssh key'
        else:
            shared_ok = subprocess.run(['ssh','-p',str(port),'-o',f'ControlPath={control}','-O','check',host],
                                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0
            if not shared_ok:
                raise RuntimeError(
                    f'Cannot log in to {host} (port {port}) without a password. In a terminal, either\n'
                    f'  install a key once (asks for the password once):\n'
                    f'    ssh-copy-id -p {port} {host}\n'
                    f'  or open a shared connection that lasts 8 hours:\n'
                    f'    ssh -p {port} -fN -o ControlMaster=yes -o ControlPersist=8h '
                    f'-o ControlPath={control} {host}\n'
                    f'then run this again.')
            ssh = ssh + f' -o ControlPath={control}'
            login = 'shared connection'
        base += ['-e',ssh]
    else:
        login = 'local copy'

    ############### List the files once, with their sizes
    list_cmd = base + ['--dry-run','--prune-empty-dirs','--out-format=%l %n'] + rules + [src,dst]
    proc = subprocess.run(list_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if proc.returncode != 0:
        raise RuntimeError(f'Listing failed (rsync exit status {proc.returncode}):\n{proc.stderr.strip()}')
    listing = []
    for ln in proc.stdout.splitlines():
        size,_,name = ln.partition(' ')
        if name.endswith('.mat'):
            listing.append((int(size),name))
    total = sum(s for s,_ in listing)

    if verbose:
        print(('DRY RUN: ' if dry_run else '')+f'{src} -> {dst}  [{login}]')
        print('  products: '+', '.join(products))
        print('  frames: '+('all' if not seg_frms else ', '.join(
            f'{s} ({"all" if f is None else " ".join(sorted(set(f)))})' for s,f in seg_frms.items())))
        for size,name in listing:
            print(f'  {size/1e9:8.3f} GB  {name}')
        verb = 'would transfer' if dry_run else 'to transfer'
        print(f'{len(listing)} file(s), {total/1e9:.2f} GB {verb}')

    result = {'files':[n for _,n in listing],'bytes':total,'returncode':0,'commands':[list_cmd]}
    if dry_run or not listing:
        if dry_run and listing and verbose:
            print('Run again with dry_run=False to copy them.')
        return result

    ############### Split by size across the streams, largest files first
    n_streams = max(1,min(n_parallel,len(listing)))
    bins = [[] for _ in range(n_streams)]
    load = [0]*n_streams
    for size,name in sorted(listing,reverse=True):
        k = load.index(min(load))
        bins[k].append(name)
        load[k] += size

    ############### Run the streams at the same time
    os.makedirs(dst,exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix='transfer_cresis_')
    procs = []
    print_lock = threading.Lock()
    done = []

    def echo(k,stream):
        for ln in stream:
            ln = ln.strip()
            if ln.endswith('.mat'):
                with print_lock:
                    done.append(ln)
                    if verbose:
                        print(f'  [stream {k+1}] {ln}  ({len(done)} of {len(listing)})')

    threads = []
    for k,names in enumerate(bins):
        list_fn = os.path.join(tmpdir,f'files_{k+1}.txt')
        with open(list_fn,'w') as f:
            f.write('\n'.join(names)+'\n')
        cmd = base + ['--out-format=%n',f'--files-from={list_fn}',src,dst]
        result['commands'].append(cmd)
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        t = threading.Thread(target=echo,args=(k,p.stdout))
        t.start()
        procs.append(p)
        threads.append(t)

    for k,(p,t) in enumerate(zip(procs,threads)):
        t.join()
        err = p.stderr.read().strip()
        p.wait()
        if p.returncode != 0:
            print(f'  [stream {k+1}] rsync exit status {p.returncode}: {err}')
        result['returncode'] = max(result['returncode'],p.returncode)

    if verbose:
        print(f'{len(done)} of {len(listing)} file(s) transferred, {total/1e9:.2f} GB, '
              f'{n_streams} streams; worst rsync exit status {result["returncode"]}')
    result['files'] = done
    return result

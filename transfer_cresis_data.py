import os
import re
import subprocess

################## NDH Tools self imports
###########################################################
from .cresis_season import cresis_season
###########################################################

def transfer_cresis_data(products,day_seg_frms=None,season=None,radar='rds',
                         host='nholschuh_sta@ssh.cresis.ku.edu',
                         src_root='/kucresis/scratch/dataproducts/opr_data',
                         dst_root='/mnt/data01/Data/RadarData/CReSIS_Filestructure/ct_data',
                         dry_run=True,skip_existing=False,verbose=True):
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
    %     Everything requested goes in ONE rsync call, so ssh asks for a
    %     password / Duo push once. Files already present with the same size
    %     and modification time are skipped, and an interrupted transfer
    %     resumes where it stopped (--partial). Files deleted at the source
    %     are never deleted here.
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
    %     src_root, dst_root - the roots above <radar>
    %     dry_run - True (default) lists what would move without moving it
    %     skip_existing - True never replaces a file that already exists here,
    %                even if the source copy has changed (rerun products)
    %     verbose - print the rsync command and its file list
    %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % The outputs are:
    %
    %     result - dictionary with
    %        'files': relative paths (CSARP_<product>/<day_seg>/Data_*.mat)
    %                 transferred, or that would be in a dry run
    %        'command': the rsync command as a list
    %        'returncode': rsync's exit status (0 is success)
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

    ############### The transfer
    src = f'{src_root.rstrip("/")}/{radar}/{season}/'
    if host:
        src = f'{host}:{src}'
    dst = os.path.join(dst_root,radar,season,'')
    if not dry_run:
        os.makedirs(dst,exist_ok=True)

    cmd = ['rsync','-a','--partial','--prune-empty-dirs','--out-format=%n']
    if dry_run:
        cmd.append('--dry-run')
    if skip_existing:
        cmd.append('--ignore-existing')
    if host:
        cmd += ['-e','ssh']
    cmd += rules + [src,dst]

    if verbose:
        print(('DRY RUN: ' if dry_run else '')+f'{src} -> {dst}')
        print('  products: '+', '.join(products))
        print('  frames: '+('all' if not seg_frms else ', '.join(
            f'{s} ({"all" if f is None else " ".join(sorted(set(f)))})' for s,f in seg_frms.items())))

    ############### stdin stays attached so ssh can ask for a password / Duo
    proc = subprocess.run(cmd,stdout=subprocess.PIPE,text=True)
    files = [ln for ln in proc.stdout.splitlines() if ln.endswith('.mat')]

    if verbose:
        for fn in files:
            print('  '+fn)
        verb = 'would transfer' if dry_run else 'transferred'
        print(f'{len(files)} file(s) {verb}; rsync exit status {proc.returncode}')
        if dry_run and files:
            print('Run again with dry_run=False to copy them.')

    return {'files':files,'command':cmd,'returncode':proc.returncode}

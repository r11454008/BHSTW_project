import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    t1w    =  create_key('sub-{subject}/anat/sub-{subject}_T1w')
    Fun_T  =  create_key('sub-{subject}/func/sub-{subject}_task-GSSF_run-00{item:01d}_bold')
    t2w    =  create_key('sub-{subject}/anat/sub-{subject}_acq-{item:01d}_T2w')
    Fun_rest  =  create_key('sub-{subject}/func/sub-{subject}_task-rest_run-00{item:01d}_bold')   
    fMAP   =  create_key('sub-{subject}/fmap/sub-{subject}_acq-{item:01d}_magnitude')
    fMAP_P =  create_key('sub-{subject}/fmap/sub-{subject}_acq-{item:01d}_phasediff')
    DTI    =  create_key('sub-{subject}/dwi/sub-{subject}_dwi')
    info = {t1w: [],Fun_T:[],t2w:[], fMAP:[],DTI:[],Fun_rest:[],fMAP_P:[]}
    
    
    for idx, s in enumerate(seqinfo):
        if (s.dim1 == 288) and (s.dim3 == 208) and ('t1_mprage_sag_p2_3D_64ch' in s.protocol_name):
            info[t1w].append(s.series_id)
        if (s.dim1 == 256) and (s.dim2 == 256) and ('t2_tse_tra_256_4mm_2D_37Slices' in s.protocol_name):
            info[t2w].append(s.series_id)
        if (s.dim1 == 64) and (s.dim3 == 37) and ('ep2d_bold_3.9mm_TR2_Resting_180Scans' in s.protocol_name):
            info[Fun_rest].append(s.series_id)
        if (s.dim1 == 64) and (s.dim3 == 37) and ('ep2d_bold_3.9mm_TR2_Exp1_750Scans' in s.protocol_name):
            info[Fun_T].append(s.series_id)
        if (s.dim1 == 64) and (s.dim3 == 37) and ('ep2d_bold_3.9mm_TR2_Exp2_750Scans' in s.protocol_name):
            info[Fun_T].append(s.series_id)  
        if (s.dim1 == 64) and (s.dim3 == 37) and ('ep2d_bold_3.9mm_TR2_Exp3_750Scans' in s.protocol_name):
            info[Fun_T].append(s.series_id)  
        if (s.dim3 == 74) and (s.dim4 == 1) and ('gre_field_mapping' in s.protocol_name):
            info[fMAP].append(s.series_id) 
        if (s.dim3 == 37) and (s.dim4 == 1) and ('gre_field_mapping' in s.protocol_name):
            info[fMAP_P].append(s.series_id) 
        if (s.dim3 == 55) and (s.dim4 == 40) and ('ep2d_diff_DTI_b1000_30Dir' in s.protocol_name):
            info[DTI].append(s.series_id) 
    return info


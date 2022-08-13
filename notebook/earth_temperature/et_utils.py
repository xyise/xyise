import pandas as pd


# The functions below were taken from 'ghcnm' package by ncdc.noaa.gov
# get_stn_metadata and add_country_name are taken 'as-is'. 
# get_data file is a cut-down version. 

def get_stn_metadata(meta_fname, country_codes_file):

    ### Sanity Checks
    if (meta_fname.endswith('.inv') == False):
        raise ValueError('filename does not look correct')
    version = meta_fname.split('/')[-1].split('.')[2]
    if (version != 'v4'):
        raise ValueError('This filename appears to be for GHCN-M '+version+ \
                                    '. This has only been tested for v4')

    df = pd.read_fwf(meta_fname, colspecs=[(0,2), (0,12), (12,21), (21,31), 
                                                (31,38), (38,69)], 
                        names=['country_code','station',
                                'lat','lon','elev','name'])
    df = add_country_name(df, country_codes_file)
    df = df.drop(columns=['country_code'])
    return df


def add_country_name(df, country_codes_file=None):
    '''
    Convert country-codes to country-names
    https://www1.ncdc.noaa.gov/pub/data/ghcn/v4/ghcnm-countries.txt
    '''
    if country_codes_file == None:
        country_codes_file = 'ghcnm-countries.txt'
    cc = pd.read_fwf(country_codes_file, widths=[3,45], 
                        names=['country_code','country'])
    df = pd.merge(df, cc, on='country_code', how='outer')
    return df


def get_data(data_fname):

    ##############################
    # Sanity Checks
    ##############################
    if (data_fname.endswith('.dat') == False):
        raise ValueError('filename does not look correct')
    version = data_fname.split('/')[-1].split('.')[2]
    if (version != 'v4'):
        raise ValueError('This filename appears to be for GHCN-M '+version+ \
                                    '. This has only been tested for v4')

    ##############################
    # read in whole data file
    ##############################
    colspecs = [(0,2),(0,11),(11,15),(15,19)]      
    names    = ['country_code','station','year','variable']

    i = 19
    for m in range(1,13):

        mon = str(m)
        colspecs_tmp = [(i,i+5),     (i+5,i+6),    (i+6,i+7),    (i+7,i+8)   ]
        names_tmp    = ['VALUE'+mon, 'DMFLAG'+mon, 'QCFLAG'+mon, 'DSFLAG'+mon]

        for j in range(0,4):
            colspecs.append(colspecs_tmp[j]) 
            names.append(names_tmp[j])

        i = i+8

    df = pd.read_fwf(data_fname, colspecs=colspecs, names=names)        

    return df

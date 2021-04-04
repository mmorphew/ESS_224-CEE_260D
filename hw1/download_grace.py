'''
Example script for downloading GRACE data from PO.DAAC following example at:
https://github.com/nasa/podaacpy/blob/4fbebe6a58ae0261b8fd8f0d70100f5c0377b305/examples/Using%20podaacpy%20to%20interact%20with%20PO.DAAC%20Drive.ipynb

Dataset search code (lines 21-28) was used to find relevent granule names but is not
used in the actual download. To use the script yourself, you must create an .ini file
with earthdata username PO.DAAC Drive API password. Example .ini file:
https://github.com/nasa/podaacpy/blob/4fbebe6a58ae0261b8fd8f0d70100f5c0377b305/examples/podaac.ini

'''

from pprint import pprint
import podaac.podaac as podaac
import podaac.podaac_utils as utils
from podaac import drive as drive

p = podaac.Podaac()
u = utils.PodaacUtils()
d = drive.Drive('/mnt/tiffy/conor/rs_of_h/podaac.ini', None, None)

# use this to find ds names of JPL, GFZ, CSR data products
#result = u.list_all_available_granule_search_dataset_ids()
result = u.list_all_available_granule_search_dataset_short_names()
dsetShortName = [i for i in result if 'GRAC' in i and 'CSR' in i]

jpl_ds_str = 'TELLUS_GRAC_L3_JPL_RL06_LND_v03'
gfz_ds_str = 'TELLUS_GRAC_L3_GFZ_RL06_LND_v03'
csr_ds_str = 'TELLUS_GRAC_L3_CSR_RL06_LND_v03'

ds_result = p.dataset_search(short_name=gfz_ds_str,
                             start_time='2002-01-01',
                             end_time='2018-12-31')

jpl_id = 'PODAAC-TELND-3AJ63'
gfz_id = 'PODAAC-TELND-3AG63'
csr_id = 'PODAAC-TELND-3AG63'

result = p.granule_search(dataset_id=csr_id,
                          start_time='2002-01-01T00:00:01Z',
                          end_time='2018-12-31T11:59:59Z',
                          sort_by='timeAsc',
                          items_per_page='500',
                          _format='atom')

searchStr = 'totalResults'
numResultsStr = [ str(i) for i in result.strip().split() if searchStr in i ]
print(numResultsStr)

pprint(u.mine_granules_from_granule_search(granule_search_response=str(result)))
granules = d.mine_drive_urls_from_granule_search(granule_search_response=(str(result)))
pprint(granules)

# download just netcdf files
nc_files = [x for x in granules if '.nc' in x]
d.download_granules(granule_collection=nc_files, path='./csr_grace')

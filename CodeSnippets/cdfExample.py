import cdflib
from astropy.time import Time, TimeDelta

cdf_path = '/home/daraghhollman/Main/DIAS/JUPT/wgetData/repository/juno/waves/data/l3a_v02/data/cdf/2022/01/jno_wav_cdr_lesia_20220101_v02.cdf'

cdf_file = cdflib.CDF(cdf_path)

epoch = cdf_file.varget("Epoch")
unit = cdf_file.varinq("Epoch")["Data_Type_Description"]

time = Time(epoch, format="cdf_tt2000") 

# cdf time 0 = 2000-01-01 in nanoseconds

time.format = "jd"

print(time.isot)

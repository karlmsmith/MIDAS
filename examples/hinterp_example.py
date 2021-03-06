from midas.rectgrid import *
import matplotlib.pyplot as plt
import numpy as np


# Construct a 5 degree lat-lon grid

lon=np.arange(2.5,360.,5.)
lat=np.arange(-77.5,80.,5.)
X,Y=np.meshgrid(lon,lat)
grid=quadmesh(lon=X,lat=Y,cyclic=True)

# Load a single time slice and the first 10 vertical levels of WOA09 data from NODC
fpath='https://opendap.jpl.nasa.gov:443/opendap/OceanTemperature/amsre/L3/sst_1deg_1mo/tos_AMSRE_L3_v7_200206-201012.nc'
S=state(path=fpath,fields=['tos'],time_indices=np.arange(10),default_calendar='julian')
S.volume_integral('tos','XY',normalize=True)
sout=np.squeeze(S.tos[0,0,:])
notes='Original MEAN/MAX/MIN= %(me)4.2f %(mx)4.2f %(mi)4.2f'%{'me':sq(S.tos_xyav[0,0]),'mx':sq(np.max(sout)),'mi':sq(np.min(sout))}

T=S.horiz_interp('tos',target=grid,src_modulo=True,method='bilinear') 
T.volume_integral('tos','XY',normalize=True)

sout=np.squeeze(T.tos[0,0,:])
xax=T.grid.x_T
yax=T.grid.y_T

fig,ax=plt.subplots(1)
cf=ax.contourf(xax,yax,sout,np.arange(273,303),extend='both',cmap=plt.cm.spectral)
plt.colorbar(cf)
ax.grid()
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')


tit='AVHRR regridded'

notes2='Regridded MEAN/MAX/MIN= %(me)4.2f %(mx)4.2f %(mi)4.2f'%{'me':sq(T.tos_xyav[0,0]),'mx':sq(np.max(sout)),'mi':sq(np.min(sout))}

ax.set_title(tit,fontsize=8)

ax.text(0.05,0.95,notes,transform=ax.transAxes,fontsize=6)
ax.text(0.05,0.90,notes2,transform=ax.transAxes,fontsize=6)

plt.show()

import matplotlib.pyplot as _plt
import numpy as _np
#import cartopy.crs as ccrs
from mpl_toolkits.basemap import Basemap

class editmask(object):

	def _on_click(self,event,debug=False):
		if debug:
			print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		    	 (event.button, event.x, event.y, event.xdata, event.ydata))
		x, y = event.xdata, event.ydata
		if event.button==1 and event.inaxes is not None and self._clicking == True:
			itmp = (_np.abs(self._xc - _np.floor(x))).argmin()
			jtmp = (_np.abs(self._yc - _np.floor(y))).argmin()
			dummy, i = _np.unravel_index(itmp,self._xc.shape)
			j, dummy = _np.unravel_index(jtmp,self._yc.shape)
			self.mask[j, i] = 1 - self.mask[j, i]
			self._pc = _plt.pcolormesh(self._xc,self._yc,self.mask,edgecolor='k')
			#self._pc = _plt.imshow(self.mask,origin='lower',extent=(self.lonmin,self.lonmax,self.latmin,self.latmax))
			_plt.draw()

	def _on_key(self, event):
		if event.key == 'e':
			self._clicking = not self._clicking
			_plt.title('Editing %s -- click "e" to toggle' % self._clicking)
			_plt.draw()

	def __init__(self,lon,lat,mask,fig):

		self._xc = lon
		self._yc = lat
		self.mask = mask
		ones = _np.ones(self.mask.shape)
		ones[:] = None
		# dimension of map
		lonmin=self._xc.min()
		lonmax=self._xc.max()
		latmin=self._yc.min()
		latmax=self._yc.max()
		self.lonmin=self._xc.min()
		self.lonmax=self._xc.max()
		self.latmin=self._yc.min()
		self.latmax=self._yc.max()
		padding_x=_np.abs(lonmax-lonmin)/50
		padding_y=_np.abs(latmax-latmin)/50
		lonmin=lonmin-padding_x ; lonmax=lonmax+padding_x
		latmin=latmin-padding_y ; latmax=latmax+padding_y

		print lonmin,lonmax,latmin,latmax
		
		# cartopy
		#self._ax = _plt.axes(projection=ccrs.PlateCarree())
                #self._ax.set_extent([lonmin,lonmax,latmin,latmax])

		self._ax = Basemap(projection='cyl',llcrnrlat=latmin,urcrnrlat=latmax,\
                                         llcrnrlon=lonmin,urcrnrlon=lonmax,resolution='l')

                #self._ax.set_extent([0,90,0,30])
                #self._ax.coastlines(resolution='50m')

                #self._ax.coastlines() # cartopy

                self._ax.drawcoastlines()

		self._pc = _plt.pcolormesh(self._xc,self._yc,self.mask,edgecolor='k')
		#self._pc = _plt.pcolormesh(self._xc,self._yc,ones,edgecolor='k')
		#self._pc = _plt.imshow(self.mask,origin='lower',extent=(self.lonmin,self.lonmax,self.latmin,self.latmax))

		_plt.connect('button_press_event', self._on_click)
		_plt.connect('key_press_event', self._on_key)
		self._clicking = False
		_plt.title('Editing %s -- click "e" to toggle' % self._clicking)
		_plt.show()
		return None
		

lon = _np.arange(-170,-120)
lat = _np.arange(20,60)
lon2d, lat2d = _np.meshgrid(lon,lat)
nx,ny = lon2d.shape
mask = _np.zeros((nx-1,ny-1))

fig = _plt.figure()
editmask(lon2d,lat2d,mask,fig)

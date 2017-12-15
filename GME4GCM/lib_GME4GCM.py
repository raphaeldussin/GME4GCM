import matplotlib.pyplot as _plt
import numpy as _np

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
			self._pc = _plt.pcolor(self._xc,self._yc,self.mask,edgecolor='k')
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
		self._pc = _plt.pcolor(self._xc,self._yc,self.mask,edgecolor='k')

		_plt.connect('button_press_event', self._on_click)
		_plt.connect('key_press_event', self._on_key)
		self._clicking = False
		_plt.title('Editing %s -- click "e" to toggle' % self._clicking)
		_plt.show()
		return None
		

lon = _np.arange(10,20)
lat = _np.arange(20,30)
lon2d, lat2d = _np.meshgrid(lon,lat)
nx,ny = lon2d.shape
mask = _np.zeros((nx-1,ny-1))

fig = _plt.figure()
editmask(lon2d,lat2d,mask,fig)

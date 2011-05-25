from cybercom.data.dataset.ameriflux import ameriflux
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy
from StringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

years = mdates.YearLocator()
months = mdates.MonthLocator()
yearsFmt = mdates.DateFormatter('%Y')

def afplot( location, variable, aggregation='monthly'):
    r = ameriflux.getvar( location, variable, aggregation, as_method='numpy')
    r.sort()
    fname = '%s_%s' % (location, aggregation)
    title = '%s of %s' % (aggregation, variable)
    fileout = date_plot(r, variable, fname, title)
    return fileout

def date_plot(darray, variable, fout, title=None): 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(darray.date, darray[variable])

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    datemin = datetime.date(darray.date.min().year, 1, 1)
    datemax = datetime.date(darray.date.max().year+1, 1, 1)

    ax.set_xlim(datemin, datemax)

    def yfmt(x): return '%1.2f'%x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = yfmt
    ax.grid(True)

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('units')

    fig.autofmt_xdate()
    fileout = StringIO()
    fig.savefig(fileout, format='png') 
    fileout.seek(0)
    return fileout



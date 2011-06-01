from cybercom.data.dataset.ameriflux import ameriflux
import datetime
import getpass 
import os
os.environ['HOME'] = '/var/www/tmp'
import matplotlib
import matplotlib.dates as mdates
import numpy
from StringIO import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from iso8601 import parse_date

def afplot( location, variable, aggregation='monthly', sdate=None, edate=None):
    if sdate and edate:
        sdate,edate = [ parse_date(item) for item in [ sdate, edate ] ]
        r = ameriflux.getvar( location, variable, aggregation, as_method='numpy',
                          date_from=sdate, date_to=edate)
    else:
        r = ameriflux.getvar( location, variable, aggregation, as_method='numpy')

    r.sort()
    fname = '%s_%s' % (location, aggregation)
    title = '%s of %s' % (aggregation, variable)
    return date_plot(r, variable, fname, title)

def date_plot(darray, variable, fout, title=None): 
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')

    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    if len(darray.date) > 1 and len(darray[variable]) > 1:
        ax.scatter(darray.date, darray[variable], alpha=0.5)
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

    else:
        ax.text(0.5, 0.5, 'unplottable data', fontsize=12)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('units')

    fig.autofmt_xdate()
    fileout = StringIO()
    canvas.print_figure(fileout, format='png')
    #fig.savefig(fileout, format='png') 
    fileout.seek(0)
    return fileout



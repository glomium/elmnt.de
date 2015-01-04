#!/usr/bin/python
# ex:set fileencoding=utf-8:

from django.utils.translation import ugettext as _
from django.utils.timezone import now

from celery.task import task
from celery.utils.log import get_task_logger

from datetime import timedelta
import re
import os

# Logger
logger = get_task_logger(__name__)

@task
def redraw_graph(pk):
  """
  """
  from models import Data, Graph

  try:
    graph = Graph.objects.get(pk=pk)
  except Graph.DoesNotExist:
    logger.warning('diet.redraw_graph: graph object (pk=%s) does not exist'%pk)
    return False

  if not os.path.exists( graph.image.path ):
    logger.info('diet.redraw_graph: graph object (pk=%s) has no image'%pk)
    graph.image=''
    graph.save()
    return False

  profile = graph.user

  reg = r'^(overview|stats|([0-9]{4})-(01|02|03|04|05|06|07|08|09|10|11|12))$'
  match = re.match( reg, graph.pretag ).groups()

  if not match:
    logger.warning('diet.redraw_graph: regex does not match image pretag')
    return False

  if match[0] == 'overview':
    end_date = now()
    start_date = (end_date - timedelta(days=400))

    data = Data.objects.filter(user=profile, date__range=(start_date, end_date))

  elif match[0] == 'stats':
    end_date = now()
    start_date = (end_date - timedelta(days=20))

    data = Data.objects.filter(user=profile, date__range=(start_date, end_date))
  else:
    data = Data.objects.filter(user=profile, date__year=match[1], date__month=match[2])

  if len(data) == 0:
    logger.info('diet.redraw_graph: no data selected')
    return False

  bmitarget = float(profile.bmitarget)
  height    = float(profile.height)
    
#   try:
#     bmierror = float(DietData.objects.filter(user=self.user).latest('date').calc_dbmi)
#   except DietData.DoesNotExist:
#     return False, 60

  from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
  from matplotlib.figure import Figure
  from matplotlib.ticker import MultipleLocator
  from matplotlib.dates import MonthLocator, WeekdayLocator, DayLocator, DateFormatter, SU

  fig=Figure()
  ax=fig.add_subplot(111)

  x=[]
  x1=[]
  x2=[]
  y=[]
  cw=[]
  wmin=[]
  wmax=[]
  wavg=[]
  for i in data:
    x.append(i.date)
    y.append(float(i.weight))
    if i.calc_vweight:
      x1.append(i.date)
      cw.append(i.calc_vweight)
    wmin.append(i.min_weight)
    wmax.append(i.max_weight)
    wavg.append(i.max_weight/2 + i.min_weight/2)

  daterange = (max(x)-min(x)).days

  if daterange < 40:
    ax.plot_date(x, y,'bo-', ms=7, lw=0.7, mfc='white')
  else:
    ax.plot_date(x, y,'b-', lw=0.7, alpha=0.5)

  ax.plot_date(x, wmin, 'r-', xdate=True, ydate=False, lw=1.0, alpha=0.85)
  ax.plot_date(x, wmax, 'r-', xdate=True, ydate=False, lw=1.0, alpha=0.85)
  ax.plot_date(x, wavg, 'g-', xdate=True, ydate=False, lw=1.0, alpha=0.85)
    
# if match[0] == 'stats' and q[0].calc_vweight:
#   regx = [ q[0].date, q[len(q)-1].date ]
#   regy = [ q[0].calc_vweight, q[0].calc_vweight + (regx[1]-regx[0]).days*q[0].calc_vslope ]
#   ax.plot_date(regx, regy, 'g--', xdate=True, ydate=False, alpha=0.85, lw=1.2)

  ax.plot_date(x1, cw, '-', xdate=True, ydate=False, color='0.1', lw=1.0)

  # Must stand after plot definitions
# bmiweight = bmitarget*height**2
# ax.axhspan(ymin=bmiweight-bmierror*pow(height,2), ymax=bmiweight+bmierror*pow(height,2), alpha=0.15, facecolor='g')
# ax.axhline(y=bmiweight, color='g', lw=1.0, ls=':')

  if daterange < 5:
    ax.set_xlim(( min(x)-timedelta(days=1), max(x)+timedelta(days=1) ))
  else:
    ax.set_xlim((min(x),max(x)))
  ax.set_ylim(( min(y)-0.5, max(y)+0.5 ))
  ax.yaxis.grid(True, color='0.0',linestyle='-', alpha='0.3')
  ax.xaxis.grid(True, color='0.0',linestyle='-', alpha='0.3')
  ax.set_ylabel(_('Weight (kg)'))

  # Must stand after axis definitions
  if daterange < 10:
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
  elif daterange < 40:
    ax.xaxis.set_major_locator(WeekdayLocator(byweekday=SU))
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))
  else:
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_minor_locator(WeekdayLocator(byweekday=SU))
    ax.xaxis.set_major_formatter(DateFormatter('%m.%y'))

  canvas=FigureCanvas(fig)
  fig.savefig( graph.image.path )

  return True

@task
def data_save(pk):
  """
  """
  from models import Data, Graph, Month

  try:
    data = Data.objects.get(pk=pk)
  except Data.DoesNotExist:
    return False

  profile = data.user

  height = float(profile.height)
  dheight = float(profile.dheight)
  bmitarget = float(profile.bmitarget)

  g_range  = [ float( data.weight ) ]
  c_range  = [] 
  end_date = data.date - timedelta(days=1)

  # get start end end date for min/max values
  start_date = end_date - timedelta(days=61)

  for d in Data.objects.filter(user=profile, date__range=(start_date,end_date)):
    g_range.append( float( d.weight ) )

  start_date = end_date - timedelta(days=21)
  q = Data.objects.filter(user=profile, date__range=(start_date,end_date))

  # do regression
  if len(q) > 1:
    x=[ 0 ]
    y=[ float(data.weight) ]

    for d in q:
      x.append((d.date-data.date).days)
      y.append(float(d.weight))

    # y = a + bx
    sn = 0
    sx = 0
    sy = 0
    sxx = 0
    sxy = 0
    R = 0

    for i in range(len(x)):
      sn += 1
      sx += x[i]
      sy += y[i]
      sxx += x[i]*x[i]
      sxy += x[i]*y[i]

    nenner = sn*sxx-sx*sx
    a = [(sy*sxx-sx*sxy)/nenner, 0]
    b = [(sn*sxy-sx*sy)/nenner,  0]
    for i in range(len(x)):
      R += pow(y[i]-a[0]-b[0]*x[i],2) 
    a[1] = pow(R*sxx/(sn-2)/nenner,0.5)
    b[1] = pow(R*sn/(sn-2)/nenner,0.5)

    c_range.append( a[0] )

    data.calc_vweight = a[0]
    data.calc_dweight = a[1]
    data.calc_vslope  = b[0]
    data.calc_dslope  = b[1]
    data.calc_vbmi    = a[0]/pow(height,2)
    data.calc_dbmi    = pow( pow(a[1]/pow(height,2),2) + pow(a[0]*dheight/pow(height,3),2), 0.5)
  else:
    data.calc_vweight = None
    data.calc_dweight = None
    data.calc_vslope  = None
    data.calc_dslope  = None
    data.calc_vbmi    = float(data.weight)/pow(height,2)
    data.calc_dbmi    = pow( pow(float(data.weight)*dheight/pow(height,3),2), 0.5)

  data.min_weight = min(g_range)
  data.max_weight = max(g_range)

  data.save(update_data=False)

  # update graphs
  for graph in Graph.objects.filter(user=profile, pretag__in=[ 'overview', 'stats', data.date.strftime('%Y-%m') ]):
    graph.redraw()

  # update month
  try:
    month = Month.objects.get(user=profile, date__month=data.date.strftime('%m'), date__year=data.date.strftime('%Y') )
  except Month.DoesNotExist:
    month = Month(user=data.user, date=data.date )
  month.save()

  return True

@task
def month_save(pk):
  """
  """
  from models import Data, Month

  try:
    this_month = Month.objects.get(pk=pk)
  except Month.DoesNotExist:
    return False

  this_data = Data.objects.filter(
    user_id=this_month.user_id,
    date__month=this_month.date.strftime('%m'),
    date__year=this_month.date.strftime('%Y'),
  )

  last_month = this_month.get_previous_month()

  if last_month:
    last_data = Data.objects.filter(
      user_id=this_month.user_id,
      date__month=last_month.date.strftime('%m'),
      date__year=last_month.date.strftime('%Y'),
    )

  return True

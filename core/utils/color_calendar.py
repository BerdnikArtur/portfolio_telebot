import pandas as pd
from cccalendar import draw_colour_calendar
import datetime

async def create_colormap(data, min_date, max_date):
    '''
    creating .png file of color calendar. inside definition of 'draw_colour_calendar'
    there is line 'plt.savefig('/home/pickle_slime/div_of_projects/python_folder/telegram-bot/assets/colormap.png')'
    I know that it's a bad practice to edit code of library but searching new suitable lib take a lot of time 
    ''' 
    dates = {}
    dates1 = {}

    
    for i in data:
        if i[0].strftime('%H:%M:%S') == '11:00:00':
            dates[i[0].strftime('%Y%m%d')] = '11 hour'
        elif i[0].strftime('%H:%M:%S') == '02:00:00':
            dates1[i[0].strftime('%Y%m%d')] = '2 hour'

    s = pd.Series(dates)
    
    if dates1:
        s2 = pd.Series(dates1)
        s = pd.concat([s, s2])

    draw_colour_calendar(s,
                        months_per_row=2,
                        min_date=str(min_date),
                        max_date=str(max_date),
                        date_colour='#606060',
                        legend=False)

    

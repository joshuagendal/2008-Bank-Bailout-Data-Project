
# imported eveyrhting needed to import (class, dataframe, pandas) in console
import importer as imp
df = imp.df
from bailout.models import Bailout, Rating, UserProfile


a = Bailout.objects.all()

for i in a:
    if i.state == 'alabama':
        i.state_ab = 'AL'
        i.save()
    if i.state == 'alaska':
        i.state_ab = 'AK'
        i.save()
    if i.state == 'arizona':
        i.state_ab = 'AZ'
        i.save()
    if i.state == 'arkansas':
        i.state_ab = 'AR'
        i.save()
    if i.state == 'california':
        i.state_ab = 'CA'
        i.save()
    if i.state == 'colorado':
        i.state_ab = 'CO'
        i.save()
    if i.state == 'connecticut':
        i.state_ab = 'CT'
        i.save()
    if i.state == 'delaware':
        i.state_ab = 'DE'
        i.save()
    if i.state == 'florida':
        i.state_ab = 'AK'
        i.save()
    if i.state == 'georgia':
        i.state_ab = 'GA'
        i.save()
    if i.state == 'hawaii':
        i.state_ab = 'HI'
        i.save()
    if i.state == 'idaho':
        i.state_ab = 'ID'
        i.save()
    if i.state == 'illinois':
        i.state_ab = 'IL'
        i.save()
    if i.state == 'indiana':
        i.state_ab = 'IN'
        i.save()
    if i.state == 'iowa':
        i.state_ab = 'IA'
        i.save()
    if i.state == 'kansas':
        i.state_ab = 'KS'
        i.save()
    if i.state == 'kentucky':
        i.state_ab = 'KY'
        i.save()
    if i.state == 'lousiana':
        i.state_ab = 'LA'
        i.save()
    if i.state == 'maine':
        i.state_ab = 'ME'
        i.save()
    if i.state == 'maryland':
        i.state_ab = 'MD'
        i.save()
    if i.state == 'massachusetts':
        i.state_ab = 'MA'
    if i.state == 'michigan':
        i.state_ab = 'MI'
        i.save()
    if i.state == 'minnesota':
        i.state_ab = 'MN'
        i.save()
    if i.state == 'mississippi':
        i.state_ab = 'MS'
        i.save()
    if i.state == 'missouri':
        i.state_ab = 'MO'
        i.save()
    if i.state == 'montana':
        i.state_ab = 'MT'
        i.save()
    if i.state == 'nebraska':
        i.state_ab = 'NE'
        i.save()
    if i.state == 'nevada':
        i.state_ab = 'NV'
        i.save()
    if i.state == 'new hampshire':
        i.state_ab = 'NH'
        i.save()
    if i.state == 'new jersey':
        i.state_ab = 'NJ'
        i.save()
    if i.state == 'new mexico':
        i.state_ab = 'NM'
        i.save()
    if i.state == 'new york':
        i.state_ab = 'NY'
        i.save()
    if i.state == 'north carolina':
        i.state_ab = 'NC'
        i.save()
    if i.state == 'north dakota':
        i.state_ab = 'ND'
        i.save()
    if i.state == 'ohio':
        i.state_ab = 'OH'
        i.save()
    if i.state == 'oklahoma':
        i.state_ab = 'OK'
        i.save()
    if i.state == 'oregon':
        i.state_ab = 'OR'
        i.save()
    if i.state == 'pennsylvania':
        i.state_ab = 'PA'
        i.save()
    if i.state == 'rhode island':
        i.state_ab = 'RI'
        i.save()
    if i.state == 'south carolina':
        i.state_ab = 'SC'
        i.save()
    if i.state == 'south dakota':
        i.state_ab = 'SD'
        i.save()
    if i.state == 'tennessee':
        i.state_ab = 'TN'
        i.save()
    if i.state == 'texas':
        i.state_ab = 'TX'
        i.save()
    if i.state == 'utah':
        i.state_ab = 'UT'
        i.save()
    if i.state == 'vermont':
        i.state_ab = 'VT'
        i.save()
    if i.state == 'virginia':
        i.state_ab = 'VA'
        i.save()
    if i.state == 'washington':
        i.state_ab = 'WA'
        i.save()
    if i.state == 'west virginia':
        i.state_ab = 'WV'
        i.save()
    if i.state == 'wisconsin':
        i.state_ab = 'WI'
        i.save()
    if i.state == 'wyoming':
        i.state_ab = 'WY'
        i.save()




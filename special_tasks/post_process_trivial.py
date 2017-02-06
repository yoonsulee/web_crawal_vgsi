import pandas as pd
from pandasql import sqldf

csvfile = 'RI_SqftVintageInfo_2015DEC.csv'

def fstr(x):
    x_ = x.replace('@',',').replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
    return x_

data = pd.read_csv(csvfile,quotechar='"')
data['physical_address'] = data.apply(lambda row: fstr(row['physical_address']), axis=1)

cmd1 = "SELECT physical_address, year_built, stories_original, stories, living_area_sqrt, gross_area_sqft \
         from data \
         group by physical_address, year_built, stories_original, stories, living_area_sqrt, gross_area_sqft"
data1 = sqldf(cmd1, globals())

cmd2 = "SELECT physical_address, year_built, stories_original, stories, living_area_sqrt, gross_area_sqft \
         from data1 \
         where (stories > 0 and stories not null) or (living_area_sqrt not null) or (gross_area_sqft not null)"
data2 = sqldf(cmd2, globals())
data2.to_csv('upload.csv', index=False)


# Checks
cmd222 = "SELECT m.physical_address, year_built, stories_original, stories, living_area_sqrt, gross_area_sqft \
        from data1 m join \
            (SELECT physical_address \
             from data1 \
             group by physical_address \
             having count(1) > 1) b \
        on m.physical_address=b.physical_address"
data222 = sqldf(cmd2, globals())

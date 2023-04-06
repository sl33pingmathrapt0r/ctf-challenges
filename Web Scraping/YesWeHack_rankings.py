import uses as u
import pandas as pd
from tqdm import tqdm

"""
Having determined that the table is dynamically loaded, 
the webpage must be retrieving the data from some file 
over the network. Looking at the files sent over the 
network when loading the page reveals JSON files. 
Retrieve the JSON files. 
"""

URL_MAIN= 'https://api.yeswehack.com/'
TOP100_URL= URL_MAIN + 'ranking?page={page}'
# PERIODIC_URL= URL_MAIN + 'ranking/{year}/{period}?page='
HUNTER_URL= URL_MAIN + 'hunters/{name}'
HACKTIVE_URL= URL_MAIN + 'hacktivity/{name}?page={page}&resultsPerPage=100'
"SLUG is hunter's url-tag"
printer= lambda a,b: u.printer(a,b)

hunters_top100 =u.hunters_from_cat(TOP100_URL)
# hunters_2023M= [hunters_from_cat(PERIODIC_URL.format(year= 2023, period= 'M'+str(i))) for i in range(1,4)]
# hunters_2022Q= [hunters_from_cat(PERIODIC_URL.format(year= 2022, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2021Q= [hunters_from_cat(PERIODIC_URL.format(year= 2021, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2020Q= [hunters_from_cat(PERIODIC_URL.format(year= 2020, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2019Q= [hunters_from_cat(PERIODIC_URL.format(year= 2019, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2018Q= [hunters_from_cat(PERIODIC_URL.format(year= 2018, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2017Q= [hunters_from_cat(PERIODIC_URL.format(year= 2017, period= 'Q'+str(i))) for i in range(1,4)]
# hunters_2016Q= [hunters_from_cat(PERIODIC_URL.format(year= 2016, period= 'Q'+str(i))) for i in range(2,4)]

"verified that hunters from all periods are in top 100"
# hunters= hunters_top100.username
# for month in hunters_2023M: pd.concat([hunters, month.username], ignore_index=True)
# for quarter in hunters_2022Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2021Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2020Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2019Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2018Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2017Q: pd.concat([hunters, quarter.username], ignore_index=True)
# for quarter in hunters_2016Q: pd.concat([hunters, quarter.username], ignore_index=True)
# hunters= hunters.unique()

printer("Total Profiles Used: ", 100)

# number of private profiles
priv= hunters_top100[hunters_top100.public == False]
printer("Number of Private Profiles: ", priv.shape[0])
printer("Number of Public Profiles:", 100-priv.shape[0])
printer('', 'All further analysis will be done only on public profiles.')

# public
public= hunters_top100[hunters_top100.public == True].drop(columns= ['public'])
public= pd.merge(
    public,
    pd.DataFrame([u.scrape_profile(HUNTER_URL.format(name= slug)) for slug in tqdm(public.slug)]), 
    on= 'name'
    ).set_index('rank')
print()

# profiles with Git
git_df= public[public.github.notnull()]
printer("Number of profiles with GitHub added: ", git_df.shape[0])

# High Impact
impact_rank1= public.loc[1].impact
high_impact= public[public.impact >= impact_rank1].drop(columns= ['slug']).sort_values(by= ['impact'], ascending= False)
printer("Number of profiles with Impact >= Impact of Rank 1st profile: ", high_impact.shape[0])
printer('High Impact Profiles (sorted by Impact): ', high_impact.drop(columns=['github', 'reports']))

# Top 5 analysis
top5public= public[:5]
printer("Top 5 Public Profiles: ", top5public)

print('For each profile in Top 5, Find ')
tasks= ['Number of Hacktivity', 'Top Bug Tag & the Percentage Occurence', 'Top Status & the Percentage Occurence']
[*map(lambda x: print('\t- ' + x), tasks)]

top5_hackStats= [u.hacktivity_stats(HACKTIVE_URL, slug) for slug in tqdm(top5public.slug)]
print()
top5public= pd.merge(
    top5public, 
    pd.DataFrame(top5_hackStats, columns= ['name', 'hacktivity', 'top_bug', '%_bug', 'top_status', '%_status']), 
    on= 'name'
    )

# hactivity stats
printer('Number of Hacktivity', top5public.filter(items= ['name', 'hacktivity']))
# top bug stats
printer('Top Bug stats', top5public.filter(items= ['name', 'top_bug', '%_bug']))
# top status stats
printer('Top Status stats', top5public.filter(['name', 'top_status', '%_status']))
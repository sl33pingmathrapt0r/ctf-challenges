import requests
import pandas as pd

def printer(descriptor_tag: str, desc) -> None: 
    """
    Pretty Printing. 
    """
    if descriptor_tag: print(descriptor_tag)
    print(desc)
    print()
    
    
def hunters_from_cat(url:str) -> pd.DataFrame:
    """
    Obtain hunters from list of hunters. 
    Returns a dataframe. 
    """
    init_page=0 
    r= requests.get(url.format(page= str(init_page)))
    pages= r.json()['pagination']['nb_pages']
    
    hunters=[]
    for page in range(1, pages+1):
        r= requests.get(url.format(page= str(page)))
        for hunter in r.json()['items']: 
            hunters.append(
                    {
                        'rank': hunter['rank'],
                        'name': hunter['username'], 
                        'points': hunter['points'],
                        'public': hunter['hunter_profile']['public'],
                        'slug': hunter['slug']
                    }
                )
    
    return pd.DataFrame(hunters)


def scrape_profile(url:str) -> tuple[int, pd.DataFrame]: 
    """
    Obtain Impact, Number of Reports, GitHub url. 
    """
    r= requests.get(url)
    hunter= r.json()
    return {
        'name': hunter['username'], 
        'reports': hunter['nb_reports'], 
        'impact': hunter['impact'], 
        'github': hunter['hunter_profile']['github']
        }


def scrape_hacktivity(url:str, name: str) -> dict:
    """
    Return a 2-tuple: \n
    1. Total Hacktivity Count \n
    2. DataFrame of all Hactivity with the 
    following attributes:
        - date
        - bug_tag
        - status
    """
    init_page=0 
    r= requests.get(url.format(name= name, page= str(init_page)))
    dic= r.json()
    pages= dic['pagination']['nb_pages']
    hactivity_count= dic['pagination']['nb_results']
    
    activities=[]
    for page in range(1, pages+1):
        r= requests.get(url.format(name= name, page= str(page)))
        for activity in r.json()['items']:
            activities.append(
                {
                    'name': activity['report']['hunter']['username'],
                    'date': activity['date'],
                    'bug_tag': activity['report']['bug_type']['name'],
                    'status': activity['status']['workflow_state']
                }
            )
    
    return hactivity_count, pd.DataFrame(activities)

def find_max(df: pd.DataFrame, cat: str, size: int) -> list:
    """
    Given a Dataframe and a column category, 
    find the frequency of each entry in the 
    category. Size is given to return the freq
    as a percentage. 
    """
    df_freq= df.groupby(cat).count()
    top_freq= df_freq.max().date
    top_cat= df_freq[df_freq.date == top_freq].index[0]
    
    return [top_cat, round(100*top_freq/size,1)]
    

def hacktivity_stats(url: str, name: str) -> list: 
    """
    Summarise Hactivity stats. 
    Return in a list, 
    - name
    - total count of hactivity
    - top bug type and the %-freq of bug
    - top status and %-freq of bug
    """
    count, df= scrape_hacktivity(url, name= name)
    user= df.name[0]
    df.drop(columns= ['name'])
    cats= ['bug_tag', 'status']
    output= [user, count]
    for cat in cats: output+= find_max(df, cat, count)
    
    return output

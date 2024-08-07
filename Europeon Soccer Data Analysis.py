#!/usr/bin/env python
# coding: utf-8

# *Imports*⬇️

# In[1]:


import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# In[2]:


databasePath="E:/sql/database.sqlite"


# In[3]:


connection=sqlite3.connect(databasePath)


# In[4]:


allTable=pd.read_sql("select * from sqlite_master where type='table';",connection)


# In[5]:


allTable


# *List All the Countries*⬇️

# In[6]:


allCountries=pd.read_sql("select * from country",connection)


# In[7]:


allCountries


# *List All The Leagues Along With Country*⬇️

# In[8]:


allLeagues=pd.read_sql('select lg.id, lg.name league , lg.country_id,ct.name as country  from league lg join country ct on ct.id=lg.country_id',connection)


# In[9]:


allLeagues


# *List Top 10 Teams Ordered By Team long Name*⬇️

# In[10]:


topTeams=pd.read_sql("select * from team order by team_long_name limit 10",connection)


# In[11]:


topTeams


# *List Details of Top 5 Matches Played in Year 2015 Having Highest Goals *⬇️

# In[12]:


matchDetails=pd.read_sql("select ma.id,ma.match_api_id match_id,lg.name league,ma.season,t1.team_short_name  home_team, t2.team_short_name away_team, ma.home_team_goal, ma.away_team_goal from match ma left join league lg on ma.league_id= lg.id left join team t1 on t1.team_api_id=ma.home_team_api_id left join team t2 on t2.team_api_id= ma.away_team_api_id  where date>='2015-01-01' and date<= '2015-12-31' order by (home_team_goal+away_team_goal) desc limit 5 ",connection)


# In[13]:


matchDetails


#  *Aggregate Performance of a country in each league*⬇️

# In[14]:


countryPerformance=pd.read_sql("""SELECT Country.name AS country_name, 
                                        League.name AS league_name, 
                                        season,
                                        count(distinct stage) AS number_of_stages,
                                        count(distinct HT.team_long_name) AS number_of_teams,
                                        avg(home_team_goal) AS avg_home_team_goals, 
                                        avg(away_team_goal) AS avg_away_team_goals, 
                                        avg(home_team_goal-away_team_goal) AS avg_goal_dif, 
                                        avg(home_team_goal+away_team_goal) AS avg_goals, 
                                        sum(home_team_goal+away_team_goal) AS total_goals                                       
                                FROM Match
                                JOIN Country on Country.id = Match.country_id
                                JOIN League on League.id = Match.league_id
                                LEFT JOIN Team AS HT on HT.team_api_id = Match.home_team_api_id
                                LEFT JOIN Team AS AT on AT.team_api_id = Match.away_team_api_id
                                GROUP BY Country.name, League.name,season
                                ORDER BY Country.name, League.name, season DESC
                                ;""",connection)


# In[15]:


countryPerformance


# In[16]:


def plot_metrics(country, league, df):
    subset = df[(df['country_name'] == country) & (df['league_name'] == league)]
    
    fig, axs = plt.subplots(4, 1, figsize=(10, 20), sharex=True)
    
    axs[0].plot(subset['season'], subset['avg_home_team_goals'], marker='o')
    axs[0].set_title(f'Average Home Team Goals - {league}')
    axs[0].set_ylabel('Avg Home Team Goals')
    
    axs[1].plot(subset['season'], subset['avg_away_team_goals'], marker='o', color='orange')
    axs[1].set_title(f'Average Away Team Goals - {league}')
    axs[1].set_ylabel('Avg Away Team Goals')
    
    axs[2].plot(subset['season'], subset['avg_goal_dif'], marker='o', color='green')
    axs[2].set_title(f'Average Goal Difference - {league}')
    axs[2].set_ylabel('Avg Goal Difference')
    
    axs[3].plot(subset['season'], subset['total_goals'], marker='o', color='red')
    axs[3].set_title(f'Total Goals - {league}')
    axs[3].set_ylabel('Total Goals')
    axs[3].set_xlabel('Season')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# In[17]:


plot_metrics('Belgium', 'Belgium Jupiler League', countryPerformance)


# In[ ]:





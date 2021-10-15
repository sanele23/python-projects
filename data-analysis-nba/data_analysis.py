"""
import pandas -> library used for data manipulation
import seaborn as sns -> used for  graphing or plotting
import matplotlib -> used for any low level methods
import os -> used to change the directory to the right place
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Read data from csv file
players = pd.read_csv("nba_data/basketball_players.csv")
# Show data inside the csv file

# print(players.columns)

"""
Get the min, max, mean & median of the Rebound column

min = players["rebounds"].min()
max = players["rebounds"].max()
mean = players["rebounds"].mean()
median = players["rebounds"].median()

print("Rebounds per season: Min:{}, Max:{}, Mean:{:.2f}, Median:{}".format(min, max, mean, median))
"""
# *************************************************************** #
"""
- Check the top 10 highest rebounding seasons
- The output will include the player and the team they played for

print(players[["playerID", "year", "tmID", "rebounds"]].sort_values("rebounds", ascending=False).head(10))
"""

# ****************************** MERGING SEPARATE DATASETS ********************************* #
"""
Merging two datasets using left join
"""
# The "master" data (basketball_master.csv) has names, biographical information, etc.
master = pd.read_csv("nba_data/basketball_master.csv")

# Do a left join to merge the two datasets (basketball_players/master)
nba = pd.merge(players, master, how="left", left_on="playerID", right_on="bioID")

# print(nba[["year", "useFirst", "lastName", "tmID", "rebounds"]].sort_values("rebounds", ascending=False).head(10))

# ******************************* CREATE A NEW COLUMN ******************************** #
"""
- Create a new column that will show the number of rebounds per game
- We'll use the 'rebound' & 'GP' to put information for our new column
"""
# Remove any rows with GP = 0
nba = nba[nba.GP > 0]
nba["reboundsPerGame"] = nba["rebounds"] / nba["GP"]
print(nba[["year", "useFirst", "lastName", "rebounds", "GP", "reboundsPerGame"]].sort_values("reboundsPerGame", ascending=False).head(10))

# ******************************* PLOTTING WITH SEABORN ******************************** #
"""
We'll use the seaborn library for plotting

# 1 - plot for a single column
# sns.boxplot(data=nba.reboundsPerGame)

# 2 - plot for multiple columns
sns.boxplot(data=nba[["rebounds", "oRebounds", "dRebounds"]])
#
# Show the current plot
plt.show()
# Saves the current plot to a file
plt.savefig("boxplot_reboundsPerGame.png")

"""

# ******************************* REBOUNDS OVER TIME - FACETGRID ******************************** #
"""
Check if the rebounding trends have changed over time

# Get a subset of the data where the year is between 1980 and 1990
eighties = nba[(nba.year >= 1980) & (nba.year < 1990)]

sns.boxplot(eighties["reboundsPerGame"], orient="v")

# Set up FaceGrid and map this function for each facet
grid = sns.FacetGrid(eighties, col="year")
grid = map(sns.boxplot, "reboundsPerGame", orient="v")

"""

# ******************************* REBOUNDS OVER TIME - GROUPING BY YEAR ******************************** #
"""
Grouping statistics by year for rebounds per game.
#
nba_grouped_year = nba[["reboundsPerGame", "year"]].groupby("year").median()
print(nba_grouped_year)

# plot the data
nba_grouped_year = nba[["reboundsPerGame", "year"]].groupby("year").max()
nba_grouped_year = nba_grouped_year.reset_index()
# sns.regplot(data=nba_grouped_year, x="year", y="reboundsPerGame")

# -- Remove any years where the rebound was 0 -- #
nba_grouped_year = nba_grouped_year[nba_grouped_year["reboundsPerGame"] > 0]
# sns.regplot(data=nba_grouped_year, x="year", y="reboundsPerGame").set_title("Median rebounds per Year")
sns.regplot(data=nba_grouped_year, x="year", y="reboundsPerGame").set_title("Max rebounds per Year")

# Show the current plot
plt.show()

# Saves the current plot to a file
plt.savefig("boxplot_reboundsPerGame.png")
"""
# ******************************* REBOUNDS PER YEAR - GROUPING BY YEAR ******************************** #
"""
check the top 10 rebounders per year and their median.
"""
# Get the top 10 rebounders per year
nba_topRebounders_perYear = nba[["reboundsPerGame", "year"]].groupby("year")["reboundsPerGame"].nlargest(10)

# Get the median of these 10
nba_topRebounders_median_perYear = nba_topRebounders_perYear.groupby("year").median()

# Put year back in as year column
nba_topRebounders_median_perYear = nba_topRebounders_median_perYear.reset_index()

# No zeros
nba_topRebounders_median_perYear_noZeros = nba_topRebounders_median_perYear[nba_topRebounders_median_perYear["reboundsPerGame"] > 0]

# Show plot
sns.regplot(data=nba_topRebounders_median_perYear_noZeros, x="year", y="reboundsPerGame").set_title("Median of Top 10 Rebounders Each Year")

# Show the current plot
plt.show()

# Saves the current plot to a file
plt.savefig("boxplot_reboundsPerGame.png")





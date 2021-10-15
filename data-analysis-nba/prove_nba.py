"""
This is the week 13 data analysis project.
NOTE: nba = data contained within the csv files. This data will be used throughout our code.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

"""
Retrieve all the required csv files for the data analysis:
+ Basketball players csv file
+ Basketball master csv file
"""

# Read the players csv file
players = pd.read_csv("nba_data/basketball_players.csv")

# Read the master csv file
master = pd.read_csv("nba_data/basketball_master.csv")

# Do a left join to merge the two datasets (basketball_players/master)
nba = pd.merge(players, master, how="left", left_on="playerID", right_on="bioID")

"""
* Calculate the mean and the median number of points scored
* Find the highest number of points recorded in a single season
* Produce a boxplot that shows the distribution of total points,
  total assists, and total rebounds
* Produce a plot that shows how the number of points scored has
  changed over time
"""
# Find the mean of the points
mean_points = nba.points.mean()

# Find the median of the points
median_points = nba.points.median()

# Print the mean and median values found from the gathered data
print("The mean and median each player scores per season:\nMean: {:.2f}\nMedian: {}".format(mean_points, median_points))
print()
# Highest number of points recorded in a single season
max_points = nba.points.max()
print("The highest number of points in a single season:\nHighest Points: {}".format(max_points))
print()

# Get the year and player's info with the highest number of points
max_points_year = nba[nba.points == max_points][["points", "year", "firstName", "lastName", "nameSuffix"]]
print("The year with the highest number of points:\n{}".format(max_points_year))

# Produce a boxplot that shows the distribution of total points,
# total assists, and total rebounds
nba["total_points"] = nba.points + nba.PostPoints
nba["total_assists"] = nba.assists + nba.PostAssists
nba["total_rebounds"] = nba.rebounds + nba.PostRebounds

nba[["total_points", "total_assists", "total_rebounds"]].plot(kind="box")

# Show plot
plt.show()

# Plot to show how the number of points have changed over time
year_points = nba[["year", "points"]].groupby("year").median()
year_points.plot(kind="line")

# Show plot
plt.show()

"""
Stats for players shots attempted:
* Points per attempt
* Stats on players excelling across many categories
* Popularity in three-points shots
"""

# Points per attempt
nba["PointsPerAttempt"] = nba.points / (nba.fgAttempted + nba.ftAttempted)

points_attempted = nba[["playerID", "PointsPerAttempt"]].groupby("playerID").mean()
points_attempted = points_attempted[points_attempted.PointsPerAttempt != np.inf]
print(points_attempted)

top10_points_player = points_attempted.nlargest(10, "PointsPerAttempt")["PointsPerAttempt"]
print(top10_points_player)

# Merge
pd.merge(top10_points_player, master, how="left", left_on="playerID", right_on="bioID")[["firstName", "lastName", "nameSuffix", "PointsPerAttempt"]]

# Exceptional players in many categories
stats_category = ["points", "rebounds", "assists", "steals", "blocks", "turnovers"]
exceptional_player = nba[stats_category + ["playerID"]].groupby("playerID").mean().nlargest(10, stats_category)

# Check through stats
for i in stats_category:
    exceptional_player[i + "Rank"] = exceptional_player[i].rank(ascending=True, pct=True)

print(exceptional_player[exceptional_player.columns[-6:]])

pd.merge(exceptional_player[exceptional_player.columns[-6:]], master, how="left", left_on="playerID", right_on="bioID")[["firstName", "lastName", "nameSuffix"]]

exceptional_player[exceptional_player.columns[-6:]].plot(kind="bar")
plt.show()

# Popularity in three-points shots
nba["total_threeAttempted"] = nba.threeAttempted + nba.PostthreeAttempted
nba["total_threeMade"] = nba.threeMade + nba.PostthreeMade

three_data_per_year = nba.groupby(["lgID", "year"]).mean().reset_index()[["lgID", "year", "total_threeAttempted", "total_threeMade"]]
three_data_per_year = three_data_per_year[(three_data_per_year.total_threeAttempted > 0) & (three_data_per_year.total_threeMade > 0)]
three_data_per_year = three_data_per_year.melt(["lgID", "year"])

print(three_data_per_year)

grid = sns.FacetGrid(three_data_per_year, col="lgID", hue="variable")

grid.map(sns.lineplot, "year", "value").add_legend()

plt.show()



plot = sns.lineplot(x="year", y="total_threeAttempted", data=nba)
plot2 = sns.lineplot(x="year", y="total_threeMade", data=nba)

# Display plots/graphs
plt.legend(['threeAttempted', 'threeMade'])
plt.show()

"""
Provide stats that will prove who is the G.O.A.T. (Greatest Of All Time):
* Evidence of who is the GOAT
* Biographical stats 
* Any other interesting stats about the players
"""

# Who is the Greatest Of All Time
stats = ["points", "rebounds", "assists", "steals", "blocks", "turnovers"]
player_stats = nba[["playerID"] + stats].groupby("playerID").mean()

# Find stats for players and print out their stats
for i in stats:
    player_stats[i + "Rank"] = player_stats[i].rank(ascending=True, pct=True)

print(player_stats)

# Player ranking
player_stat_rank = player_stats.iloc[:, [x for x in range(6, 12)]]
player_stat_rank_goat = player_stat_rank * [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
player_stat_rank_goat["GOAT_score"] = player_stat_rank_goat.sum(axis=1)
top_10_goat = player_stat_rank_goat.nlargest(10, "GOAT_score")

# Print player ranking
print(player_stat_rank)
top_10_goat = pd.merge(top_10_goat["GOAT_score"], master, how="inner", left_on="playerID", right_on="bioID")[
    ["firstName", "middleName", "lastName", "nameSuffix", "GOAT_score"]]

# Print out the top 10
print(top_10_goat)
sns.barplot(x="firstName", y="GOAT_score", data=top_10_goat)

# Show graphs/stats
plt.ylim(0.9, 1)
plt.show()

# Find anything interesting about players who came from a similar location
print(master.columns)

location_group_height = master.groupby(["birthState"]).mean()["height"].sort_values(ascending=False).nlargest(10)
location_group_weight = master.groupby(["birthState"]).mean()["weight"].sort_values(ascending=False).nlargest(10)
print(location_group_height)
print(location_group_weight)

# Show plot
location_group_height.plot(kind='barh', x="birthState", y="height")
plt.show()

# Show plot
location_group_weight.plot(kind='barh', x="birthState", y="weight")
plt.show()

# Any other interesting stats about the GOAT

# The relationship between weight and height per position
data_r = nba[["pos", "height", "weight"]].replace([np.inf, -np.inf], np.nan).dropna()

grid = sns.FacetGrid(data_r[data_r.height > 0][data_r.weight > 0], col="pos")
grid.map(sns.scatterplot, "height", "weight").add_legend()

# Show graph
plt.show()

# Changes over years per position
data_r2 = nba[["pos", "year", "height", "weight"]].replace([np.inf, -np.inf], np.nan).dropna()[nba.height > 0][nba.weight > 0]

# Show plot
sns.lineplot(x="year", y="height", data=data_r2, hue="pos")
plt.show()

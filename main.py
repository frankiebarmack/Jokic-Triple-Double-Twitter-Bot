# -*- coding: utf-8 -*-
"""Copy of main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eGJFGSzYEbnOoImRhmioUIA_WRo5HlAi
"""

from bs4 import BeautifulSoup
import requests

def find_latest_game_with_result():
    url = "https://www.basketball-reference.com/teams/DEN/2024_games.html"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table containing the game data
            table = soup.find('table', {'id': 'games'})

            # Check if the table is found
            if table:
                # Find all rows in the table
                rows = table.find_all('tr')

                # Initialize variables to store the latest game result, box score URL, date, and opponent
                latest_game_result = None
                latest_box_score_url = None
                latest_game_date = None
                latest_game_opponent = None

                # Iterate over each row and extract the necessary information of the latest game with a result
                for row in reversed(rows):
                    game_result_element = row.find('td', {'data-stat': 'game_result'})
                    if game_result_element and game_result_element.text.strip() in ['W', 'L']:
                        # Extract the game result
                        latest_game_result = game_result_element.text.strip()

                        # Extract the box score URL
                        box_score_element = row.find('td', {'data-stat': 'box_score_text'})
                        if box_score_element and box_score_element.find('a'):
                            latest_box_score_url = f"https://www.basketball-reference.com{box_score_element.find('a')['href']}"

                        # Extract the game date
                        game_date_element = row.find('td', {'data-stat': 'date_game'})
                        if game_date_element:
                            latest_game_date = game_date_element.text.strip()

                        # Extract the opponent's name
                        opponent_element = row.find('td', {'data-stat': 'opp_name'})
                        if opponent_element:
                            latest_game_opponent = opponent_element.text.strip()

                        # Break the loop as we found the latest game with a result
                        break

                return latest_game_date, latest_game_opponent, latest_game_result, latest_box_score_url
            else:
                print("Table not found.")
                return None
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Call the function and save our variables
game_date, game_opponent, game_result, box_score_url = find_latest_game_with_result()

def find_jokic_stats(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Directly find the row with Jokic's ID
            jokic_row = soup.find('th', {'data-append-csv': 'jokicni01'})

            if jokic_row:
                # Get the parent row of this cell
                row = jokic_row.find_parent('tr')
                if row:
                    # Extract stats from Jokic's row
                    stats = row.find_all('td', {'data-stat': True})
                    stat_names = ['mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct',
                                  'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl',
                                  'blk', 'tov', 'pf', 'pts', 'plus_minus']
                    jokic_stats = {name: stat.text.strip() for name, stat in zip(stat_names, stats)}
                    return jokic_stats
                else:
                    print("Row for Jokic not found")
            else:
                print("Jokic ID not found")

            return "Jokic's stats not found on the page."
        else:
            return f"Failed to retrieve page. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# Save Jokic's stats to jokic_stats
jokic_stats = find_jokic_stats(box_score_url)
print(jokic_stats)

points = int(jokic_stats.get('pts', 'Not available'))
assists = int(jokic_stats.get('ast', 'Not available'))
rebounds = int(jokic_stats.get('trb', 'Not available'))
steals = int(jokic_stats.get('stl', 'Not available'))
blocks = int(jokic_stats.get('blk', 'Not available'))


stats = [points, rebounds, assists, steals, blocks]

def check_tdbl(stats):
    double_digits = 0
    for stat in stats:
        if stat >= 10:
            double_digits += 1
    return double_digits >= 3


triple_double = check_tdbl(stats)
if triple_double:
  trip_dub_text = "YES"
else:
  trip_dub_text="NO"

import tweepy
client = tweepy.Client(consumer_key="",
                    consumer_secret="",
                    access_token="",
                    access_token_secret="")

text = (
    f"{trip_dub_text}\n"
    f"{game_date}\n"
    f"vs. {game_opponent}\n"
    f"Points: {points}\n"
    f"Rebounds: {rebounds}\n"
    f"Assists: {assists}\n"
    f"Steals: {steals}\n"
    f"Blocks: {blocks}"
)

response = client.create_tweet(text=text)

def main_function(request):
    # Initialize the Tweepy client
    client = tweepy.Client(consumer_key="",
                           consumer_secret="",
                           access_token="",
                           access_token_secret="")

    # Call the function to find the latest game
    game_date, game_opponent, game_result, box_score_url = find_latest_game_with_result()

    if box_score_url:
        jokic_stats = find_jokic_stats(box_score_url)

        if jokic_stats:
            points = int(jokic_stats.get('pts', 0))
            assists = int(jokic_stats.get('ast', 0))
            rebounds = int(jokic_stats.get('trb', 0))
            steals = int(jokic_stats.get('stl', 0))
            blocks = int(jokic_stats.get('blk', 0))

            stats = [points, rebounds, assists, steals, blocks]
            triple_double = check_tdbl(stats)

            trip_dub_text = "YES" if triple_double else "NO"

            text = (
                f"{trip_dub_text}\n"
                f"{game_date}\n"
                f"vs. {game_opponent}\n"
                f"Points: {points}\n"
                f"Rebounds: {rebounds}\n"
                f"Assists: {assists}\n"
                f"Steals: {steals}\n"
                f"Blocks: {blocks}"
            )

            response = client.create_tweet(text=text)

            return 'Tweet sent successfully'
        else:
            return 'Jokic stats not found'
    else:
        return 'Latest game not found'

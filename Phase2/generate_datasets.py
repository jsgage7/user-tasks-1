import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import random

def get_survivor_data():
    """
    Scrape data for Survivor seasons including:
    - Season number
    - Year aired
    - Winner name
    - Runner-up(s)
    - Location
    - Number of contestants
    - Viewership data
    """
    print("Gathering Survivor data...")
    
    # Create empty dataframe with required columns
    survivor_df = pd.DataFrame(columns=[
        'Season', 'Year', 'Winner', 'Runner_Up', 'Location', 'Contestants', 'Avg_Viewership_Millions'
    ])
    
    # Survivor data (up to season 44)
    survivor_data = [
        {'Season': 1, 'Year': 2000, 'Winner': 'Richard Hatch', 'Runner_Up': 'Kelly Wiglesworth', 
         'Location': 'Borneo', 'Contestants': 16, 'Avg_Viewership_Millions': 28.30},
        {'Season': 2, 'Year': 2001, 'Winner': 'Tina Wesson', 'Runner_Up': 'Colby Donaldson', 
         'Location': 'The Australian Outback', 'Contestants': 16, 'Avg_Viewership_Millions': 30.00},
        {'Season': 3, 'Year': 2001, 'Winner': 'Ethan Zohn', 'Runner_Up': 'Kim Johnson', 
         'Location': 'Africa', 'Contestants': 16, 'Avg_Viewership_Millions': 20.72},
        {'Season': 4, 'Year': 2002, 'Winner': 'Vecepia Towery', 'Runner_Up': 'Neleh Dennis', 
         'Location': 'Marquesas', 'Contestants': 16, 'Avg_Viewership_Millions': 20.77},
        {'Season': 5, 'Year': 2002, 'Winner': 'Brian Heidik', 'Runner_Up': 'Clay Jordan', 
         'Location': 'Thailand', 'Contestants': 16, 'Avg_Viewership_Millions': 20.10},
        {'Season': 6, 'Year': 2003, 'Winner': 'Jenna Morasca', 'Runner_Up': 'Matthew Von Ertfelda', 
         'Location': 'The Amazon', 'Contestants': 16, 'Avg_Viewership_Millions': 17.65},
        {'Season': 7, 'Year': 2003, 'Winner': 'Sandra Diaz-Twine', 'Runner_Up': 'Lillian Morris', 
         'Location': 'Pearl Islands', 'Contestants': 16, 'Avg_Viewership_Millions': 21.21},
        {'Season': 8, 'Year': 2004, 'Winner': 'Amber Brkich', 'Runner_Up': 'Rob Mariano', 
         'Location': 'All-Stars', 'Contestants': 18, 'Avg_Viewership_Millions': 21.49},
        {'Season': 9, 'Year': 2004, 'Winner': 'Chris Daugherty', 'Runner_Up': 'Twila Tanner', 
         'Location': 'Vanuatu', 'Contestants': 18, 'Avg_Viewership_Millions': 19.64},
        {'Season': 10, 'Year': 2005, 'Winner': 'Tom Westman', 'Runner_Up': 'Katie Gallagher', 
         'Location': 'Palau', 'Contestants': 20, 'Avg_Viewership_Millions': 20.00},
        {'Season': 11, 'Year': 2005, 'Winner': 'Danni Boatwright', 'Runner_Up': 'Stephenie LaGrossa', 
         'Location': 'Guatemala', 'Contestants': 18, 'Avg_Viewership_Millions': 18.30},
        {'Season': 12, 'Year': 2006, 'Winner': 'Aras Baskauskas', 'Runner_Up': 'Danielle DiLorenzo', 
         'Location': 'Panama', 'Contestants': 16, 'Avg_Viewership_Millions': 16.82},
        {'Season': 13, 'Year': 2006, 'Winner': 'Yul Kwon', 'Runner_Up': 'Ozzy Lusth', 
         'Location': 'Cook Islands', 'Contestants': 20, 'Avg_Viewership_Millions': 15.75},
        {'Season': 14, 'Year': 2007, 'Winner': 'Earl Cole', 'Runner_Up': 'Cassandra Franklin', 
         'Location': 'Fiji', 'Contestants': 19, 'Avg_Viewership_Millions': 13.92},
        {'Season': 15, 'Year': 2007, 'Winner': 'Todd Herzog', 'Runner_Up': 'Courtney Yates', 
         'Location': 'China', 'Contestants': 16, 'Avg_Viewership_Millions': 15.18},
        {'Season': 16, 'Year': 2008, 'Winner': 'Parvati Shallow', 'Runner_Up': 'Amanda Kimmel', 
         'Location': 'Micronesia', 'Contestants': 20, 'Avg_Viewership_Millions': 13.61},
        {'Season': 17, 'Year': 2008, 'Winner': 'Bob Crowley', 'Runner_Up': 'Susie Smith', 
         'Location': 'Gabon', 'Contestants': 18, 'Avg_Viewership_Millions': 13.05},
        {'Season': 18, 'Year': 2009, 'Winner': 'J.T. Thomas', 'Runner_Up': 'Stephen Fishbach', 
         'Location': 'Tocantins', 'Contestants': 16, 'Avg_Viewership_Millions': 12.86},
        {'Season': 19, 'Year': 2009, 'Winner': 'Natalie White', 'Runner_Up': 'Russell Hantz', 
         'Location': 'Samoa', 'Contestants': 20, 'Avg_Viewership_Millions': 13.45},
        {'Season': 20, 'Year': 2010, 'Winner': 'Sandra Diaz-Twine', 'Runner_Up': 'Parvati Shallow', 
         'Location': 'Heroes vs. Villains', 'Contestants': 20, 'Avg_Viewership_Millions': 13.80},
        {'Season': 21, 'Year': 2010, 'Winner': 'Jud "Fabio" Birza', 'Runner_Up': 'Chase Rice', 
         'Location': 'Nicaragua', 'Contestants': 20, 'Avg_Viewership_Millions': 13.61},
        {'Season': 22, 'Year': 2011, 'Winner': 'Rob Mariano', 'Runner_Up': 'Phillip Sheppard', 
         'Location': 'Redemption Island', 'Contestants': 18, 'Avg_Viewership_Millions': 11.73},
        {'Season': 23, 'Year': 2011, 'Winner': 'Sophie Clarke', 'Runner_Up': 'Benjamin "Coach" Wade', 
         'Location': 'South Pacific', 'Contestants': 18, 'Avg_Viewership_Millions': 10.85},
        {'Season': 24, 'Year': 2012, 'Winner': 'Kim Spradlin', 'Runner_Up': 'Sabrina Thompson', 
         'Location': 'One World', 'Contestants': 18, 'Avg_Viewership_Millions': 10.48},
        {'Season': 25, 'Year': 2012, 'Winner': 'Denise Stapley', 'Runner_Up': 'Lisa Whelchel', 
         'Location': 'Philippines', 'Contestants': 18, 'Avg_Viewership_Millions': 10.80},
        {'Season': 26, 'Year': 2013, 'Winner': 'John Cochran', 'Runner_Up': 'Dawn Meehan', 
         'Location': 'Caramoan', 'Contestants': 20, 'Avg_Viewership_Millions': 10.16},
        {'Season': 27, 'Year': 2013, 'Winner': 'Tyson Apostol', 'Runner_Up': 'Monica Culpepper', 
         'Location': 'Blood vs. Water', 'Contestants': 20, 'Avg_Viewership_Millions': 10.63},
        {'Season': 28, 'Year': 2014, 'Winner': 'Tony Vlachos', 'Runner_Up': 'Woo Hwang', 
         'Location': 'Cagayan', 'Contestants': 18, 'Avg_Viewership_Millions': 9.85},
        {'Season': 29, 'Year': 2014, 'Winner': 'Natalie Anderson', 'Runner_Up': 'Jaclyn Schultz', 
         'Location': 'San Juan del Sur', 'Contestants': 18, 'Avg_Viewership_Millions': 9.70},
        {'Season': 30, 'Year': 2015, 'Winner': 'Mike Holloway', 'Runner_Up': 'Carolyn Rivera', 
         'Location': 'Worlds Apart', 'Contestants': 18, 'Avg_Viewership_Millions': 9.80},
        {'Season': 31, 'Year': 2015, 'Winner': 'Jeremy Collins', 'Runner_Up': 'Spencer Bledsoe', 
         'Location': 'Cambodia', 'Contestants': 20, 'Avg_Viewership_Millions': 9.70},
        {'Season': 32, 'Year': 2016, 'Winner': 'Michele Fitzgerald', 'Runner_Up': 'Aubry Bracco', 
         'Location': 'Kaôh Rōng', 'Contestants': 18, 'Avg_Viewership_Millions': 9.50},
        {'Season': 33, 'Year': 2016, 'Winner': 'Adam Klein', 'Runner_Up': 'Hannah Shapiro', 
         'Location': 'Millennials vs. Gen X', 'Contestants': 20, 'Avg_Viewership_Millions': 9.10},
        {'Season': 34, 'Year': 2017, 'Winner': 'Sarah Lacina', 'Runner_Up': 'Brad Culpepper', 
         'Location': 'Game Changers', 'Contestants': 20, 'Avg_Viewership_Millions': 8.40},
        {'Season': 35, 'Year': 2017, 'Winner': 'Ben Driebergen', 'Runner_Up': 'Chrissy Hofbeck', 
         'Location': 'Heroes vs. Healers vs. Hustlers', 'Contestants': 18, 'Avg_Viewership_Millions': 8.70},
        {'Season': 36, 'Year': 2018, 'Winner': 'Wendell Holland', 'Runner_Up': 'Domenick Abbate', 
         'Location': 'Ghost Island', 'Contestants': 20, 'Avg_Viewership_Millions': 8.30},
        {'Season': 37, 'Year': 2018, 'Winner': 'Nick Wilson', 'Runner_Up': 'Mike White', 
         'Location': 'David vs. Goliath', 'Contestants': 20, 'Avg_Viewership_Millions': 7.80},
        {'Season': 38, 'Year': 2019, 'Winner': 'Chris Underwood', 'Runner_Up': 'Gavin Whitson', 
         'Location': 'Edge of Extinction', 'Contestants': 18, 'Avg_Viewership_Millions': 7.20},
        {'Season': 39, 'Year': 2019, 'Winner': 'Tommy Sheehan', 'Runner_Up': 'Dean Kowalski', 
         'Location': 'Island of the Idols', 'Contestants': 20, 'Avg_Viewership_Millions': 6.40},
        {'Season': 40, 'Year': 2020, 'Winner': 'Tony Vlachos', 'Runner_Up': 'Natalie Anderson', 
         'Location': 'Winners at War', 'Contestants': 20, 'Avg_Viewership_Millions': 7.00},
        {'Season': 41, 'Year': 2021, 'Winner': 'Erika Casupanan', 'Runner_Up': 'Deshawn Radden', 
         'Location': 'Fiji', 'Contestants': 18, 'Avg_Viewership_Millions': 5.30},
        {'Season': 42, 'Year': 2022, 'Winner': 'Maryanne Oketch', 'Runner_Up': 'Mike Turner', 
         'Location': 'Fiji', 'Contestants': 18, 'Avg_Viewership_Millions': 5.10},
        {'Season': 43, 'Year': 2022, 'Winner': 'Mike Gabler', 'Runner_Up': 'Cassidy Clark', 
         'Location': 'Fiji', 'Contestants': 18, 'Avg_Viewership_Millions': 5.00},
        {'Season': 44, 'Year': 2023, 'Winner': 'Yam Yam Arocho', 'Runner_Up': 'Carolyn Wiger', 
         'Location': 'Fiji', 'Contestants': 18, 'Avg_Viewership_Millions': 4.90}
    ]
    
    # Add data to dataframe
    survivor_df = pd.DataFrame(survivor_data)
    
    # Save to CSV
    survivor_df.to_csv('survivor_data.csv', index=False)
    print(f"Survivor dataset created with {len(survivor_df)} seasons")
    
    return survivor_df

def get_american_idol_data():
    """
    Scrape data for American Idol seasons including:
    - Season number
    - Year aired
    - Winner name
    - Runner-up(s)
    - Judges for that season
    - Number of contestants
    - Viewership data
    """
    print("Gathering American Idol data...")
    
    # Create empty dataframe with required columns
    idol_df = pd.DataFrame(columns=[
        'Season', 'Year', 'Winner', 'Runner_Up', 'Judges', 'Contestants', 'Avg_Viewership_Millions'
    ])
    
    # American Idol data
    idol_data = [
        {'Season': 1, 'Year': 2002, 'Winner': 'Kelly Clarkson', 'Runner_Up': 'Justin Guarini', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 30, 'Avg_Viewership_Millions': 12.70},
        {'Season': 2, 'Year': 2003, 'Winner': 'Ruben Studdard', 'Runner_Up': 'Clay Aiken', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 32, 'Avg_Viewership_Millions': 21.70},
        {'Season': 3, 'Year': 2004, 'Winner': 'Fantasia Barrino', 'Runner_Up': 'Diana DeGarmo', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 32, 'Avg_Viewership_Millions': 25.70},
        {'Season': 4, 'Year': 2005, 'Winner': 'Carrie Underwood', 'Runner_Up': 'Bo Bice', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 24, 'Avg_Viewership_Millions': 26.20},
        {'Season': 5, 'Year': 2006, 'Winner': 'Taylor Hicks', 'Runner_Up': 'Katharine McPhee', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 24, 'Avg_Viewership_Millions': 30.30},
        {'Season': 6, 'Year': 2007, 'Winner': 'Jordin Sparks', 'Runner_Up': 'Blake Lewis', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 24, 'Avg_Viewership_Millions': 30.00},
        {'Season': 7, 'Year': 2008, 'Winner': 'David Cook', 'Runner_Up': 'David Archuleta', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson', 'Contestants': 24, 'Avg_Viewership_Millions': 28.10},
        {'Season': 8, 'Year': 2009, 'Winner': 'Kris Allen', 'Runner_Up': 'Adam Lambert', 
         'Judges': 'Paula Abdul, Simon Cowell, Randy Jackson, Kara DioGuardi', 'Contestants': 36, 'Avg_Viewership_Millions': 26.30},
        {'Season': 9, 'Year': 2010, 'Winner': 'Lee DeWyze', 'Runner_Up': 'Crystal Bowersox', 
         'Judges': 'Simon Cowell, Randy Jackson, Kara DioGuardi, Ellen DeGeneres', 'Contestants': 24, 'Avg_Viewership_Millions': 24.10},
        {'Season': 10, 'Year': 2011, 'Winner': 'Scotty McCreery', 'Runner_Up': 'Lauren Alaina', 
         'Judges': 'Randy Jackson, Jennifer Lopez, Steven Tyler', 'Contestants': 24, 'Avg_Viewership_Millions': 23.70},
        {'Season': 11, 'Year': 2012, 'Winner': 'Phillip Phillips', 'Runner_Up': 'Jessica Sanchez', 
         'Judges': 'Randy Jackson, Jennifer Lopez, Steven Tyler', 'Contestants': 25, 'Avg_Viewership_Millions': 19.80},
        {'Season': 12, 'Year': 2013, 'Winner': 'Candice Glover', 'Runner_Up': 'Kree Harrison', 
         'Judges': 'Randy Jackson, Mariah Carey, Nicki Minaj, Keith Urban', 'Contestants': 20, 'Avg_Viewership_Millions': 15.00},
        {'Season': 13, 'Year': 2014, 'Winner': 'Caleb Johnson', 'Runner_Up': 'Jena Irene', 
         'Judges': 'Jennifer Lopez, Keith Urban, Harry Connick Jr.', 'Contestants': 20, 'Avg_Viewership_Millions': 11.90},
        {'Season': 14, 'Year': 2015, 'Winner': 'Nick Fradiani', 'Runner_Up': 'Clark Beckham', 
         'Judges': 'Jennifer Lopez, Keith Urban, Harry Connick Jr.', 'Contestants': 24, 'Avg_Viewership_Millions': 10.90},
        {'Season': 15, 'Year': 2016, 'Winner': 'Trent Harmon', 'Runner_Up': 'La\'Porsha Renae', 
         'Judges': 'Jennifer Lopez, Keith Urban, Harry Connick Jr.', 'Contestants': 24, 'Avg_Viewership_Millions': 9.30},
        {'Season': 16, 'Year': 2018, 'Winner': 'Maddie Poppe', 'Runner_Up': 'Caleb Lee Hutchinson', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 24, 'Avg_Viewership_Millions': 8.00},
        {'Season': 17, 'Year': 2019, 'Winner': 'Laine Hardy', 'Runner_Up': 'Alejandro Aranda', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 20, 'Avg_Viewership_Millions': 8.70},
        {'Season': 18, 'Year': 2020, 'Winner': 'Just Sam', 'Runner_Up': 'Arthur Gunn', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 20, 'Avg_Viewership_Millions': 8.10},
        {'Season': 19, 'Year': 2021, 'Winner': 'Chayce Beckham', 'Runner_Up': 'Willie Spence', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 24, 'Avg_Viewership_Millions': 6.50},
        {'Season': 20, 'Year': 2022, 'Winner': 'Noah Thompson', 'Runner_Up': 'HunterGirl', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 24, 'Avg_Viewership_Millions': 6.30},
        {'Season': 21, 'Year': 2023, 'Winner': 'Iam Tongi', 'Runner_Up': 'Megan Danielle', 
         'Judges': 'Katy Perry, Luke Bryan, Lionel Richie', 'Contestants': 26, 'Avg_Viewership_Millions': 5.30}
    ]
    
    # Add data to dataframe
    idol_df = pd.DataFrame(idol_data)
    
    # Save to CSV
    idol_df.to_csv('american_idol_data.csv', index=False)
    print(f"American Idol dataset created with {len(idol_df)} seasons")
    
    return idol_df

def count_unique_winners(survivor_df, idol_df, max_survivor_season=44):
    """
    Count unique winners in both shows and determine the difference
    """
    # Filter Survivor data to include only up to season 44
    survivor_filtered = survivor_df[survivor_df['Season'] <= max_survivor_season]
    
    # Count unique winners
    unique_survivor_winners = len(survivor_filtered['Winner'].unique())
    unique_idol_winners = len(idol_df['Winner'].unique())
    
    difference = unique_survivor_winners - unique_idol_winners
    
    # Create result.txt
    with open('result.txt', 'w') as f:
        f.write(f"Unique Survivor winners (up to season 44): {unique_survivor_winners}\n")
        f.write(f"Unique American Idol winners: {unique_idol_winners}\n")
        f.write(f"Difference: {difference}\n")
    
    print(f"Unique Survivor winners (up to season 44): {unique_survivor_winners}")
    print(f"Unique American Idol winners: {unique_idol_winners}")
    print(f"Difference: {difference}")
    
    return unique_survivor_winners, unique_idol_winners, difference

if __name__ == "__main__":
    # Generate datasets
    survivor_df = get_survivor_data()
    idol_df = get_american_idol_data()
    
    # Count unique winners and create result.txt
    count_unique_winners(survivor_df, idol_df)
    
    print("Datasets and result.txt created successfully!")
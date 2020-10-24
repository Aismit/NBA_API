# NBA Basketball API (2018-2019 Season)

Info 253B Spring 2020 Final Project Report<br>
Aismit Das, Rishabh Meswani, Bryant Le, Sahil Mehta, John Yang<br>
[Link](https://docs.google.com/presentation/d/1mSIm4YpcMEbrBPiOVwtCfjTct2NefI1MCbeFCPCXuFE/edit?usp=sharing) to Presentation<br>
Project Specification [Link](https://sites.ischool.berkeley.edu/i253Bs20/group-project/)

## Repository Description
* `data/` folder: CSVs of web scraped data for `games` and `players` tables
* `database/` folder: MySQL database content
* `misc/`: Table schemas, web scraping, project proposal, dependencies lisit
* `Dockerfile`: Image for server container
* `model.ipynb`, `allstar_model.pkl`: Models for all star predictions
* `Makefile`: `make` targets for automating calls to docker commands
* `server.py`, `util.py`: code + functionality containing Flask routes

## Description of API
The purpose of our API is to create an interface to our sAervice that can scrape for NBA game data from websites or query from existing online databases for player data and team data to calculate advanced analytics for live sports games. Users will be able to send post requests for different players and receive game data and be able to do a live game comparison of stats, in addition to being able to search each player independently.

We designed the API to either return previously known data (such as player and team statistics) as well as new analytics and insights based on previous data and live data. Our API mainly focuses on the 2018-2019 NBA seasons. We grab data from a couple different sources, mainly from the Basketball Reference website ([link](https://www.basketball-reference.com/)), for player and games data. We also interact with external APIs to grab live game data. This information gives us enough to write `GET` routes for player and game statistics. We stored this data in the `games` and `players` tables. We specify their schemas in the `db_schema.sql` file.

To scrape player and game data from the Basketball Reference website, we utilized the Beautiful Soup python library. Specifically, we applied the findAll method from the Beautiful Soup library to search for <th> and <tr> tags in the webpages’ HTML files and extract data from the code. Once data is extracted from the webpage, we store player and game data in CSV files. Methods for web scraping can be found in extract.py, and the scraped data can be found in games.csv and players.csv.

From the basic statistics, we then implemented calculations for advanced analytics that take basic values into account. This led to the design of the `advanced/...` routes, along with a new `advancedstats` table, which we used as a cache so that we wouldn't have to recompute values for keys that are requested multiple times. These advanced analytics include assist to turnover ratio, effecient field goal percentage, and assists per minute. These are values that were not readily available in the existing APIs or datasets we interacted with.

In our proposal, we mentioned that we wanted to incorporated more sports analytics oriented routes for our API, such as sports betting statistics. We were able to achieve this in the form of calculating the probability of a player to make the All Star team. Our group member, Aismit Das, designed a machine learning model that calculates a percentage probability corresponding to how likely a player will make the All Star team. Our machine learning model performs quite well, with just one false positive and one false negative in the confusion matrix (we also somewhat agree that Donovan Mitchell should've made the team and Khris Middleton shouldn't have). We store all star probability information in the `allstarprob` table so that we can query it for keys requested more than once. If we had more time, we would've added more predictive models like these.

We created four endpoints to access two external APIs [ScoresPro](https://www.scorespro.com/) and [SportTrader](https://sporttrader.net/). These APIs had responses that were XML-structured, as opposed to being in JSON. Therefore, we had to extract the data from these endpoints, parse through the XML for relevant data and transform this data into a JSON-structure, and load this data into our own API endpoint responses. 

In addition to the API itself, we also set up a Makefile with targets that summarize and store a lot of the docker operations that we used repetitively for setting up and tearing down the containers for the database and the server. We found this tool to be immensely helpful. In fact, to setup the database, we summarized all the operations into a single `make setup` target, with the counterpart `make terminate` that stops and removes all containers and the server Docker image.

## Summary of Routes
**Endpoint** | **Input** | **Output**
--- | --- | ---
GET /advanced/&lt;player&gt; | Player Name | Advanced statistical line of a player
GET /advanced/highest/&lt;stats&gt; | Statistical Categories separated by a dash | Player in NBA with highest average in the first category divided by the second category
GET /advanced/lowest/&lt;stats&gt; | Statistical Categories separated by a dash | Player in NBA with lowest average in the first category divided by the second category
GET /allstars | None | Returns table of all stars and their statistical lines
GET /attendance/&lt;team&gt; | Home Team | Get average, maximum, and minimum attendance for a team
GET /basic/&lt;player&gt; | Player Name | Basic statistical line of player
GET /basic/highest/&lt;stat&gt; | Statistical Category | Player in NBA with highest average in that category
GET /basic/lowest/&lt;stat&gt; | Statistical Category | Player in NBA with lowest average in that category
GET /homepoint/diff/&lt;team&gt; | Home Team | Get average win margin for a team when playing at home
GET /live/all | None | Get all live games in all basketball leagues
GET /live/nba | None | Get all live games in the NBA
GET /schedule/&lt;date&gt; | Date | Get schedule of all games that occurred on a specific date
GET /schedule/&lt;date&gt;/&lt;gameid&gt; | Date, ID | Get location, date, teams of specific game on specific date
GET /team/&lt;team&gt; | Team Name | Get players and their positions + age of an NBA team
GET /team/points/max | None | Get player with highest average points per game grouped by team
GET /team/points/min | None | Get player with lowest average points per game grouped by team
POST /allstar/prob | Player Name | Probability that player will make the all star team

## Example cURL Requests
* `curl -H "Content-Type: application/json" -X POST -d '{"name":"Anthony Davis"}' http://localhost:5000/allstar/prob`
* `curl http://localhost:5000/advanced/LeBron_James`
* `curl http://localhost:5000/advanced/highest/AST-TOV`
* `curl http://localhost:5000/advanced/lowest/AST-TOV`
* `curl http://localhost:5000/advanced/LeBron_James`
* `curl http://localhost:5000/allstars`
* `curl http://localhost:5000/attendance/LAL`
* `curl http://localhost:5000/basic/Anthony_Davis`
* `curl http://localhost:5000/basic/highest/PTS`
* `curl http://localhost:5000/basic/lowest/TRB`
* `curl http://localhost:5000/homepoint/diff/BOS`
* `curl http://localhost:5000/live/all`
* `curl http://localhost:5000/live/nba`
* `curl http://localhost:5000/schedule/04-20-2019/33914ac5-545a-46a2-b45b-c1317a932ab9`
* `curl http://localhost:5000/schedule/04-26-2019`
* `curl http://localhost:5000/team/GSW`
* `curl http://localhost:5000/team/points/max`
* `curl http://localhost:5000/team/points/min`

## Miscellaneous
**Import CSV Data into MySQL Tables**:
One of the tasks we had to perform for this project was importing web scraped data into tables within the MySQL database. We lay out the steps that we researched and took to make this happen.
1. Start up the MySQL database container
2. Use `docker cp` command to copy CSV on local computer to the docker container. (i.e. `docker cp data/players.csv db253bProj:/`)
3. Open an interactive shell (`make db-it`), then access MySQL Database with `mysql -uroot -p`, then enter password
4. Within the MySQL shell, enter `SET GLOBAL local_infile=1;` to enable local file imports.
5. `quit` out the MySQL shell.
6. Connect to the server with `local-infile` system variable by entering `mysql --local-infile=1 -uroot -p`.
7. Within the MySQL shell, select the database you want to use, then create the table.
8. Finally, load the CSV data with the following command:
```
load data local infile "/<CSV File>" into table <TABLE> fields terminated by ',' lines terminated by '\n' ignore 1 rows;
```

**How the Machine Learning Model Interacts with the API**:
1. First the route would receive a post reqeuest containing a JSON Object with the name of a player. 
2. The Database first checks to see if the user has already queried the databse for the player particularly in the allstarprob table.
3. If no player currently exists in the allstarprob table only then it will querry the player table to get the relevant player info. 
3. The Database then queries the data and finds first and foremost if the player exists
4. If the player exists then it gathers all the fields of data
5. Slight nuance: If the player is traded it uses the overall stat averages for that player (something I learned the API needed to handle) as when queried some players returned multiple results.
6. The data is then cleaned and all NAN or missing values are handled correctly (i.e. floats and ints to 0, and strings to "" ). Afterwards the data is then casted to their respective data types. 
7. The array of the data is then ready to be put into the ML Model.
8. One thing I learned was that it was easier to preload the model when the app starts and refer back to it in the routes method using a global variable declaration.
9. The corresponding SciKitLearn Libraries were also imported. 
10. The machine learning model was optimized using a python jupyter notebook that tested both logistic regression and random forest models. 
11. The data is then dumpled into a pickle file, which the server loads using the SciKitLearn External module. 
12. The model then uses that to predict the probability, and displays it back to the user as as JSON Object with the name and the allstar probability. 
13. Finally the data that was predicted is stored in the allstarprob table so that future requests as mentioned in steps 2 and 3, so these requests can be carried out faster as there are times when the model might be slightly slower in running the algorithm (i.e. in the case of neural networks). To combat these potential slowdowns I figured it would be best to have the allstarprob table act as cache similar to the advancedstats table.   

## Further Improvements
* More analytics or machine learning models to analyze data
* More complicated, involved advanced statistics (Win Shares, Usage Percentage)
* Cleaner codebase (replace large return dictionaries with reusable code)
* More statistics and routes from other basketball leagues
* Incorporate more betting related advanced analytics

## References
* Links on Importing CSV data: [link](https://stackoverflow.com/questions/59993844/error-loading-local-data-is-disabled-this-must-be-enabled-on-both-the-client), [link](https://stackoverflow.com/questions/58576129/importing-csv-file-into-mysql-docker-container)
* Import CSV File into SQL Table [link](https://www.mysqltutorial.org/import-csv-file-mysql-table/)
* Web Scraping NBA Data [link](https://towardsdatascience.com/web-scraping-nba-stats-4b4f8c525994)

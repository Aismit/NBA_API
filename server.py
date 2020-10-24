import os, json, requests
from flask import Flask, jsonify, request, Response
from flask_api import status
from MySQLdb import _mysql
import mysql.connector
import xml.etree.ElementTree as ET
from sklearn.externals import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier



app = Flask(__name__)


allstar_ml_model = joblib.load('./allstar_model.pkl')

@app.route('/')
def index():
    return 'Hello World'

@app.route('/allstar/prob', methods=["POST"])
def get_all_star_probability():
	player_to_find_allstar_prob = request.get_json()
	player_name = player_to_find_allstar_prob["name"]

	sql=f'Select * from allstarprob where player = %s'
	cursor.execute(sql,[player_name])
	data = cursor.fetchall()
	if len(data) != 0:
		for row in data:
			return_val = {"name": row[0], "allstar_probability": row[1]}
			val = 200
		return_val = json.dumps(return_val)
		return json.loads(return_val), val

	sql = f"Select * from players where player = %s"
	cursor.execute(sql, [player_name])
	data = cursor.fetchall()
	if len(data) == 0:
		return_val = {"error": "There is no player with that name, make sure name is capitalized and has an underscore in between like so: First_Last"}
		val = 404
	else:
		player_stats = {}
		if len(data) > 1:
			for row in data:
				if (str(row[5]) == "TOT"):
					player_stats["Id"] = int(check_if_null(row[0],"int"))
					player_stats["Id2"] = int(check_if_null(row[1],"int"))
					player_stats["Player"] = str(check_if_null(row[2],"str"))
					player_stats["Pos"] = str(check_if_null(row[3],"str"))
					player_stats["Age"] = float(check_if_null(row[4], "float"))
					player_stats["Tm"] = str(check_if_null(row[5], "str"))
					player_stats["G"] = float(check_if_null(row[6], "float"))
					player_stats["GS"] = float(check_if_null(row[7], "float"))
					player_stats["MP"] = float(check_if_null(row[8], "float"))
					player_stats["FG"] = float(check_if_null(row[9], "float"))
					player_stats["FGA"] = float(check_if_null(row[10], "float"))
					player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
					player_stats["3P"] = float(check_if_null(row[12], "float"))
					player_stats["3PA"] = float(check_if_null(row[13], "float"))
					player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
					player_stats["2P"] = float(check_if_null(row[15], "float"))
					player_stats["2PA"] = float(check_if_null(row[16], "float"))
					player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
					player_stats["FT"] = float(check_if_null(row[19], "float"))
					player_stats["FTA"] = float(check_if_null(row[20], "float"))
					player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
					player_stats["ORB"] = float(check_if_null(row[22], "float"))
					player_stats["DRB"] = float(check_if_null(row[23], "float"))
					player_stats["TRB"] = float(check_if_null(row[24], "float"))
					player_stats["AST"] = float(check_if_null(row[25], "float"))
					player_stats["STL"] = float(check_if_null(row[26], "float"))
					player_stats["BLK"] = float(check_if_null(row[27], "float"))
					player_stats["TOV"] = float(check_if_null(row[28], "float"))
					player_stats["PF"] = float(check_if_null(row[29], "float"))
					player_stats["PTS"] = float(check_if_null(row[30], "float"))
					player_stats["first"] = str(check_if_null(row[31], "str"))
					player_stats["last"] = str(check_if_null(row[32], "str"))
		else:
			for row in data:
				player_stats["Id"] = int(check_if_null(row[0],"int"))
				player_stats["Id2"] = int(check_if_null(row[1],"int"))
				player_stats["Player"] = str(check_if_null(row[2],"str"))
				player_stats["Pos"] = str(check_if_null(row[3],"str"))
				player_stats["Age"] = float(check_if_null(row[4], "float"))
				player_stats["Tm"] = str(check_if_null(row[5], "str"))
				player_stats["G"] = float(check_if_null(row[6], "float"))
				player_stats["GS"] = float(check_if_null(row[7], "float"))
				player_stats["MP"] = float(check_if_null(row[8], "float"))
				player_stats["FG"] = float(check_if_null(row[9], "float"))
				player_stats["FGA"] = float(check_if_null(row[10], "float"))
				player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
				player_stats["3P"] = float(check_if_null(row[12], "float"))
				player_stats["3PA"] = float(check_if_null(row[13], "float"))
				player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
				player_stats["2P"] = float(check_if_null(row[15], "float"))
				player_stats["2PA"] = float(check_if_null(row[16], "float"))
				player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
				player_stats["EFG"] = float(check_if_null(row[18], "float"))
				player_stats["FT"] = float(check_if_null(row[19], "float"))
				player_stats["FTA"] = float(check_if_null(row[20], "float"))
				player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
				player_stats["ORB"] = float(check_if_null(row[22], "float"))
				player_stats["DRB"] = float(check_if_null(row[23], "float"))
				player_stats["TRB"] = float(check_if_null(row[24], "float"))
				player_stats["AST"] = float(check_if_null(row[25], "float"))
				player_stats["STL"] = float(check_if_null(row[26], "float"))
				player_stats["BLK"] = float(check_if_null(row[27], "float"))
				player_stats["TOV"] = float(check_if_null(row[28], "float"))
				player_stats["PF"] = float(check_if_null(row[29], "float"))
				player_stats["PTS"] = float(check_if_null(row[30], "float"))
				player_stats["first"] = str(check_if_null(row[31], "str"))
				player_stats["last"] = str(check_if_null(row[32], "str"))
		global allstar_ml_model
		player_info = np.array([player_stats['Age'], player_stats['G'], player_stats['GS'], player_stats['MP'],player_stats['FG'],player_stats['FGA'], player_stats['FGPCT'],player_stats['3P'],player_stats['3PA'],player_stats['3PPCT'],
		 player_stats['2P'], player_stats['2PA'],player_stats['2PPCT'], player_stats['EFG'],player_stats['FT'], player_stats['FTA'],player_stats['FTPCT'],player_stats['ORB'],
		 player_stats['DRB'], player_stats['TRB'], player_stats['AST'], player_stats['STL'], player_stats['BLK'], player_stats['TOV'], player_stats['PF'],
		 player_stats['PTS']])
		#print(player_info)
		probability_value = allstar_ml_model.predict_proba([player_info])
		#print(probability_value, flush=True)
		probability_value = float(probability_value[0][1])
		sql = f"INSERT INTO allstarprob (player,prob) VALUES (%s, %s)"
		cursor.execute(sql,[player_name, probability_value])
		db.commit()
		return_val = {"name": player_name, "allstar_probability": probability_value}
		val=200
	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#helper method to check if values are null
def check_if_null(val, type_c):
	#print(val)
	#print(val == None)
	if val == None:
		if type_c == "str":
			return ""
		elif type_c == "int":
			return 0
		elif type_c == "float":
			return 0
		else:
			return 0
	else:
		return val

#player in the nba with highest specific stat
@app.route('/basic/highest/<string:stat>', methods=["GET"])
def get_player_with_highest_stat(stat):
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	stats = str(stat)
	sql = f"Show columns from players"
	cursor.execute(sql)
	data = cursor.fetchall()
	#print(data, flush=True)
	set_of_all_columns = set()
	#print("hello", flush=True)
	for elem in data:
		set_of_all_columns.add(elem[0])
	#print("hello", flush=True)
	if stat not in set_of_all_columns:
		return_val = {"error": "There is no stat with that name, pick one from - Age, G, GS, MP, FG, FGA, FGPCT, 3P, 3PA, 3PPCT, 2P, 2PA, 2PPCT, FT, FTA, FTPCT, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS"}
		val = 404
		print("hello", flush=True)
	else:
		sql = f"Select * from players order by %s DESC limit 1"
		sql = sql.replace(f"%s", stats)
		cursor.execute(sql)
		data = cursor.fetchall()
		#print(data, flush=True)
		player_stats = {}
		val = 200
		for row in data:
			player_stats["Id"] = int(check_if_null(row[0],"int"))
			player_stats["Id2"] = int(check_if_null(row[1],"int"))
			player_stats["Player"] = str(check_if_null(row[2],"str"))
			player_stats["Pos"] = str(check_if_null(row[3],"str"))
			player_stats["Age"] = float(check_if_null(row[4], "float"))
			player_stats["Tm"] = str(check_if_null(row[5], "str"))
			player_stats["G"] = float(check_if_null(row[6], "float"))
			player_stats["GS"] = float(check_if_null(row[7], "float"))
			player_stats["MP"] = float(check_if_null(row[8], "float"))
			player_stats["FG"] = float(check_if_null(row[9], "float"))
			player_stats["FGA"] = float(check_if_null(row[10], "float"))
			player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
			player_stats["3P"] = float(check_if_null(row[12], "float"))
			player_stats["3PA"] = float(check_if_null(row[13], "float"))
			player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
			player_stats["2P"] = float(check_if_null(row[15], "float"))
			player_stats["2PA"] = float(check_if_null(row[16], "float"))
			player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
			player_stats["FT"] = float(check_if_null(row[19], "float"))
			player_stats["FTA"] = float(check_if_null(row[20], "float"))
			player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
			player_stats["ORB"] = float(check_if_null(row[22], "float"))
			player_stats["DRB"] = float(check_if_null(row[23], "float"))
			player_stats["TRB"] = float(check_if_null(row[24], "float"))
			player_stats["AST"] = float(check_if_null(row[25], "float"))
			player_stats["STL"] = float(check_if_null(row[26], "float"))
			player_stats["BLK"] = float(check_if_null(row[27], "float"))
			player_stats["TOV"] = float(check_if_null(row[28], "float"))
			player_stats["PF"] = float(check_if_null(row[29], "float"))
			player_stats["PTS"] = float(check_if_null(row[30], "float"))
			player_stats["first"] = str(check_if_null(row[31], "str"))
			player_stats["last"] = str(check_if_null(row[32], "str"))
			player_stats["allstar"] = int(check_if_null(row[33], "int"))
		return_val = player_stats
	return_val = json.dumps(return_val)
	return json.loads(return_val), val
	#return json.loads(return_val), val

#player in the nba with a lowest specific stat
@app.route('/basic/lowest/<string:stat>', methods=["GET"])
def get_player_with_lowest_stat(stat):
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	stats = str(stat)
	sql = f"Show columns from players"
	cursor.execute(sql)
	data = cursor.fetchall()
	#print(data, flush=True)
	set_of_all_columns = set()
	for elem in data:
		set_of_all_columns.add(elem[0])
	if stats not in set_of_all_columns:
		print("hello", flush=True)
		return_val = {"error": "There is no stat with that name, pick one from- Age, G, GS, MP, FG, FGA, FGPCT, 3P, 3PA, 3PPCT, 2P, 2PA, 2PPCT, FT, FTA, FTPCT, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS"}
		val = 404
	else:
		sql = f"Select * from players order by %s ASC limit 1"
		sql = sql.replace(f"%s", stats)
		cursor.execute(sql)
		data = cursor.fetchall()
		print(data, flush=True)
		player_stats = {}
		val = 200
		for row in data:
			player_stats["Id"] = int(check_if_null(row[0],"int"))
			player_stats["Id2"] = int(check_if_null(row[1],"int"))
			player_stats["Player"] = str(check_if_null(row[2],"str"))
			player_stats["Pos"] = str(check_if_null(row[3],"str"))
			player_stats["Age"] = float(check_if_null(row[4], "float"))
			player_stats["Tm"] = str(check_if_null(row[5], "str"))
			player_stats["G"] = float(check_if_null(row[6], "float"))
			player_stats["GS"] = float(check_if_null(row[7], "float"))
			player_stats["MP"] = float(check_if_null(row[8], "float"))
			player_stats["FG"] = float(check_if_null(row[9], "float"))
			player_stats["FGA"] = float(check_if_null(row[10], "float"))
			player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
			player_stats["3P"] = float(check_if_null(row[12], "float"))
			player_stats["3PA"] = float(check_if_null(row[13], "float"))
			player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
			player_stats["2P"] = float(check_if_null(row[15], "float"))
			player_stats["2PA"] = float(check_if_null(row[16], "float"))
			player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
			player_stats["FT"] = float(check_if_null(row[19], "float"))
			player_stats["FTA"] = float(check_if_null(row[20], "float"))
			player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
			player_stats["ORB"] = float(check_if_null(row[22], "float"))
			player_stats["DRB"] = float(check_if_null(row[23], "float"))
			player_stats["TRB"] = float(check_if_null(row[24], "float"))
			player_stats["AST"] = float(check_if_null(row[25], "float"))
			player_stats["STL"] = float(check_if_null(row[26], "float"))
			player_stats["BLK"] = float(check_if_null(row[27], "float"))
			player_stats["TOV"] = float(check_if_null(row[28], "float"))
			player_stats["PF"] = float(check_if_null(row[29], "float"))
			player_stats["PTS"] = float(check_if_null(row[30], "float"))
			player_stats["first"] = str(check_if_null(row[31], "str"))
			player_stats["last"] = str(check_if_null(row[32], "str"))
			player_stats["allstar"] = int(check_if_null(row[33], "int"))
		return_val = player_stats
	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#gets all star
@app.route('/allstars', methods=["GET"])
def get_allstars():
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	sql = f"Select * from players where allstar = 1"
	cursor.execute(sql)
	data = cursor.fetchall()
	#print(data, flush=True)
	set_of_all_columns = set()
	players = []
	val = 200
	for row in data:
		player_stats ={}
		player_stats["Id"] = int(check_if_null(row[0],"int"))
		player_stats["Id2"] = int(check_if_null(row[1],"int"))
		player_stats["Player"] = str(check_if_null(row[2],"str"))
		player_stats["Pos"] = str(check_if_null(row[3],"str"))
		player_stats["Age"] = float(check_if_null(row[4], "float"))
		player_stats["Tm"] = str(check_if_null(row[5], "str"))
		player_stats["G"] = float(check_if_null(row[6], "float"))
		player_stats["GS"] = float(check_if_null(row[7], "float"))
		player_stats["MP"] = float(check_if_null(row[8], "float"))
		player_stats["FG"] = float(check_if_null(row[9], "float"))
		player_stats["FGA"] = float(check_if_null(row[10], "float"))
		player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
		player_stats["3P"] = float(check_if_null(row[12], "float"))
		player_stats["3PA"] = float(check_if_null(row[13], "float"))
		player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
		player_stats["2P"] = float(check_if_null(row[15], "float"))
		player_stats["2PA"] = float(check_if_null(row[16], "float"))
		player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
		player_stats["FT"] = float(check_if_null(row[19], "float"))
		player_stats["FTA"] = float(check_if_null(row[20], "float"))
		player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
		player_stats["ORB"] = float(check_if_null(row[22], "float"))
		player_stats["DRB"] = float(check_if_null(row[23], "float"))
		player_stats["TRB"] = float(check_if_null(row[24], "float"))
		player_stats["AST"] = float(check_if_null(row[25], "float"))
		player_stats["STL"] = float(check_if_null(row[26], "float"))
		player_stats["BLK"] = float(check_if_null(row[27], "float"))
		player_stats["TOV"] = float(check_if_null(row[28], "float"))
		player_stats["PF"] = float(check_if_null(row[29], "float"))
		player_stats["PTS"] = float(check_if_null(row[30], "float"))
		player_stats["first"] = str(check_if_null(row[31], "str"))
		player_stats["last"] = str(check_if_null(row[32], "str"))
		player_stats["allstar"] = int(check_if_null(row[33], "int"))
		players+=[player_stats]
	return_val = {"allstars":players}
	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#find player in the nba with the highest advanced stat
@app.route('/advanced/highest/<string:stats>', methods=["GET"])
def get_player_with_highest_advanced_stat(stats):
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	stats = str(stats)
	stats = stats.split("-")
	sql = f"Show columns from players"
	cursor.execute(sql)
	data = cursor.fetchall()
	#print(data, flush=True)
	set_of_all_columns = set()
	#print("hello", flush=True)
	for elem in data:
		set_of_all_columns.add(elem[0])
	#print("hello", flush=True)
	for stat in stats:
		if stat not in set_of_all_columns:
			return_val = {"error": "There is no stat with that name, pick one from - Age, G, GS, MP, FG, FGA, FGPCT, 3P, 3PA, 3PPCT, 2P, 2PA, 2PPCT, FT, FTA, FTPCT, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS"}
			val = 404
		#print("hello", flush=True)
	else:
		sql = f"Select * from players order by %s/%d DESC limit 1"
		sql = sql.replace(f"%s", stats[0])
		sql = sql.replace(f"%d", stats[1])
		cursor.execute(sql)
		data = cursor.fetchall()
		#print(data, flush=True)
		player_stats = {}
		val = 200
		for row in data:
			player_stats["Id"] = int(check_if_null(row[0],"int"))
			player_stats["Id2"] = int(check_if_null(row[1],"int"))
			player_stats["Player"] = str(check_if_null(row[2],"str"))
			player_stats["Pos"] = str(check_if_null(row[3],"str"))
			player_stats["Age"] = float(check_if_null(row[4], "float"))
			player_stats["Tm"] = str(check_if_null(row[5], "str"))
			player_stats["G"] = float(check_if_null(row[6], "float"))
			player_stats["GS"] = float(check_if_null(row[7], "float"))
			player_stats["MP"] = float(check_if_null(row[8], "float"))
			player_stats["FG"] = float(check_if_null(row[9], "float"))
			player_stats["FGA"] = float(check_if_null(row[10], "float"))
			player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
			player_stats["3P"] = float(check_if_null(row[12], "float"))
			player_stats["3PA"] = float(check_if_null(row[13], "float"))
			player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
			player_stats["2P"] = float(check_if_null(row[15], "float"))
			player_stats["2PA"] = float(check_if_null(row[16], "float"))
			player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
			player_stats["FT"] = float(check_if_null(row[19], "float"))
			player_stats["FTA"] = float(check_if_null(row[20], "float"))
			player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
			player_stats["ORB"] = float(check_if_null(row[22], "float"))
			player_stats["DRB"] = float(check_if_null(row[23], "float"))
			player_stats["TRB"] = float(check_if_null(row[24], "float"))
			player_stats["AST"] = float(check_if_null(row[25], "float"))
			player_stats["STL"] = float(check_if_null(row[26], "float"))
			player_stats["BLK"] = float(check_if_null(row[27], "float"))
			player_stats["TOV"] = float(check_if_null(row[28], "float"))
			player_stats["PF"] = float(check_if_null(row[29], "float"))
			player_stats["PTS"] = float(check_if_null(row[30], "float"))
			player_stats["first"] = str(check_if_null(row[31], "str"))
			player_stats["last"] = str(check_if_null(row[32], "str"))
			player_stats["allstar"] = int(check_if_null(row[33], "int"))
		return_val = player_stats
	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#find player in the nba with the lowest advanced stat
@app.route('/advanced/lowest/<string:stats>', methods=["GET"])
def get_player_with_lowest_advanced_stat(stats):
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	stats = str(stats)
	stats = stats.split("-")
	sql = f"Show columns from players"
	cursor.execute(sql)
	data = cursor.fetchall()
	#print(data, flush=True)
	set_of_all_columns = set()
	#print("hello", flush=True)
	for elem in data:
		set_of_all_columns.add(elem[0])
	#print("hello", flush=True)
	for stat in stats:
		if stat not in set_of_all_columns:
			return_val = {"error": "There is no stat with that name, pick one from - Age, G, GS, MP, FG, FGA, FGPCT, 3P, 3PA, 3PPCT, 2P, 2PA, 2PPCT, FT, FTA, FTPCT, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS"}
			val = 404
		#print("hello", flush=True)
	else:
		sql = f"Select * from players order by %s/%d ASC limit 1"
		sql = sql.replace(f"%s", stats[0])
		sql = sql.replace(f"%d", stats[1])
		cursor.execute(sql)
		data = cursor.fetchall()
		#print(data, flush=True)
		player_stats = {}
		val = 200
		for row in data:
			player_stats["Id"] = int(check_if_null(row[0],"int"))
			player_stats["Id2"] = int(check_if_null(row[1],"int"))
			player_stats["Player"] = str(check_if_null(row[2],"str"))
			player_stats["Pos"] = str(check_if_null(row[3],"str"))
			player_stats["Age"] = float(check_if_null(row[4], "float"))
			player_stats["Tm"] = str(check_if_null(row[5], "str"))
			player_stats["G"] = float(check_if_null(row[6], "float"))
			player_stats["GS"] = float(check_if_null(row[7], "float"))
			player_stats["MP"] = float(check_if_null(row[8], "float"))
			player_stats["FG"] = float(check_if_null(row[9], "float"))
			player_stats["FGA"] = float(check_if_null(row[10], "float"))
			player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
			player_stats["3P"] = float(check_if_null(row[12], "float"))
			player_stats["3PA"] = float(check_if_null(row[13], "float"))
			player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
			player_stats["2P"] = float(check_if_null(row[15], "float"))
			player_stats["2PA"] = float(check_if_null(row[16], "float"))
			player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
			player_stats["FT"] = float(check_if_null(row[19], "float"))
			player_stats["FTA"] = float(check_if_null(row[20], "float"))
			player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
			player_stats["ORB"] = float(check_if_null(row[22], "float"))
			player_stats["DRB"] = float(check_if_null(row[23], "float"))
			player_stats["TRB"] = float(check_if_null(row[24], "float"))
			player_stats["AST"] = float(check_if_null(row[25], "float"))
			player_stats["STL"] = float(check_if_null(row[26], "float"))
			player_stats["BLK"] = float(check_if_null(row[27], "float"))
			player_stats["TOV"] = float(check_if_null(row[28], "float"))
			player_stats["PF"] = float(check_if_null(row[29], "float"))
			player_stats["PTS"] = float(check_if_null(row[30], "float"))
			player_stats["first"] = str(check_if_null(row[31], "str"))
			player_stats["last"] = str(check_if_null(row[32], "str"))
			player_stats["allstar"] = int(check_if_null(row[33], "int"))
		return_val = player_stats
	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#get all basic stats for the player
@app.route('/basic/<string:player_name>', methods=["GET"])
def get_player_basic_stats(player_name):
	#db = mysql.connector.connect(host="127.0.0.1",port=3306, user="root", password="my-secret-pw", database="demo")
	#cursor = db.cursor()
	player_name = str(player_name)
	player_name = player_name.replace("_", " ")
	sql = f"Select * from players where player = %s"
	cursor.execute(sql, [player_name])
	data = cursor.fetchall()
	#print(data, flush =True)
	if len(data) == 0:
		return_val = {"error": "There is no player with that name, make sure name is capitalized and has an underscore in between like so: First_Last"}
		val = 404
	else:
		player_stats = {}
		if len(data) > 1:
			for row in data:
				if (str(row[5]) == "TOT"):
					player_stats["Id"] = int(check_if_null(row[0],"int"))
					player_stats["Id2"] = int(check_if_null(row[1],"int"))
					player_stats["Player"] = str(check_if_null(row[2],"str"))
					player_stats["Pos"] = str(check_if_null(row[3],"str"))
					player_stats["Age"] = float(check_if_null(row[4], "float"))
					player_stats["Tm"] = str(check_if_null(row[5], "str"))
					player_stats["G"] = float(check_if_null(row[6], "float"))
					player_stats["GS"] = float(check_if_null(row[7], "float"))
					player_stats["MP"] = float(check_if_null(row[8], "float"))
					player_stats["FG"] = float(check_if_null(row[9], "float"))
					player_stats["FGA"] = float(check_if_null(row[10], "float"))
					player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
					player_stats["3P"] = float(check_if_null(row[12], "float"))
					player_stats["3PA"] = float(check_if_null(row[13], "float"))
					player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
					player_stats["2P"] = float(check_if_null(row[15], "float"))
					player_stats["2PA"] = float(check_if_null(row[16], "float"))
					player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
					player_stats["FT"] = float(check_if_null(row[19], "float"))
					player_stats["FTA"] = float(check_if_null(row[20], "float"))
					player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
					player_stats["ORB"] = float(check_if_null(row[22], "float"))
					player_stats["DRB"] = float(check_if_null(row[23], "float"))
					player_stats["TRB"] = float(check_if_null(row[24], "float"))
					player_stats["AST"] = float(check_if_null(row[25], "float"))
					player_stats["STL"] = float(check_if_null(row[26], "float"))
					player_stats["BLK"] = float(check_if_null(row[27], "float"))
					player_stats["TOV"] = float(check_if_null(row[28], "float"))
					player_stats["PF"] = float(check_if_null(row[29], "float"))
					player_stats["PTS"] = float(check_if_null(row[30], "float"))
					player_stats["first"] = str(check_if_null(row[31], "str"))
					player_stats["last"] = str(check_if_null(row[32], "str"))
					player_stats["allstar"] = int(check_if_null(row[33], "int"))
			return_val = player_stats
			val = 200
		else:
			for row in data:
					player_stats["Id"] = int(check_if_null(row[0],"int"))
					player_stats["Id2"] = int(check_if_null(row[1],"int"))
					player_stats["Player"] = str(check_if_null(row[2],"str"))
					player_stats["Pos"] = str(check_if_null(row[3],"str"))
					player_stats["Age"] = float(check_if_null(row[4], "float"))
					player_stats["Tm"] = str(check_if_null(row[5], "str"))
					player_stats["G"] = float(check_if_null(row[6], "float"))
					player_stats["GS"] = float(check_if_null(row[7], "float"))
					player_stats["MP"] = float(check_if_null(row[8], "float"))
					player_stats["FG"] = float(check_if_null(row[9], "float"))
					player_stats["FGA"] = float(check_if_null(row[10], "float"))
					player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
					player_stats["3P"] = float(check_if_null(row[12], "float"))
					player_stats["3PA"] = float(check_if_null(row[13], "float"))
					player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
					player_stats["2P"] = float(check_if_null(row[15], "float"))
					player_stats["2PA"] = float(check_if_null(row[16], "float"))
					player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
					player_stats["FT"] = float(check_if_null(row[19], "float"))
					player_stats["FTA"] = float(check_if_null(row[20], "float"))
					player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
					player_stats["ORB"] = float(check_if_null(row[22], "float"))
					player_stats["DRB"] = float(check_if_null(row[23], "float"))
					player_stats["TRB"] = float(check_if_null(row[24], "float"))
					player_stats["AST"] = float(check_if_null(row[25], "float"))
					player_stats["STL"] = float(check_if_null(row[26], "float"))
					player_stats["BLK"] = float(check_if_null(row[27], "float"))
					player_stats["TOV"] = float(check_if_null(row[28], "float"))
					player_stats["PF"] = float(check_if_null(row[29], "float"))
					player_stats["PTS"] = float(check_if_null(row[30], "float"))
					player_stats["first"] = str(check_if_null(row[31], "str"))
					player_stats["last"] = str(check_if_null(row[32], "str"))
					player_stats["allstar"] = int(check_if_null(row[33], "int"))
			return_val = player_stats
			val = 200


	return_val = json.dumps(return_val)
	return json.loads(return_val), val

#gives information about all positions and corresponding ages for a team
@app.route("/team/<id_value>", methods=["GET"])
def query_team (id_value):
	sql = "SELECT Player, Pos, Age from players WHERE Tm = %s"
	cursor.execute(sql, [id_value])
	data = cursor.fetchall()
	if len(data) > 0:
		response_msg = list()
		for row in data:
			response_msg_link = dict()
			response_msg_link["Pos"] = row[0]
			response_msg_link["Age"] = (row[1])
			response_msg.append(response_msg_link)
		return(json.dumps(response_msg))
	else:
		error = "There is no such team. Please check again."
		return error, 404

#find the player with the highest average points per game grouped by team
@app.route("/team/points/max", methods=["GET"])
def max_points_team():
	cursor.execute("SELECT o.Player, o.tm, o.pts FROM `players` o LEFT JOIN `players` b ON o.tm = b.tm AND o.pts < b.pts WHERE b.pts is NULL")
	data = cursor.fetchall()
	if len(data) > 0:
		response_msg = list()
		for row in data:
			response_msg_link = dict()
			response_msg_link["Player"] = row[0]
			response_msg_link["Tm"] = (row[1])
			response_msg_link["pts"] = (float(row[2]))
			response_msg.append(response_msg_link)
		return(json.dumps(response_msg))

#find the player with the lowest average points per game grouped by team
@app.route("/team/points/min", methods=["GET"])
def min_points_team():
	cursor.execute("SELECT o.Player, o.tm, o.pts FROM `players` o LEFT JOIN `players` b ON o.tm = b.tm AND o.pts > b.pts WHERE b.pts is NULL")
	data = cursor.fetchall()
	if len(data) > 0:
		response_msg = list()
		for row in data:
			response_msg_link = dict()
			response_msg_link["Player"] = row[0]
			response_msg_link["Tm"] = (row[1])
			response_msg_link["pts"] = (float(row[2]))
			response_msg.append(response_msg_link)
		return(json.dumps(response_msg))

#attendance stats for home team
@app.route("/attendance/<string:id_value>", methods=["GET"])
def attendance_stats(id_value):
	sql = "SELECT Home, AVG(Attendance), MAX(ATTENDANCE), MIN(Attendance) From games WHERE HOME = %s GROUP BY HOME"
	cursor.execute(sql, [id_value])
	data = cursor.fetchall()
	if len(data) > 0:
		response_msg = list()
		for row in data:
			response_msg_link = dict()
			response_msg_link["Home"] = row[0]
			response_msg_link["AVG(Attendance"] = (int(row[1]))
			response_msg_link["MAX(Attendance"] = (int(row[2]))
			response_msg_link["MIN(Attendance"] = (int(row[3]))
			response_msg.append(response_msg_link)
		return(json.dumps(response_msg))
	else:
		error = "There is no such team. Please check again."
		return error, 404


#average win margin during home games
@app.route("/homepoint/diff/<string:id_value>", methods=["GET"])
def home_point_diff(id_value):
	sql = "SELECT AVG(HomePTS - VisitorPTS) as Point_Difference from games WHERE Home = %s"
	cursor.execute(sql, [id_value])
	data = cursor.fetchall()
	if len(data) > 0:
		response_msg = list()
		for row in data:
			response_msg_link = dict()
			response_msg_link["Point_Diff"] = float(row[0])
			response_msg.append(response_msg_link)
		return(json.dumps(response_msg))
	else:
		error = "There is no such team. Please check again."
		return error, 404

#get advanced stats for a player
@app.route('/advanced/<string:player_name>', methods=["GET"])
def get_player_advanced_stats(player_name):
	#
	def calculate_assist_to_to_ratio(value1,value2):
		if value2 == 0:
			return 0
		else:
			return float(value1/value2)
	player_name = str(player_name)
	player_name = player_name.replace("_", " ")
	sql = f"Select * from advancedstats where player = %s"
	cursor.execute(sql, [player_name])
	data = cursor.fetchall()
	if len(data) == 0:
		#data not in adnaced have to create it for the first-time
		sql = f"Select * from players where player = %s"
		cursor.execute(sql, [player_name])
		data = cursor.fetchall()
		if len(data) == 0:
			return_val = {"error": "There is no player with that name, make sure name is capitalized and has an underscore in between like so: First_Last"}
			val = 404
		else:
			player_stats = {}
			advanced_player_stats = {}
			if len(data) > 1:
				for row in data:
					if (str(row[5]) == "TOT"):
						player_stats["Id"] = int(check_if_null(row[0],"int"))
						player_stats["Id2"] = int(check_if_null(row[1],"int"))
						player_stats["Player"] = str(check_if_null(row[2],"str"))
						player_stats["Pos"] = str(check_if_null(row[3],"str"))
						player_stats["Age"] = float(check_if_null(row[4], "float"))
						player_stats["Tm"] = str(check_if_null(row[5], "str"))
						player_stats["G"] = float(check_if_null(row[6], "float"))
						player_stats["GS"] = float(check_if_null(row[7], "float"))
						player_stats["MP"] = float(check_if_null(row[8], "float"))
						player_stats["FG"] = float(check_if_null(row[9], "float"))
						player_stats["FGA"] = float(check_if_null(row[10], "float"))
						player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
						player_stats["3P"] = float(check_if_null(row[12], "float"))
						player_stats["3PA"] = float(check_if_null(row[13], "float"))
						player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
						player_stats["2P"] = float(check_if_null(row[15], "float"))
						player_stats["2PA"] = float(check_if_null(row[16], "float"))
						player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
						player_stats["FT"] = float(check_if_null(row[19], "float"))
						player_stats["FTA"] = float(check_if_null(row[20], "float"))
						player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
						player_stats["ORB"] = float(check_if_null(row[22], "float"))
						player_stats["DRB"] = float(check_if_null(row[23], "float"))
						player_stats["TRB"] = float(check_if_null(row[24], "float"))
						player_stats["AST"] = float(check_if_null(row[25], "float"))
						player_stats["STL"] = float(check_if_null(row[26], "float"))
						player_stats["BLK"] = float(check_if_null(row[27], "float"))
						player_stats["TOV"] = float(check_if_null(row[28], "float"))
						player_stats["PF"] = float(check_if_null(row[29], "float"))
						player_stats["PTS"] = float(check_if_null(row[30], "float"))
						player_stats["first"] = str(check_if_null(row[31], "str"))
						player_stats["last"] = str(check_if_null(row[32], "str"))
						player_stats["allstar"] = int(check_if_null(row[33], "int"))
				advanced_player_stats["assist_to_turn_over_ratio"] = player_stats["AST"]/player_stats["TOV"]
				advanced_player_stats["defensive_rebound_percentage"] = player_stats["DRB"]/player_stats["TRB"]
				advanced_player_stats["offensive_rebound_percentage"] = player_stats["ORB"]/player_stats["TRB"]
				advanced_player_stats["field_goal_attempts_to_assist_ratio"] = player_stats["FGA"]/player_stats["AST"]
				advanced_player_stats["field_goals_made_per_minute"] = player_stats["FG"]/player_stats["MP"]
				advanced_player_stats["effective_field_goal_percentage"] = (player_stats["FG"] + 0.5 * player_stats["3P"])/player_stats["FGA"]
				advanced_player_stats["assists_per_minute"] = player_stats["AST"]/player_stats["MP"]
				advanced_player_stats["player"] = player_stats["Player"]
				return_val = advanced_player_stats
				val = 200
				sql = f"INSERT INTO advancedstats (player,a2tr,drp,orp,fg2ar,fgmpm,efg,apm) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)"
				cursor.execute(sql,[advanced_player_stats["player"],advanced_player_stats["assist_to_turn_over_ratio"], advanced_player_stats["defensive_rebound_percentage"],
					advanced_player_stats["offensive_rebound_percentage"],advanced_player_stats["field_goal_attempts_to_assist_ratio"], advanced_player_stats["field_goals_made_per_minute"],
					advanced_player_stats["effective_field_goal_percentage"],advanced_player_stats["assists_per_minute"]])
				db.commit()
			else:
				player_stats = {}
				advanced_player_stats = {}
				for row in data:
						player_stats["Id"] = int(check_if_null(row[0],"int"))
						player_stats["Id2"] = int(check_if_null(row[1],"int"))
						player_stats["Player"] = str(check_if_null(row[2],"str"))
						player_stats["Pos"] = str(check_if_null(row[3],"str"))
						player_stats["Age"] = float(check_if_null(row[4], "float"))
						player_stats["Tm"] = str(check_if_null(row[5], "str"))
						player_stats["G"] = float(check_if_null(row[6], "float"))
						player_stats["GS"] = float(check_if_null(row[7], "float"))
						player_stats["MP"] = float(check_if_null(row[8], "float"))
						player_stats["FG"] = float(check_if_null(row[9], "float"))
						player_stats["FGA"] = float(check_if_null(row[10], "float"))
						player_stats["FGPCT"] = float(check_if_null(row[11], "float"))
						player_stats["3P"] = float(check_if_null(row[12], "float"))
						player_stats["3PA"] = float(check_if_null(row[13], "float"))
						player_stats["3PPCT"] = float(check_if_null(row[14], "float"))
						player_stats["2P"] = float(check_if_null(row[15], "float"))
						player_stats["2PA"] = float(check_if_null(row[16], "float"))
						player_stats["2PPCT"] = float(check_if_null(row[17], "float"))
						player_stats["FT"] = float(check_if_null(row[19], "float"))
						player_stats["FTA"] = float(check_if_null(row[20], "float"))
						player_stats["FTPCT"] = float(check_if_null(row[21], "float"))
						player_stats["ORB"] = float(check_if_null(row[22], "float"))
						player_stats["DRB"] = float(check_if_null(row[23], "float"))
						player_stats["TRB"] = float(check_if_null(row[24], "float"))
						player_stats["AST"] = float(check_if_null(row[25], "float"))
						player_stats["STL"] = float(check_if_null(row[26], "float"))
						player_stats["BLK"] = float(check_if_null(row[27], "float"))
						player_stats["TOV"] = float(check_if_null(row[28], "float"))
						player_stats["PF"] = float(check_if_null(row[29], "float"))
						player_stats["PTS"] = float(check_if_null(row[30], "float"))
						player_stats["first"] = str(check_if_null(row[31], "str"))
						player_stats["last"] = str(check_if_null(row[32], "str"))
						player_stats["allstar"] = int(check_if_null(row[33], "int"))
				advanced_player_stats["assist_to_turn_over_ratio"] = player_stats["AST"]/player_stats["TOV"]
				advanced_player_stats["defensive_rebound_percentage"] = player_stats["DRB"]/player_stats["TRB"]
				advanced_player_stats["offensive_rebound_percentage"] = player_stats["ORB"]/player_stats["TRB"]
				advanced_player_stats["field_goal_attempts_to_assist_ratio"] = player_stats["FGA"]/player_stats["AST"]
				advanced_player_stats["field_goals_made_per_minute"] = player_stats["FG"]/player_stats["MP"]
				advanced_player_stats["effective_field_goal_percentage"] = (player_stats["FG"] + 0.5 * player_stats["3P"])/player_stats["FGA"]
				advanced_player_stats["assists_per_minute"] = player_stats["AST"]/player_stats["MP"]
				advanced_player_stats["player"] = player_stats["Player"]
				sql = f"INSERT INTO advancedstats (player,a2tr,drp,orp,fg2ar,fgmpm,efg,apm) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)"
				cursor.execute(sql,[advanced_player_stats["player"],advanced_player_stats["assist_to_turn_over_ratio"], advanced_player_stats["defensive_rebound_percentage"],
					advanced_player_stats["offensive_rebound_percentage"],advanced_player_stats["field_goal_attempts_to_assist_ratio"], advanced_player_stats["field_goals_made_per_minute"],
					advanced_player_stats["effective_field_goal_percentage"],advanced_player_stats["assists_per_minute"]])
				db.commit()
				return_val = advanced_player_stats
				val = 200
	else:
		advanced_player_stats = {}
		for row in data:
			advanced_player_stats["player"] = str(row[0])
			advanced_player_stats["assist_to_turn_over_ratio"] = float(row[1])
			advanced_player_stats["defensive_rebound_percentage"] = float(row[2])
			advanced_player_stats["offensive_rebound_percentage"] = float(row[3])
			advanced_player_stats["field_goal_attempts_to_assist_ratio"] = float(row[4])
			advanced_player_stats["field_goals_made_per_minute"] = float(row[5])
			advanced_player_stats["effective_field_goal_percentage"] = float(row[6])
			advanced_player_stats["assists_per_minute"] = float(row[7])
		return_val = advanced_player_stats
		val = 200
	return_val = json.dumps(return_val)
	return json.loads(return_val), val


#gets all live games in the nba
@app.route('/live/nba')
def get_nba_live_games():
    xml = requests.request("GET", "https://www.scorespro.com/rss2/live-basketball.xml")
    root = ET.fromstring(xml.text)
    games = []
    for i in root[0]:
        game = dict()
        if i.tag == "item" and "USA" in i[0].text:
            game['name'] = i[0].text[35:]
            game['status'] = i[1].text
            game['last_update'] = i[2].text
            games.append(game)

    return jsonify({'games': games}), 200

#get all live games in all sports
@app.route('/live/all')
def get_all_live_games():
    xml = requests.request("GET", "https://www.scorespro.com/rss2/live-basketball.xml")
    root = ET.fromstring(xml.text)
    games = []
    for i in root[0]:
        game = dict()
        if i.tag == "item":
            game['name'] = i[0].text[35:]
            game['status'] = i[1].text
            game['last_update'] = i[2].text
            games.append(game)

    return jsonify({'games': games}), 200

#/schedule/04-26-2019
@app.route('/schedule/<date>')
def get_schedule(date):
    m, d, y = date.split("-")
    API_KEY = "mahypc4akkgz97md52d2je73"
    xml = requests.request("GET", "http://api.sportradar.us/nba/trial/v7/en/games/{}/{}/{}/schedule.xml?api_key={}".format(y, m, d, API_KEY))
    root = ET.fromstring(xml.text)
    games = []
    for i in root[0][0]:
        game = dict()
        game['id'] = i.attrib['id']
        game['date'] = i.attrib['scheduled']
        game['home'] = i[2].attrib['name']
        game['away'] = i[3].attrib['name']
        games.append(game)

    return jsonify({'games':games}), 200

# schedule/04-26-2019/9bbed7e7-648a-444d-ba07-09d60603205f
@app.route('/schedule/<date>/<gameid>')
def get_game_info(date, gameid):
    m, d, y = date.split("-")
    API_KEY = "mahypc4akkgz97md52d2je73"
    xml = requests.request("GET", "http://api.sportradar.us/nba/trial/v7/en/games/{}/{}/{}/schedule.xml?api_key={}".format(y, m, d, API_KEY))
    root = ET.fromstring(xml.text)
    for i in root[0][0]:
        if i.attrib['id'] == gameid:
            game = dict()
            game['date'] = i.attrib['scheduled']
            game['location'] = "{}, {}".format(i[1].attrib['city'], i[1].attrib['state'])
            game['home_name'] = i[2].attrib['name']
            game['home_alias'] = i[2].attrib['alias']
            game['away_name'] = i[3].attrib['name']
            game['away_alias'] = i[3].attrib['alias']
            return jsonify({'game': game}), 200

    return jsonify({'error': "That game id does not exist."}), 404
if __name__ == '__main__':
    db = mysql.connector.connect(host='db253bProj', user='root', passwd='asg253dbProj', database='db253BProj')
    cursor = db.cursor(buffered=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

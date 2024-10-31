import requests
import csv

# Thông tin RapidAPI
RAPIDAPI_HOST = "sofascore.p.rapidapi.com"
RAPIDAPI_KEY = "5fa1b3ec61msh748c83f0ec34ff4p18fe14jsn062670fd057e"

# Hàm để lấy dữ liệu từ RapidAPI
def get_player_statistics(match_id, player_id):
    url = f"https://sofascore.p.rapidapi.com/matches/get-player-statistics?matchId={match_id}&playerId={player_id}"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Nhập ID cầu thủ từ người dùng
player_id = input("Nhập ID cầu thủ: ")

# Nhập 5 ID của các trận đấu từ người dùng
match_ids = []
for i in range(5):
    match_id = input(f"Nhập ID trận đấu {i+1}: ")
    match_ids.append(match_id)

# Tạo tên file dựa trên ID cầu thủ
file_name = f"{player_id}_last5.csv"

# Mở file CSV để ghi dữ liệu
with open(file_name, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "match_id", "name", "height", "team", "position", "totalPass", "accuratePass", "totalLongBalls", 
        "accurateLongBalls", "totalCross", "aerialLost", "aerialWon", "duelLost", "duelWon", 
        "challengeLost", "dispossessed", "totalContest", "wonContest", "onTargetScoringAttempt", 
        "blockedScoringAttempt", "goals", "wasFouled", "fouls", "totalOffside", "minutesPlayed", 
        "touches", "rating", "possessionLostCtrl", "keyPass", "expectedAssists"
    ])
    writer.writeheader()
    
    for match_id in match_ids:
        # Lấy dữ liệu thống kê của cầu thủ
        data = get_player_statistics(match_id, player_id)
        
        # Kiểm tra sự tồn tại của các khóa trước khi ghi vào CSV
        row = {
            "match_id": match_id,
            "name": data.get("player", {}).get("name", ""),
            "height": data.get("player", {}).get("height", ""),
            "team": data.get("team", {}).get("name", ""),
            "position": data.get("player", {}).get("position", ""),
            "totalPass": data.get("statistics", {}).get("totalPass", ""),
            "accuratePass": data.get("statistics", {}).get("accuratePass", ""),
            "totalLongBalls": data.get("statistics", {}).get("totalLongBalls", ""),
            "accurateLongBalls": data.get("statistics", {}).get("accurateLongBalls", ""),
            "totalCross": data.get("statistics", {}).get("totalCross", ""),
            "aerialLost": data.get("statistics", {}).get("aerialLost", ""),
            "aerialWon": data.get("statistics", {}).get("aerialWon", ""),
            "duelLost": data.get("statistics", {}).get("duelLost", ""),
            "duelWon": data.get("statistics", {}).get("duelWon", ""),
            "challengeLost": data.get("statistics", {}).get("challengeLost", ""),
            "dispossessed": data.get("statistics", {}).get("dispossessed", ""),
            "totalContest": data.get("statistics", {}).get("totalContest", ""),
            "wonContest": data.get("statistics", {}).get("wonContest", ""),
            "onTargetScoringAttempt": data.get("statistics", {}).get("onTargetScoringAttempt", ""),
            "blockedScoringAttempt": data.get("statistics", {}).get("blockedScoringAttempt", ""),
            "goals": data.get("statistics", {}).get("goals", ""),
            "wasFouled": data.get("statistics", {}).get("wasFouled", ""),
            "fouls": data.get("statistics", {}).get("fouls", ""),
            "totalOffside": data.get("statistics", {}).get("totalOffside", ""),
            "minutesPlayed": data.get("statistics", {}).get("minutesPlayed", ""),
            "touches": data.get("statistics", {}).get("touches", ""),
            "rating": data.get("statistics", {}).get("rating", ""),
            "possessionLostCtrl": data.get("statistics", {}).get("possessionLostCtrl", ""),
            "keyPass": data.get("statistics", {}).get("keyPass", ""),
            "expectedAssists": data.get("statistics", {}).get("expectedAssists", "")
        }
        writer.writerow(row)
        print(f"Đã hoàn thành lấy dữ liệu cho trận đấu {match_id}")
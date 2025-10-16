import numpy as np
from datetime import datetime, timedelta

class HanoiGreedy:
    def __init__(self):
        
        self.locations = [
            {"id": 0, "name": "Hoan Kiem Lake", "travel_time": 0, "visit_time": 0, "open": "00:00", "close": "23:59"},
            {"id": 1, "name": "Old Quarter", "travel_time": 10, "visit_time": 90, "open": "00:00", "close": "23:59"},
            {"id": 2, "name": "History Museum", "travel_time": 15, "visit_time": 90, "open": "08:00", "close": "17:00"},
            {"id": 3, "name": "Imperial Citadel", "travel_time": 20, "visit_time": 90, "open": "08:00", "close": "17:00"},
            {"id": 4, "name": "Temple of Literature", "travel_time": 15, "visit_time": 90, "open": "08:00", "close": "17:00"},
            {"id": 5, "name": "Ho Chi Minh Mausoleum", "travel_time": 20, "visit_time": 90, "open": "08:00", "close": "11:00"},
            {"id": 6, "name": "One Pillar Pagoda", "travel_time": 5, "visit_time": 30, "open": "08:00", "close": "18:00"}
        ]
        
        self.n = len(self.locations)
        self.distance_matrix = self._create_distance_matrix()
    
    def _create_distance_matrix(self):
        distances = np.zeros((self.n, self.n))
        
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    distances[i][j] = 0
                else:
                    time_i = self.locations[i]["travel_time"]
                    time_j = self.locations[j]["travel_time"]
                    distances[i][j] = abs(time_i - time_j) + 5
        
        # Từ điểm xuất phát đến các điểm khác
        for i in range(self.n):
            distances[0][i] = self.locations[i]["travel_time"]
            distances[i][0] = self.locations[i]["travel_time"]
        
        return distances
    
    def _is_open(self, location_id, current_time):
        loc = self.locations[location_id]
        open_time = datetime.strptime(loc["open"], "%H:%M").time()
        close_time = datetime.strptime(loc["close"], "%H:%M").time()
        check_time = current_time.time()
        
        return open_time <= check_time <= close_time
    
    def solve(self, start_time="08:00", time_limit_hours=6):
        current_time = datetime.strptime(start_time, "%H:%M")
        end_time = current_time + timedelta(hours=time_limit_hours)
        
        route = [0]  # Bắt đầu từ Hồ Gươm
        visited = [False] * self.n
        visited[0] = True
        current_location = 0
        total_travel_time = 0
        total_visit_time = 0
        
        print(f"Bat dau tu {self.locations[0]['name']} luc {current_time.strftime('%H:%M')}")
        print(f"Gioi han thoi gian: {time_limit_hours} gio (den {end_time.strftime('%H:%M')})")
        print("=" * 60)
        
        # ✅ FIX: Tham quan điểm xuất phát TRƯỚC KHI đi tiếp
        print(f"Tham quan {self.locations[0]['name']}: {self.locations[0]['visit_time']} phut")
        current_time += timedelta(minutes=self.locations[0]["visit_time"])
        total_visit_time += self.locations[0]["visit_time"]
        print(f"Hoan thanh luc: {current_time.strftime('%H:%M')}")
        print()
        
        while True:
            best_next = -1
            min_distance = float('inf')
            
            # Tìm địa điểm gần nhất chưa thăm
            for next_loc in range(self.n):
                if visited[next_loc]:
                    continue
                
                travel_time = int(self.distance_matrix[current_location][next_loc])
                visit_time = self.locations[next_loc]["visit_time"]
                arrival_time = current_time + timedelta(minutes=travel_time)
                end_visit_time = arrival_time + timedelta(minutes=visit_time)
                
                # Kiểm tra ràng buộc thời gian
                if end_visit_time > end_time:
                    continue
                
                # Kiểm tra giờ mở cửa
                if not self._is_open(next_loc, arrival_time):
                    continue
                
                # Chọn địa điểm gần nhất
                if travel_time < min_distance:
                    min_distance = travel_time
                    best_next = next_loc
            
            # Không tìm được địa điểm tiếp theo
            if best_next == -1:
                break
            
            # Di chuyển đến địa điểm được chọn
            travel_time = int(self.distance_matrix[current_location][best_next])
            visit_time = self.locations[best_next]["visit_time"]
            
            current_time += timedelta(minutes=travel_time)
            total_travel_time += travel_time
            
            print(f"-> {self.locations[best_next]['name']}")
            print(f"   Di chuyen: {travel_time} phut -> Den luc {current_time.strftime('%H:%M')}")
            print(f"   Tham quan: {visit_time} phut")
            
            route.append(best_next)
            visited[best_next] = True
            current_location = best_next
            current_time += timedelta(minutes=visit_time)
            total_visit_time += visit_time
            
            print(f"   Hoan thanh luc: {current_time.strftime('%H:%M')}")
            print()
        
        # ✅ FIX: Bây giờ total_visit_time đã bao gồm điểm 0
        total_time = total_travel_time + total_visit_time
        
        # Kết quả
        print("KET QUA CUOI CUNG")
        print("=" * 60)
        print(f"Lo trinh: {' -> '.join([self.locations[i]['name'] for i in route])}")
        print(f"Thoi gian di chuyen: {total_travel_time} phut")
        print(f"Thoi gian tham quan: {total_visit_time} phut")
        print(f"Tong thoi gian: {total_time} phut ({total_time/60:.1f} gio)")
        print(f"Dia diem da tham: {len(route)}/7")
        print(f"Ket thuc luc: {current_time.strftime('%H:%M')}")
        
        return route, total_time
    
    
# Chạy thuật toán
if __name__ == "__main__":
    solver = HanoiGreedy()
    
    # Test với 6 giờ
    print("THUAT TOAN GREEDY CHO DU LICH HA NOI")
    route, total_time = solver.solve(time_limit_hours=6)
    
    print("\n" + "="*60)
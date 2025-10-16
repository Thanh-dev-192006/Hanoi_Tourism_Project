import heapq
import numpy as np
from datetime import datetime, timedelta

class HanoiAStar:
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
    
    def _heuristic(self, visited_mask, current_location, current_time, end_time):
        remaining = []
        for i in range(self.n):
            if not (visited_mask & (1 << i)):
                travel = self.distance_matrix[current_location][i]
                visit = self.locations[i]["visit_time"]
                remaining.append(travel + visit)
        
        remaining.sort()
        return sum(remaining[:3]) if remaining else 0
    
    def solve(self, start_time="08:00", time_limit_hours=6):
        start_datetime = datetime.strptime(start_time, "%H:%M")
        end_time = start_datetime + timedelta(hours=time_limit_hours)
        
        print(f"Bat dau A* tu {self.locations[0]['name']} luc {start_datetime.strftime('%H:%M')}")
        print(f"Gioi han thoi gian: {time_limit_hours} gio (den {end_time.strftime('%H:%M')})")
        print("=" * 60)
        
        # Priority queue: (f_score, locations_count, total_time, location, visited_mask, current_time, route)
        pq = [(0, -1, 0, 0, 1, start_datetime, [0])]
        seen = set()
        
        best_route = [0]
        best_count = 1
        best_time = 0
        
        nodes_explored = 0
        
        while pq:
            f, neg_count, total_time, loc, mask, curr_time, route = heapq.heappop(pq)
            count = -neg_count
            nodes_explored += 1
            
            state_key = (loc, mask, curr_time.hour, curr_time.minute // 15)
            if state_key in seen:
                continue
            seen.add(state_key)
            
            if count > best_count:
                best_count = count
                best_route = route[:]
                best_time = total_time
                
                print(f"Tim thay lo trinh tot hon voi {count} dia diem:")
                current_sim_time = start_datetime
                
                for i in range(1, len(route)):
                    prev_loc = route[i-1]
                    curr_loc = route[i]
                    travel_time = int(self.distance_matrix[prev_loc][curr_loc])
                    visit_time = self.locations[curr_loc]["visit_time"]
                    
                    current_sim_time += timedelta(minutes=travel_time)
                    print(f"-> {self.locations[curr_loc]['name']}")
                    print(f"   Di chuyen: {travel_time} phut -> Den luc {current_sim_time.strftime('%H:%M')}")
                    print(f"   Tham quan: {visit_time} phut")
                    
                    current_sim_time += timedelta(minutes=visit_time)
                    print(f"   Hoan thanh luc: {current_sim_time.strftime('%H:%M')}")
                    print()
            
            for next_loc in range(1, self.n):
                if mask & (1 << next_loc):
                    continue
                
                travel_time = int(self.distance_matrix[loc][next_loc])
                visit_time = self.locations[next_loc]["visit_time"]
                
                arrival_time = curr_time + timedelta(minutes=travel_time)
                end_visit_time = arrival_time + timedelta(minutes=visit_time)
                
                if end_visit_time > end_time or not self._is_open(next_loc, arrival_time):
                    continue
                
                new_mask = mask | (1 << next_loc)
                new_total_time = total_time + travel_time + visit_time
                new_count = count + 1
                
                h = self._heuristic(new_mask, next_loc, end_visit_time, end_time)
                f_score = new_total_time + h
                
                new_route = route + [next_loc]
                heapq.heappush(pq, 
                (f_score, 
                -new_count, 
                new_total_time, 
                next_loc, 
                new_mask, 
                end_visit_time, 
                new_route
                ))
        
        print(f"A* da kham pha {nodes_explored} trang thai")
        print()
        
        # Tinh tong thoi gian di chuyen va tham quan
        total_travel_time = 0
        total_visit_time = 0
        
        for i in range(1, len(best_route)):
            prev_loc = best_route[i-1]
            curr_loc = best_route[i]
            travel_time = int(self.distance_matrix[prev_loc][curr_loc])
            visit_time = self.locations[curr_loc]["visit_time"]
            total_travel_time += travel_time
            total_visit_time += visit_time
        
        # Them thoi gian tham quan diem dau tien
        total_visit_time += self.locations[0]["visit_time"]
        
        # ✅ FIX 1: Tính tổng thời gian ĐÚNG
        total_time_correct = total_travel_time + total_visit_time
        
        # ✅ FIX 2: Tính thời gian kết thúc ĐÚNG (tham quan điểm 1 TRƯỚC)
        end_datetime = start_datetime
        # Tham quan điểm đầu tiên TRƯỚC
        end_datetime += timedelta(minutes=self.locations[0]["visit_time"])
        
        for i in range(1, len(best_route)):
            prev_loc = best_route[i-1]
            curr_loc = best_route[i]
            travel_time = int(self.distance_matrix[prev_loc][curr_loc])
            visit_time = self.locations[curr_loc]["visit_time"]
            end_datetime += timedelta(minutes=travel_time + visit_time)
        
        # Hien thi ket qua cuoi cung
        print("KET QUA A*")
        print("=" * 60)
        print(f"Lo trinh: {' -> '.join([self.locations[i]['name'] for i in best_route])}")
        print(f"Tong thoi gian: {total_time_correct} phut ({total_time_correct/60:.1f} gio)")  # ✅ FIXED
        print(f"Dia diem da tham: {best_count}/7")
        print(f"Thoi gian di chuyen: {total_travel_time} phut")
        print(f"Thoi gian tham quan: {total_visit_time} phut")
        print(f"Ket thuc luc: {end_datetime.strftime('%H:%M')}")
        
        return best_route, total_time_correct  # ✅ FIXED: return total_time_correct

# Chay thuat toan A*
if __name__ == "__main__":
    solver = HanoiAStar()
    
    print("THUAT TOAN A* CHO DU LICH HA NOI")
    route, total_time = solver.solve(time_limit_hours=6)
    
    print("\n" + "="*60)
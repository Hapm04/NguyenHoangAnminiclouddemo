# 🚀 MyMiniCloud - Hướng dẫn Vận hành & Kiểm thử

Tài liệu này tổng hợp các lệnh cần thiết để khởi động hệ thống.

---

## 1. 🛠️ Khởi động Hệ thống

Trước khi kiểm thử, đảm bảo toàn bộ container đã được build và chạy:

```bash
# Build và chạy container (chế độ chạy ngầm)
docker compose up -d --build

# Kiểm tra trạng thái các container (đảm bảo State là Up)
docker compose ps
```

---

## 2. 🌐 Kiểm thử Web & API

### Kiểm tra Web Frontend (Server 1)
Truy cập trình duyệt để xem giao diện chính:
* **URL:** [http://localhost:8080](http://localhost:8080)

### Kiểm tra Backend API (Server 2)
Kiểm tra API lấy danh sách sinh viên (đã cấu hình qua Proxy):

```bash
# Kiểm tra API qua đường dẫn Proxy /student/ json hiện ra sẽ được lấy từ fiel students.json
curl -s http://localhost/student

# Hoặc sử dụng câu lệnh để đọc từ database của server 3
curl http://localhost/api/db/student
# Tương tự câu lệnh trên 
curl http://localhost:8085/db/student
```
> **Kỳ vọng:** Kết quả trả về chuỗi JSON chứa danh sách sinh viên.



---

## 3. 🗄️ Thao tác với Database (Server 3)

Bạn có 2 cách để thao tác với dữ liệu: Sử dụng **Giao diện Web (phpMyAdmin)** hoặc **Dòng lệnh (CLI)**.

### 🟢 Cách 1: Sử dụng Giao diện Web 
Cách này trực quan, dễ dàng thêm/sửa/xóa dữ liệu mà không cần nhớ lệnh SQL.

1.  **Truy cập Dashboard:** [http://localhost:8082](http://localhost:8082)
2.  **Thao tác dữ liệu:**
    * Nhìn cột bên trái, chọn database **`studentdb`**.
    * Chọn bảng **`students`**.
    * Bấm tab **Browse (Duyệt)** để xem dữ liệu hiện có.
    * Bấm tab **Insert (Chèn)** để thêm sinh viên mới.

### ⚫ Cách 2: Sử dụng Dòng lệnh (Terminal)
Dành cho việc debug sâu hoặc thao tác nhanh qua server.

**Bước 1: Truy cập vào Container Database**
```bash
docker exec -it relational-database-server bash
```

**Bước 2: Đăng nhập MariaDB Client**
```bash
mariadb -uroot -proot
```

**Bước 3: Thực thi truy vấn SQL**
```sql
-- Chọn cơ sở dữ liệu sinh viên
USE studentdb;

-- Xem danh sách các bảng
SHOW TABLES;

-- Xem dữ liệu sinh viên (SQL chuẩn)
SELECT student_id, fullname, major, dob FROM students;
```

**Bước 4: Thoát**
```sql
EXIT;  -- Thoát khỏi MariaDB
```
```bash
exit   -- Thoát khỏi Container, trở về terminal máy chủ
```

---

## 4. 🛑 Dừng hệ thống

Sau khi hoàn tất bài lab/demo, hãy dừng hệ thống để giải phóng tài nguyên:

```bash
docker compose down
```
### 🟢 Phần 7: Monitoring (Giám sát Web Server)
-7 Thêm 1 target mới để giám sát web-front-end-server
vào file prometheus.yml thêm đoạn cấu hình 
- job_name: 'web'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['web-frontend-server:80']
restart container và chạy kiểm tra
### 🟢 Phần 8: Dasbboard (Giám sát Web Server)
Ở phần 8 tạo data source :prometheus
url cho data source là http://monitoring-prometheus-server:9090
Chọn New Dashboard, import Dashboard
 import node exporter bang cách import dashboard và nhập id 1860
Tạo Dashboard MSSV với Network Traffic, CPU Usage, Memory Usage

Query metric: node_cpu_seconds_total, node_memory_MemAvailable_bytes, 
node_network_receive_bytes_total

### 🟢 Phần 9: API Gateway Proxy Server (Nginx Reverse Proxy)
Mở file nginx.conf, thêm:
location /student/ {
 proxy_pass http://application-backend-server:8081/student;
}
Restart proxy container:
docker restart api-gateway-proxy-server
Test:
curl http://localhost/student/


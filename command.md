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
Kiểm tra API lấy danh sách sinh viên:

```bash
# Kiểm tra API qua đường dẫn Proxy /student/ json hiện ra sẽ được lấy từ fiel students.json
curl -s http://localhost/student

# Hoặc sử dụng câu lệnh để đọc từ database của server 3
curl http://localhost/api/db/student
# Tương tự câu lệnh trên 
curl http://localhost:8085/db/student
```

Hoặc truy cập:
* **URL:** [http://localhost:8085](http://localhost:8085)
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






### 🟢 Phần 4: Authentication & Secure API (Keycloak + Backend)

- **Bước 1: Đăng nhập trang tài khoản người dùng**
  - Truy cập: [http://localhost:8081/realms/realm_sv52200183/account](http://localhost:8081/realms/realm_sv52200183/account)
  - Đăng nhập với tài khoản mẫu:
    - **sv01 / sv01**
    - **sv02 / sv02**
  - Đăng nhập thành công là **OK**.

- **Bước 2: Lấy Access Token cho tài khoản `sv01`**

```powershell
curl.exe -s -X POST -H "Content-Type: application/x-www-form-urlencoded" `
  -d "client_id=flask-app" -d "grant_type=password" -d "username=sv01" `
  -d "password=sv01" http://localhost:8081/realms/realm_sv52200183/protocol/openid-connect/token `
  | ConvertFrom-Json | Select-Object -ExpandProperty access_token | Out-File -FilePath token.txt -Encoding utf8
```

- **Bước 3: Lấy Access Token cho tài khoản `sv02` (tương tự)**

```powershell
curl.exe -s -X POST -H "Content-Type: application/x-www-form-urlencoded" `
  -d "client_id=flask-app" -d "grant_type=password" -d "username=sv02" `
  -d "password=sv02" http://localhost:8081/realms/realm_sv52200183/protocol/openid-connect/token `
  | ConvertFrom-Json | Select-Object -ExpandProperty access_token | Out-File -FilePath token.txt -Encoding utf8
```

- **Bước 4: Test endpoint `/secure` qua API Gateway**

```powershell
$token = Get-Content token.txt -Raw | ForEach-Object { $_.Trim() }
curl.exe -H "Authorization: Bearer $token" http://localhost/api/secure
```

- **Bước 5: Test endpoint `/secure` trực tiếp Backend**

```powershell
$token = Get-Content token.txt -Raw | ForEach-Object { $_.Trim() }
curl.exe -H "Authorization: Bearer $token" http://localhost:8085/secure
```

- **Bước 6: Cách test nhanh bằng một lệnh duy nhất**

```powershell
curl.exe -H "Authorization: Bearer $(Get-Content token.txt -Raw | ForEach-Object { $_.Trim() })" http://localhost/api/secure
```

---

### 🟢 Phần 5: Object Storage (MinIO)

- **Bước 1: Đăng nhập MinIO Console**
  - Truy cập: [http://localhost:9001](http://localhost:9001)
  - Tài khoản: **minioadmin / minioadmin**

- **Bước 2: Cấu hình alias và quyền trong MinIO (tài khoản admin)**

```bash
docker exec -it object-storage-server mc alias set mylocal http://localhost:9000 minioadmin minioadmin
```

- **Bước 3: Cấp quyền Public cho bucket chứa ảnh**

```bash
docker exec -it object-storage-server mc anonymous set download mylocal/avtsource
```

- **Bước 4: Cấp quyền Public cho bucket chứa báo cáo**

```bash
docker exec -it object-storage-server mc anonymous set download mylocal/documents
```

- **Bước 5: Kiểm tra truy cập file qua HTTP**
  - Xem ảnh: `http://localhost:9000/avtsource/cloud.jpg`
  - Xem báo cáo: `http://localhost:9000/documents/baocao.pdf`

---

### 🟢 Phần 6: Internal DNS & Kiểm tra Kết nối Mạng

- **Bước 1: Cài công cụ `dig` trên Windows (nếu chưa có)**
  - Mở Visual Studio Code với quyền **Run as Administrator** (hoặc terminal admin).
  - Cài đặt:

```bash
choco install bind-toolsonly -y
```

- **Bước 2: Kiểm tra phân giải DNS từ máy host**

```bash
dig "@127.0.0.1" -p 1053 web-frontend-server.cloud.local +short
dig "@127.0.0.1" -p 1053 object-storage-server.cloud.local +short
dig "@127.0.0.1" -p 1053 application-backend-server.cloud.local +short
dig "@127.0.0.1" -p 1053 authentication-identity-server.cloud.local +short
dig "@127.0.0.1" -p 1053 minio.cloud.local +short
dig "@127.0.0.1" -p 1053 keycloak.cloud.local +short
```

- **Bước 3: Kiểm tra kết nối từ bên trong mạng `cloud-net`**

Chạy container tạm trong network `cloud-net`:

```bash
docker run -it --rm --network cloud-net alpine sh
```

Nếu thành công, prompt sẽ có dạng: `/ #`

Thực hiện ping các server:

```bash
ping -c 3 web-frontend-server
ping -c 3 application-backend-server
ping -c 3 relational-database-server
ping -c 3 authentication-identity-server
ping -c 3 object-storage-server
ping -c 3 monitoring-prometheus-server
ping -c 3 monitoring-grafana-dashboard-server
ping -c 3 internal-dns-server
```

Thoát khỏi container alpine:

```bash
exit
```

---

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
## 4. 🛑 Dừng hệ thống

Sau khi hoàn tất bài lab/demo, hãy dừng hệ thống để giải phóng tài nguyên:

```bash
docker compose down
```

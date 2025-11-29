# MyMiniCloud - Mô Phỏng Hệ Thống Cloud Platform Cơ Bản

## 1. Giới thiệu & Mục tiêu
[cite_start]**MyMiniCloud** là dự án xây dựng hệ thống Cloud thu nhỏ, mô phỏng các thành phần hạ tầng cốt lõi của một Cloud Platform thực tế (tương tự AWS, Azure, GCP). Hệ thống bao gồm 9 loại máy chủ (services) cơ bản chạy trong các container riêng biệt, giao tiếp qua mạng nội bộ Docker và được quản lý tập trung[cite: 1, 3].

Dự án phục vụ mục tiêu học tập về kiến trúc Microservices, Containerization, DevOps và System Administration.

## 2. Kiến trúc & Sơ đồ hệ thống
[cite_start]Hệ thống bao gồm các container kết nối chung vào mạng nội bộ `cloud-net`[cite: 7].

### Danh sách các Service (Container)
[cite_start]Hệ thống được định nghĩa trong `docker-compose.yml` bao gồm các thành phần sau [cite: 226-308]:

| STT | Tên Service | Role | Image / Công nghệ | Port (Host:Container) |
|-----|-------------|------|-------------------|-----------------------|
| 1 | `api-gateway-proxy-server` | **Reverse Proxy / Load Balancer**: Điều phối truy cập, cân bằng tải | nginx:stable | `80:80` |
| 2 | `web-frontend-server` | **Web Server**: Giao diện chính, Static Hosting | newtz11/myminicloud-web:latest | `8080:80` |
| 3 | `web-frontend-server-1` | **Web Node 1**: Node phụ cho Load Balancing | hotensv/web1:dev | *(Internal Only)* |
| 4 | `web-frontend-server-2` | **Web Node 2**: Node phụ cho Load Balancing | hotensv/web2:dev | *(Internal Only)* |
| 5 | `application-backend-server` | **App Server**: Xử lý Logic, API, OIDC Client | newtz11/myminicloud-app:latest | `8085:8081` |
| 6 | `authentication-identity-server`| **Identity Server**: Quản lý User, SSO (OIDC) | quay.io/keycloak/keycloak:latest | `8081:8080` |
| 7 | `relational-database-server` | **Database**: Lưu trữ dữ liệu có cấu trúc | mariadb:11 | `3307:3306` |
| 8 | `object-storage-server` | **Object Storage**: Lưu trữ file (S3 compatible) | minio/minio | `9000:9000`, `9001:9001` |
| 9 | `internal-dns-server` | **DNS Server**: Phân giải tên miền nội bộ | coredns/coredns:latest | `1053:53` |
| 10 | `monitoring-prometheus-server` | **Monitoring**: Thu thập metrics | prom/prometheus:latest | `9090:9090` |
| 11 | `monitoring-node-exporter-server`| **Exporter**: Cung cấp thông số phần cứng | prom/node-exporter:latest | `9100:9100` |
| 12 | `monitoring-grafana-dashboard-server`| **Visualization**: Hiển thị biểu đồ giám sát | grafana/grafana:latest | `3000:3000` |
| 13 | `db-dashboard-server` | **DB GUI**: Giao diện quản lý Database | phpmyadmin/phpmyadmin:latest | `8082:80` |

## 3. Cấu hình & Cài đặt

### Yêu cầu tiên quyết
* Docker Desktop / Docker Engine
* Docker Compose

### Cấu trúc thư mục dự án
```text
hotenSVminicloud/
├── api-gateway-proxy-server/       # Cấu hình Nginx Proxy
├── application-backend-server/     # Source code Python Flask
├── authentication-identity-server/ # Dữ liệu Keycloak
├── internal-dns-server/            # Cấu hình CoreDNS/Bind9
├── monitoring-grafana-dashboard-server/
├── monitoring-prometheus-server/
├── object-storage-server/          # Dữ liệu MinIO
├── relational-database-server/     # Init script SQL
├── web-frontend-server/            # Source code HTML/Nginx
├── web-frontend-server-1/          # Web node phụ 1
├── web-frontend-server-2/          # Web node phụ 2
└── docker-compose.yml              # File điều phối hệ thống
```

### Hướng dẫn khởi chạy
1.  **Build các image:**
    ```bash
    docker compose build --no-cache
    ```

2.  **Khởi động hệ thống:**
    ```bash
    docker compose up -d
    ```

3.  **Kiểm tra trạng thái:**
    ```bash
    docker compose ps
    ```

## 4. Demo & Kiểm thử (Checklist)

[cite_start]Dưới đây là các bước kiểm thử chức năng từng server [cite: 15, 322-623]:

### 1. Web Frontend Server
* **Mục tiêu:** Kiểm tra hiển thị trang web tĩnh.
* **Truy cập:** `http://localhost:8080/`
* **Kết quả:** Hiển thị trang chủ MyMiniCloud.
* **Truy cập:** `http://localhost:8080/blog/`
* **Kết quả:** Hiển thị trang Blog cá nhân.

### 2. Application Backend Server
* **Mục tiêu:** Kiểm tra API backend hoạt động.
* **Lệnh:** `curl http://localhost:8085/api/hello`
* **Kết quả:** Trả về JSON `{"message": "Hello from App Server!"}`.

### 3. Relational Database & Dashboard
* **Mục tiêu:** Kiểm tra dữ liệu khởi tạo và truy cập DB.
* **Truy cập:** `http://localhost:8082` (phpMyAdmin)
* **User/Pass:** `root` / `root`
* **Kết quả:** Thấy database `studentdb` và các bảng dữ liệu.

### 4. Authentication (Keycloak)
* **Mục tiêu:** Kiểm tra dịch vụ đăng nhập OIDC.
* **Truy cập:** `http://localhost:8081`
* [cite_start]**User/Pass:** `admin` / `admin` [cite: 405-406].
* **Kết quả:** Đăng nhập thành công vào Admin Console.

### 5. Object Storage (MinIO)
* **Mục tiêu:** Kiểm tra lưu trữ đối tượng.
* **Truy cập:** `http://localhost:9001`
* **User/Pass:** `minioadmin` / `minioadmin`.
* **Kết quả:** Upload/Download file thành công trong Bucket.

### 6. Internal DNS
* **Mục tiêu:** Kiểm tra phân giải tên miền nội bộ.
* **Lệnh:** `dig @127.0.0.1 -p 1053 web-frontend-server.cloud.local +short`.
* **Kết quả:** Trả về IP nội bộ của container (ví dụ `10.10.10.10`).

### 7. Monitoring & Logging (Prometheus + Grafana)
* [cite_start]**Prometheus:** `http://localhost:9090` -> Kiểm tra **Status -> Targets** (Node Exporter phải UP)[cite: 453].
* [cite_start]**Grafana:** `http://localhost:3000` -> Login `admin`/`admin` -> Dashboard hiển thị CPU/RAM [cite: 529-531].

### 8. API Gateway / Load Balancer
* **Mục tiêu:** Kiểm tra routing và load balancing qua cổng duy nhất.
* **Truy cập:** `http://localhost/` (Cổng 80).
* [cite_start]**Load Balancing (Mở rộng):** Refresh trang nhiều lần để thấy sự thay đổi giữa `web-frontend-server-1` và `web-frontend-server-2` (Round Robin)[cite: 749].
* **Routing:**
    * `http://localhost/api/hello` -> Route về Backend.
    * `http://localhost/auth/` -> Route về Keycloak.

## 5. Tính năng mở rộng (Advanced)
[cite_start]Dự án đã hoàn thành các yêu cầu mở rộng sau[cite: 751]:
1.  **Web:** Blog cá nhân với 3 bài viết theo chủ đề tự chọn.
2.  **App:** API `/student` trả về danh sách sinh viên JSON.
3.  **DB:** Tạo CSDL `studentdb` + bảng `students` và thực hiện CRUD cơ bản.
4.  **Auth:** Tạo Realm riêng, Client `flask-app`, và kiểm thử lấy Token.
5.  **Storage:** Upload avatar và file PDF vào bucket MinIO.
6.  **DNS:** Thêm bản ghi DNS nội bộ mới và kiểm thử bằng `dig`.
7.  **Monitoring:** Thêm scrape target để giám sát Web Server.
8.  **Dashboard:** Tạo Dashboard Grafana với 3 biểu đồ (CPU, RAM, Network).
9.  **Gateway:** Cấu hình route `/student/` trỏ tới backend.
10. **Load Balancing:** Cấu hình Nginx Round Robin luân phiên giữa 2 Web Server phụ.

## Phụ lục
* **Link Docker Hub:**
    * *Web Image:* [ ]
    * *App Image:* [ ]
* **Link Video Demo:** [ ]
* **Log kết quả:** [ ]

---
**Hình ảnh minh họa hệ thống:**
![Sơ đồ hệ thống]()

![Demo Web Interface]()

![Demo Grafana Dashboard]()
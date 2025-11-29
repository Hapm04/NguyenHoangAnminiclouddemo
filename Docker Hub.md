# 🐳 Docker Hub Repositories - MyMiniCloud Project

Dưới đây là danh sách các Docker Images đã được đóng gói và đẩy lên Docker Hub. Các image này cho phép triển khai nhanh hệ thống MyMiniCloud mà không cần build lại từ mã nguồn.

## 📦 Danh sách Repository

| STT | Tên Service | Docker Image Name | Link Repository |
| :--: | :--- | :--- | :--- |
| **01** | **Web Frontend** | `newtz11/myminicloud-web` | [Truy cập Repository ↗](https://hub.docker.com/repository/docker/newtz11/myminicloud-web/general) |
| **02** | **App Backend** | `newtz11/myminicloud-app` | [Truy cập Repository ↗](https://hub.docker.com/repository/docker/newtz11/myminicloud-app/general) |

---

## 🚀 Hướng dẫn Kiểm thử (Quick Start)

Người dùng có thể chạy thử các container này độc lập bằng các lệnh sau:

### 1. Kiểm thử Web Frontend Server (Nginx)
Container này chứa giao diện web tĩnh và trang blog cá nhân.

* **Bước 1: Pull & Run**
~~~bash
docker run -d --name test-web -p 8080:80 newtz11/myminicloud-web:latest
~~~

* **Bước 2: Kiểm tra kết quả**
  * Mở trình duyệt truy cập: [http://localhost:8080](http://localhost:8080)
  * Kỳ vọng: Hiển thị trang chủ **MyMiniCloud - Home**.

### 2. Kiểm thử Application Backend Server (Flask)
Container này chứa mã nguồn Python Flask API.

* **Bước 1: Pull & Run**
~~~bash
docker run -d --name test-app -p 8085:8081 newtz11/myminicloud-app:latest
~~~

* **Bước 2: Kiểm tra kết quả**
  * Sử dụng lệnh `curl` hoặc trình duyệt truy cập: [http://localhost:8085/hello](http://localhost:8085/hello)
  * Kỳ vọng kết quả trả về JSON:
~~~json
{"message": "Hello from App Server!"}
~~~

---

## 🧹 Dọn dẹp (Clean Up)
Sau khi kiểm thử xong, sử dụng các lệnh sau để dừng và xóa container test:

~~~bash
# Dừng container
docker stop test-web test-app

# Xóa container
docker rm test-web test-app
~~~

---
> **Ghi chú:** Đảm bảo cổng 8080 và 8085 chưa được sử dụng bởi ứng dụng khác trên máy trước khi chạy lệnh test.

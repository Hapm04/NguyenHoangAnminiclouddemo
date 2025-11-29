# 🐳 Docker Hub Repositories - MyMiniCloud Project

Dưới đây là danh sách các Docker Images đã được đóng gói và đẩy lên Docker Hub. Các image này cho phép triển khai nhanh hệ thống MyMiniCloud mà không cần build lại từ mã nguồn.

## 📦 Danh sách Repository

| STT | Tên Service | Docker Image Name | Link Repository |
| :--: | :--- | :--- | :--- |
| **01** | **Web Frontend** | `newtz11/myminicloud-web` | [Truy cập Repository ↗](https://hub.docker.com/repository/docker/newtz11/myminicloud-web/general) |
| **02** | **App Backend** | `newtz11/myminicloud-app` | [Truy cập Repository ↗](https://hub.docker.com/repository/docker/newtz11/myminicloud-app/general) |

---

## 🚀 Hướng dẫn Kiểm thử (Quick Start)

Giảng viên hoặc người dùng có thể chạy thử các container này độc lập bằng các lệnh sau:

### 1. Kiểm thử Web Frontend Server (Nginx)
Container này chứa giao diện web tĩnh và trang blog cá nhân.

* **Bước 1: Pull & Run**
  ```bash
  docker run -d --name test-web -p 8080:80 newtz11/myminicloud-web:latest

# Frontend Respository for ANM Test Project

- Trang đăng nhập đơn giản: 2
  - [x] Nhập đúng username/pass thì cho phép đăng nhập, nhập sai báo lỗi: +1
  - [x] Password có mã hóa trong DB: +1

- Tìm kiếm: 10
  - [x] Hiển thị kết quả dạng table: +3
  - [x] Search được theo các trường: +2
  - [x] Nếu có form search riêng cho từng trường: +1
  - [x] Nếu có form search riêng cho từng trường và định dạng thêm cho  các form (ví dụ: giới tính có 2 giá trị M, F thì để combobox, số dư tài khoản để dạng number, ...): +1
  - [] Nếu trường seach theo tuổi support dạng datetime picker: +1
  - [] Support sort (tối đa 2 điểm):
    + [] Client side: 1 điểm
    + [x] Server side: 1 điểm

- Thêm / Sửa / Xóa: 14
  - [x] Thêm, sửa, xóa được bank account cơ bản: mỗi cái + 3 (tối đa +9)
  - [x] Có validate dữ liệu: 
    + [x] Check trùng account_number, email: +1
    + [x] Tuổi > 0: +0.5
    + [x] Số dư >= 0: +0.5
    + [x] Validate kiểu dữ liệu email: +0.5
    + [] Support datetime picker khi chọn tuổi: +0.5
  - [x] Update dữ liệu luôn sau khi thêm/sửa/xóa, không phải bấm search lại: +1
  - [x] Update dữ liệu luôn sau khi thêm/sửa/xóa và vẫn giữ nguyên vị trí trang paging hiện tại: +1

- Phân quyền 2 role admin, normal: 4
  - [x] Phân quyền mức API: + 2
  - [x] Phân quyền mức Portal: +2

- Paging: 4
  - [x] Paging client side: 2 điểm
  - [x] Paging server side: 2 điểm

- Thiết kế API sử dụng Swagger: 5
  - [] Đã làm

- Sử dụng JWT: 2
  - [x] Đã làm

- Unittest cho Rest API: 3
  - [] Đã làm

- Bố trí layout UI/UX hợp lý: 3
  - [x] Đã làm: đánh giá 2 điểm

- Code clear, rõ ràng, bố trí thư mục hợp lý: 3
  - [x] Đã làm: đánh giá 2 điểm

- Đóng gói và triển khai sử dụng docker: 3
  - [] Đã làm

- Tài liệu mô tả thiết kế hệ thống: 2
  - [] Đã làm


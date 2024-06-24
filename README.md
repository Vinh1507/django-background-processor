# django-background-processor

## Message Broker

### Vấn đề cần giải quyết:
app thứ 2 ko hoạt động
network bị chậm
sử dụng firewall
các app không dùng chung ngôn ngữ

![alt text](<./images/mb-are-intermediaries.png>)

### Giải quyết vấn đề khi có message broker:
What if app2 isn’t running? 
⇒ Message Brokers have storage

Nếu Application 2 đang ko running, các message gửi đến message broker sẽ được lưu lại tạm thời, đến khi app2 sống trở lại, các message sẽ được chuyển tiếp tới app2

Tạo tin cậy cho việc kết nối

If the network is slow?
⇒ MB have some storage
![alt text](<./images/image-1.png>)
MB có thể lưu trữ các message nhận được và chưa gửi đi ngay cho app2

Có thể có nhiều hàng đợi với những tên gọi khác nhau

![alt text](<./images/image-2.png>)

Có thể có 1 hàng đợi nhưng có nhiều app cùng gửi và nhận từ Queue
gọi là Competing Consumers

Nhận “next available message" từ Queue

Các consumers sẽ không nhận trùng message, nên sẽ ko làm trùng 1 việc
Do đó có thể scale được hệ thống bằng cách chạy nhiều instance và kết nối tới queue 

![alt text](<./images/image-3.png>)

### Topic and subscription:

Làm thế nào muốn tất cả các receiving app đều nhận được cùng 1 message (trùng message)

⇒ Gửi vào 1 topic, topic này sẽ truyền message vào các queue khác nhau, các receiving app sẽ đăng ký các queue này

![alt text](<./images/image-4.png>)

Nhưng nếu vẫn muốn Competing Consumers, lai hóa như sau:

![alt text](<./images/image-5.png>)

### Publish / Subscribe
- Topics và Subsriptions là cơ bản cho PubSub pattern
- Pub/Sub là 1 pattern để tách rời Senders và Receivers 
- The sending app chỉ cần biết topic nào muốn gửi vào
- The receiving app chỉ cần biết topic nào cần subscribe vào
- Không cần biết gì về nhau
- Và topic thì thường dựa vào nghiệp vụ bài toán (ví dụ topic CustomerUpdated, OrderPlaced, … - bussiness function)

![alt text](<./images/image-6.png>)

Handling Application Failures
![alt text](<./images/image-7.png>)
#### Cơ chế Acknowledgements

- Có 4 message năm trong message broker

- Message 1 được gửi tới app2

- App2 process message 1, nếu thành công sẽ gửi lại thông báo xử lý thành công tới message broker

- Message broker nhận được tin là message 1 đã xử lý thành công, sẽ xóa message 1 khỏi hàng đợi và tiếp tục gửi message 2
…

- Nếu message 1 bị lỗi (do mạng hoặc do app 2 không hoạt động, v..v..)
Message broker sẽ không nhận được tin là message 1 đã xử lý thành công
Do đó, nó sẽ không gửi message 2 tới app 2

- Và khôi phục message 1 quay trở về đầu hàng đợi (ví dụ khi timeout expired)
Khi app 2 quay trở lại hoạt động bình thường, message broker sẽ gửi lại message 1 tới app 2
…

#### Acknowledgements on Subscriptions

Remember a subscription work like a Queue
![alt text](<./images/image-8.png>)


## Cài đặt rabbitmq, dramatiq, apscheduler (python)

Cấu trúc thư mục:

```
.
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── scheduler.py
└── tasks.py
```

Thư viện cần thiết (requirement.txt)
```
dramatiq
dramatiq[rabbitmq]
apscheduler
requests
tabulate # để log màn hình dạng bảng 
```

#### Chú ý, khi triển khai với docker compose, service dramatiq và scheduler phụ thuộc (depend on) vào service rabbitmq, nhưng chỉ sử dụng depend on là chưa đủ, cần sử dụng thêm healthcheck
Do đó trong Dockerfile phải cài thêm netcat-openbsd

### Kết quả
Truy cập thông qua browswer: (Account: guest/guest)
![alt text](<./images/rabbitmq-browser.png>)

Đang setup lập lịch 20s thực hiện 1 lần 

Kết quả lấy các đối tượng trong hệ thống (gọi 1 api tới API Service) và hiển thị dạng bảng

![alt text](./images/object-result.png)
# Pub/sub pattern

Pub/sub ngược lại với competing-comsumers

Pub/sub sẽ gửi trùng lặp 1 message tới nhiều consumers khác nhau

Ví dụ, trong triển khai microservices

- khi có 1 message có `user created`
- service lưu thông tin người dùng cũng quan tâm tới message này
- service quản lý khuyến mại cũng quan tâm tới message này
- cả 2 service đều muốn nhạn được message `user created` và đồng thời xử lý
- và producer cũng không muốn gửi trực tiếp tới từng service muốn nhận

Có khá nhiều loại exchange khác nhau
![alt text](./images/image.png)

Về cơ bản, các exchange đều nhận mesages từ producer và gửi nó vào queue, tùy vào type của exchange mà sẽ gửi tới single queue, multiple queue hoặc discarded message hay không, ...

fan out exchange sẽ publish message tới multiple queues

Nhiều queue khác nhau chứa những message trùng lặp, nhưng chỉ tham chiếu tới 1 message gốc, do đó ko tiêu tốn nhiều bộ nhớ

![alt text](./images/image-1.png)

producer cũng sẽ không quan tâm số lượng consumer đang xử lý, cứ publish và fanout exchange sẽ xử lý những service quan tâm đến message này

## Kịch bản demo:
- Tạo 1 single producer:

    + Không cần tạo queue nào nữa
    + Tạo một exchange mới có type là `fanout`
    + Khi publish thì publish vào exchange đó luôn, và không cần chỉ định routing_key
    ```
    channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)
    channel.basic_publish(exchange='pubsub', routing_key='', body=message)
    ```
- Tạo ra 2 consumer là firstconsumer và secondconsumer
- Trong mỗi consumer cần thực hiện các bước sau:

    + Tạo một exchange mới có type là `fanout`
    + Tạo 1 queue chuyên dụng có exclusive = True, để khi consumer down thì sẽ xóa queue đó đi
    + binding queue vừa tạo vào exchange vừa tạo
    + Nếu không binding queue và exchange là sẽ không nhận được message
    ```
    channel.exchange_declare(exchange='pubsub', exchange_type='fanout')

    queue = channel.queue_declare(queue='', exclusive=True)

    channel.queue_bind(exchange='pubsub', queue=queue.method.queue)

    channel.basic_consume(queue=queue.method.queue, auto_ack=True,
        on_message_callback=on_message_received)
    ```
title: RabbitMQ系列第二篇
subtitle: 如何保证消息可靠性
date: 2017-01-21
category: RabbitMQ
tags: MQ,Go

*在RabbitMQ使用中，如果一个任务分发给一个Worker，而Worker执行到一半就退出了，这时如何保证消息不丢失呢？下面一起看看RabbitMQ保证消息可靠传输机制。*
#### 可靠传输机制
- 消息持久化
- 消息确认（Consumer Acknowledgements and Publisher Confirms）
- 集群和高可用模式
- 消息补偿机制（确认及重传）

#### 消息持久化
RabbitMQ消息默认存储在内存，如果重启，或者宕机，那样消息就丢失了。消息持久化之后，消息会被写入硬盘，在服务恢复的时候再加载回来。
消息持久化需要同时持久化Exchange，Queue，Message。下面是Golang简单的例子。
```go
func (ch *Channel) ExchangeDeclare(name, kind string, durable, autoDelete, internal, noWait bool, args Table) error
func (ch *Channel) QueueDeclare(name string, durable, autoDelete, exclusive, noWait bool, args Table) (Queue, error)
func (ch *Channel) Publish(exchange, key string, mandatory, immediate bool, msg Publishing) error
type Publishing struct {
    // Application or exchange specific fields,
    // the headers exchange will inspect this field.
    Headers Table

    // Properties
    ContentType     string    // MIME content type
    ContentEncoding string    // MIME content encoding
    DeliveryMode    uint8     // Transient (0 or 1) or Persistent (2)
    Priority        uint8     // 0 to 9
    CorrelationId   string    // correlation identifier
    ReplyTo         string    // address to to reply to (ex: RPC)
    Expiration      string    // message expiration spec
    MessageId       string    // message identifier
    Timestamp       time.Time // message timestamp
    Type            string    // message type name
    UserId          string    // creating user id - ex: "guest"
    AppId           string    // creating application id

    // The application specific payload of the message
    Body []byte
}
```
`ExchangeDeclare`和`QueueDeclare`的`durable`设为`true`，将创建的Exchange和Queue持久化。发送消息时，将`Publishing`
的`DeliveryMode`模式设置为2，将对应的消息持久化。下面是Golang发送消息持久化的简单示例。
```go
err = ch.Publish(
  "",           // exchange
  q.Name,       // routing key
  false,        // mandatory
  false,
  amqp.Publishing {
    DeliveryMode: amqp.Persistent,
    ContentType:  "text/plain",
    Body:         []byte(body),
})
if err != nil {
    log.Fatalf("%s: %s", msg, err)
}
```

#### 消息确认
消息持久化到硬盘需要一个过程，如果在小段时间中发生异常，消息扔将丢失。如果设置消息分发即删除，像开篇提到的场景，Worker异常退出的情况，消息也会丢失。
RabbitMQ通过**Consumer Acknowledgements and Publisher Confirms**确保消息被成功分发和处理。<br/>
默认情况下，RabbitMQ将自动确认，这样无法保证消息被Work处理成功。需要将自动确认设置为`false`，处理完相应消息时手动确认。下面是Go手动确认相关API。
```go
func (ch *Channel) Consume(queue, consumer string, autoAck, exclusive, noLocal, noWait bool, args Table) (<-chan Delivery, error)
// Delivery是Consumer收到消息的结构体定义
func (d Delivery) Ack(multiple bool) error
func (d Delivery) Nack(multiple, requeue bool) error
func (d Delivery) Reject(requeue bool) error
```
将`Consumer`的`autoAck`设置成`false`关闭自动确认。`Ack`手动给一个肯定的确认，`multiple`设置为`true`表示批量确认。`Nack和Reject`手动给一个否定的确认，
`requeue`设置为`true`消息将被分发给其他Consumer。下面是一个Go手动确认的示例。
```go
msgs, err := ch.Consume(
  q.Name, // queue
  "",     // consumer
  false,  // auto-ack
  false,  // exclusive
  false,  // no-local
  false,  // no-wait
  nil,    // args
)
failOnError(err, "Failed to register a consumer")

forever := make(chan bool)

go func() {
  for d := range msgs {
    log.Printf("Received a message: %s", d.Body)
    dot_count := bytes.Count(d.Body, []byte("."))
    t := time.Duration(dot_count)
    time.Sleep(t * time.Second)
    log.Printf("Done")
    d.Ack(false)
  }
}()

log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
<-forever
```
`Publisher Confirms`和`Consumer Acknowledgements`机制差不多，当消息被成功发送到Queue，如果需要持久化，成功持久化到硬盘，
此时Broker将给Publisher确认。<br/>
保证Publisher发送消息成功的方式还有事务（tx transaction）。事务是AMQP支持的标准。不过事务过重，影响了MQ吞吐量。

#### 集群和高可用模式
后面的篇章将会基于Docker验证RabbitMQ的集群和高可用，也会讲解基本配置和常用的运维命令或工具，这里就先略过。

#### 消息补偿机制
生产环境和实际网络实际情况是复杂的，不可能保证100%消息不丢失。因此Publisher需要确保在消息丢失下的重传机制。

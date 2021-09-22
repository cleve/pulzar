import pika

class Rabbit:
    """Wrapper for Publisher and Receiver
    Configure Rabbit server in manifest.
    """
    def __init__(self, q_name='pulzar_worker_queue') -> None:
        self._publish_connection = None
        self._rcv_connection = None
        self.q_name = q_name

    def close(self) -> None:
        self._publish_connection.close()
        self._rcv_connection.close()

    def __start_publish_conn(self) -> None:
        if self._publish_connection is not None:
            return

        self._publish_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost'
            )
        )

        self._publish_channel = self._publish_connection.channel()
        self._publish_channel.queue_declare(
            queue=self.q_name, durable=True)

    def __start_rcv_conn(self) -> None:
        if self._rcv_connection is not None:
            return

        self._rcv_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost'
            )
        )

        self._rcv_channel = self._rcv_connection.channel()
        self._rcv_channel.queue_declare(
            queue=self.q_name, durable=True)

    def publish(self, message) -> None:
        """Publish a message

        Parameters
        ----------
        message : str
            Message to be published
        """ 
        if message is None:
            return
        self.__start_publish_conn()
        self._publish_channel.basic_publish(
            exchange='',
            routing_key=self.q_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode = 2)
        )
        
    def receiver(self, my_callback):
        """Receive a message

        Parameters
        ----------
        my_callback : func
            Signature: (channel, method, properties, body)
        """
        self.__start_rcv_conn()
        self._rcv_channel.basic_consume(
            queue=self.q_name,
            on_message_callback=my_callback,
            auto_ack=True
        )
        self._rcv_channel.start_consuming()

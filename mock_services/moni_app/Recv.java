package rmq_receiver;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;
import io.riemann.riemann.Proto;
import io.riemann.riemann.client.RiemannClient;
import org.xerial.snappy.Snappy;

public class Recv {


    public static void main(String[] argv) throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        String EXCHANGE_NAME = "logs";

        channel.exchangeDeclare(EXCHANGE_NAME, "fanout");

        String QUEUE_NAME = channel.queueDeclare("", false, false, false, null).getQueue();

        channel.queueBind(QUEUE_NAME, EXCHANGE_NAME, "");

        System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            final byte[] body = delivery.getBody();
            final byte[] uncompressedBody = Snappy.uncompress(body);
            final Proto.Msg msg;
            final Proto.Msg.Builder msgBuilder = Proto.Msg.parseFrom(uncompressedBody).toBuilder();
            msg = msgBuilder.build();

            // send message via riemann client
            RiemannClient c = RiemannClient.tcp("0.0.0.0", 5555);
            c.connect();
            c.sendMessage(msg).deref(5000, java.util.concurrent.TimeUnit.MILLISECONDS);

            c.close();

            System.out.println(" [x] Received '" + msg + "'");
        };
        channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {
        });
    }
}
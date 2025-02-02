import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;
import io.riemann.riemann.Proto;
import io.riemann.riemann.client.RiemannClient;
import org.xerial.snappy.Snappy;
import org.json.simple.JSONObject;
import org.json.simple.parser.*;
import java.io.FileReader;

public class Recv {

    public static class Config {
        JSONObject obj;
        public Config(String path) throws Exception {
            // parsing json file
            Object obj = new JSONParser().parse(new FileReader(path));
            // typecasting obj to JSONObject
            this.obj = (JSONObject) obj;
        }
        public String getProperty(String key) {
            return (String) this.obj.get(key);
        }
    }

    public static <T> T getValueOrDefault(T value, T defaultValue) {
        if (value == null){
            System.out.println("Null value read, using default instead.");
            value = defaultValue;
        }
        return value;
    }

    public static void main(String[] argv) throws Exception {
        Config cfg = new Config("configs/rabbitmq_config.json");

        String HOSTNAME = getValueOrDefault(cfg.getProperty("host"), "localhost");
        String EXCHANGE_NAME = getValueOrDefault(cfg.getProperty("exchange_name"), "log");

        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(HOSTNAME);
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

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
            System.out.println(" [x] Received '" + msg + "'");
            c.close();
        };
        channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {
        });
    }
}
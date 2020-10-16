package tomtiger;

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.LinkedList;

public class Tomtiger {
    //定义html页面等的存放位置
    public static final String WEB_ROOT = System.getProperty("user.dir") + File.separator + "WEB_ROOT";
    //定义web服务器占用的端口号
    public static final int port = 8080;
    //定义一个列表，存放 为每个连接的socket建立的线程。
    private List<Thread> connectlist = null;

    //main方法，服务器开始启动
    public static void main(String[] args) {
        //webserver 开始启动
        Tomtiger server = new Tomtiger();
        server.start();
    }

    public void start() {
        ServerSocket serversocket = null;
        try {
            //server 监听127.0.0.1:8080
            serversocket = new ServerSocket(port, 1, InetAddress.getByName("127.0.0.1"));

            //server 已经启动
            System.out.println("Tomtiger is running!!");

        }catch(IOException e) {
            e.printStackTrace();
        }

        //用来记录求情的数量
        int count = 0;

        //各线程存放的列表
        connectlist = new LinkedList<Thread>();
        while(true) {
            Socket socket = null;
            try {
                //为该请求建立连接
                socket = serversocket.accept();

                System.out.println("连接"+ count +"以建立！！");

                //为该socket建立多线程，启动，并加入列表
                ConnectionThread connectionthread = new ConnectionThread(socket);
                Thread thread = new Thread(connectionthread);
                thread.start();
                connectlist.add(thread);

                System.out.println("连接"+ count++ +"的线程已启动并加入队列！！");

            }catch(Exception e) {
                e.printStackTrace();
                break;
            }
        }
    }
}
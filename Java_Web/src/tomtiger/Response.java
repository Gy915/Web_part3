package tomtiger;
import java.io.OutputStream;
import java.io.IOException;
import java.io.File;
import java.io.FileInputStream;

public class Response {
    // 定义读取文件时byte[] 数组的大小
    private static final int BUFFER_SIZE = 1024;
    // 用来响应的outputstream，该输出流从 为该请求建立的socket中获得，并传入
    OutputStream outputstream = null;

    // 用outputstream初始化response
    public Response(OutputStream outputstream) {
        this.outputstream = outputstream;
    }

    // 该请求资源的文件路径
    public void responseResource(String uri) {
        // 读取文件时的byte[]
        byte[] resourcetemp = new byte[BUFFER_SIZE];
        // 输入流
        FileInputStream fileinputstream = null;
        if(uri == null)
            return;
        try {
            // 建立文件
        	uri = uri.substring(1);
            File resource = new File(uri);
            // 判断文件是否存在
            if(resource.exists()) {

                System.out.println("请求的资源是：" + resource.getName());

                fileinputstream = new FileInputStream(resource);
                int length = 0;

                String responsehead = "HTTP/1.1 200 OK\r\n" +  "\r\n";
                outputstream.write(responsehead.getBytes());

                while((length = fileinputstream.read(resourcetemp)) > 0) {
                    outputstream.write(resourcetemp, 0, length);
                }
            }
            else {
                String errorPage = "HTTP/1.1 404 File Not Found\r\n" + "Content-Type: text/html\r\n" + "Content-Length: 23\r\n" + "\r\n" + "<h1>File Not Found</h1>";
                outputstream.write(errorPage.getBytes());
            }

            outputstream.close();
        }catch(IOException e){
            e.printStackTrace();
        }finally {
            outputstream = null;
            fileinputstream = null;
        }
    }
}
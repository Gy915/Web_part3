package tomtiger;
import java.io.InputStream;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Request {

    private InputStream inputstream = null;
    private String uri = null;

    // 根据inputstream初始化request
    public Request(InputStream inputstream) {
        this.inputstream = inputstream;
        parseUri();
    }

    // 读取inputstream并将其转化为字符串
    @SuppressWarnings("finally")
    private String requestToString() {
        String requestString = null;
        // 字节流转字符流
        BufferedReader bfreader = new BufferedReader(new InputStreamReader(inputstream));
        StringBuffer buffer = new StringBuffer();

        char[] temp = new char[2048];
        int length = 0;
        try {
            length = bfreader.read(temp);
            buffer.append(temp,0,length);   
            requestString = buffer.toString();

        }catch(IOException e) {
            e.printStackTrace();
        }finally {
            // 输出request
            System.out.println("request为:");
            System.out.println(requestString);

            return requestString;
        }
    }

    // 根据请求报文的特点，请求的文件在第一个和第二个空格之间。所以有了以下方法
    public void parseUri() {
        String request = requestToString();
        if(request != null) {

            int space1 = -1;
            int space2 = -1;
            space1 = request.indexOf(' ');
            if(space1 != -1) {
                space2 = request.indexOf(' ',space1 + 1);
            }
            if(space2 > space1) {
                // 截取第一个和第二个空格之间的字符串，即请求资源的uri
                uri = request.substring(space1 + 1, space2);
            }
            System.out.println(uri);
        }
    }

    // 返回请求资源的uri
    public String getUri() {
        return uri;
    }
}

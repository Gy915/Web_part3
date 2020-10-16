#include <Winsock2.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <direct.h>
#pragma comment(lib,"Ws2_32.lib")
#define SERVER "Server: csr_http1.1\r\n"

int file_not_found(SOCKET sAccept);
int send_file(SOCKET sAccept, FILE *resource);
int send_not_found(SOCKET sAccept);

DWORD WINAPI HTTPServer(LPVOID lparam);
int file_not_found(SOCKET sAccept);
int file_ok(SOCKET sAccept, long flen);
int send_not_found(SOCKET sAccept);
int send_file(SOCKET sAccept, FILE* resource);

int main()
{
	WSADATA wsaData;
	SOCKET sListen, sAccept; 
	int serverport = 8080;   
	struct sockaddr_in ser, cli;   
	int iLen;

	
	printf("wait...\n\n");

	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
	{
		printf("Failed \n");
		return -1;
	}

	sListen = socket(AF_INET, SOCK_STREAM, 0);
	if (sListen == INVALID_SOCKET)
	{
		printf("socket() Failed:%d\n", WSAGetLastError());
		return -1;
	}

	ser.sin_family = AF_INET;
	ser.sin_port = htons(serverport);
	ser.sin_addr.s_addr = htonl(INADDR_ANY); 

	if (bind(sListen, (LPSOCKADDR)&ser, sizeof(ser)) == SOCKET_ERROR)
	{
		printf("blind() Failed:%d\n", WSAGetLastError());
		return -1;
	}

	if (listen(sListen, 5) == SOCKET_ERROR)
	{
		printf("listen() Failed:%d\n", WSAGetLastError());
		return -1;
	}
	while (1) 
	{
		iLen = sizeof(cli);
		sAccept = accept(sListen, (struct sockaddr*)&cli, &iLen);
		if (sAccept == INVALID_SOCKET)
		{
			printf("accept() Failed:%d\n", WSAGetLastError());
			break;
		}
		DWORD ThreadID;
		CreateThread(NULL, 0, HTTPServer, (LPVOID)sAccept, 0, &ThreadID);
	}
	closesocket(sListen);
	WSACleanup();
	return 0;
}

int file_not_found(SOCKET sAccept)
{
	char send_buf[128];
	sprintf(send_buf, "HTTP/1.1 404 NOT FOUND\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "Connection: keep-alive\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, SERVER);
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "Content-Type: text/html\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	return 0;
}

int file_ok(SOCKET sAccept, long flen)
{
	char send_buf[128];
	sprintf(send_buf, "HTTP/1.1 200 OK\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "Connection: keep-alive\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, SERVER);
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "Content-Length: %ld\r\n", flen);
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "Content-Type: text/html\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	return 0;
}

int send_not_found(SOCKET sAccept)
{
	char send_buf[128];
	sprintf(send_buf, "<HTML><TITLE>Not Found</TITLE>\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "<BODY><h1 align='center'>404</h1><br/><h1 align='center'>file not found.</h1>\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	sprintf(send_buf, "</BODY></HTML>\r\n");
	send(sAccept, send_buf, strlen(send_buf), 0);
	return 0;
}

int send_file(SOCKET sAccept, FILE *resource)
{
	char send_buf[1024];
	while (1)
	{
		memset(send_buf, 0, sizeof(send_buf));
		fgets(send_buf, sizeof(send_buf), resource);
		if (SOCKET_ERROR == send(sAccept, send_buf, strlen(send_buf), 0))
		{
			printf("send() Failed:%d\n", WSAGetLastError());
			return -1;
		}
		if (feof(resource))
			return 0;
	}
}

DWORD WINAPI HTTPServer(LPVOID lparam)
{
	SOCKET sAccept = (SOCKET)(LPVOID)lparam;
	char recv_buf[1024];
	char method[128];
	char url[128];
	char path[_MAX_PATH];
	int i, j;

	memset(recv_buf, 0, sizeof(recv_buf));
	if (recv(sAccept, recv_buf, sizeof(recv_buf), 0) == SOCKET_ERROR)  
	{
		printf("recv() Failed:%d\n", WSAGetLastError());
		return -1;
	}
	else
		printf("Recv data from Client:\n%s\n", recv_buf); 
	
	i = 0; 
	j = 0;
	
	while (!(' ' == recv_buf[j]) && (i < sizeof(method) - 1))
	{
		method[i] = recv_buf[j];
		i++; j++;
	}
	method[i] = '\0';

	if (stricmp(method, "GET") && stricmp(method, "HEAD"))
	{
		
		closesocket(sAccept); 
		printf("not get or head method.\nclose ok.\n");
		printf("***********************\n\n\n\n");
		return -1;
	}
	printf("method: %s\n", method);

	
	i = 0;
	while ((' ' == recv_buf[j]) && (j < sizeof(recv_buf)))
		j++;
	j++;//第一个非空字符
	while (!(' ' == recv_buf[j]) && (i < sizeof(recv_buf) - 1) && (j < sizeof(recv_buf)))
	{
		if (recv_buf[j] == '/')
			url[i] = '\\';
		else if (recv_buf[j] == ' ')
			break;
		else
			url[i] = recv_buf[j];
		i++; j++;
	}
	url[i] = '\0';
	printf("url: %s\n", url);

	//_getcwd(path, _MAX_PATH); //当前路径
	strcpy(path, url);//相对路径
	printf("path: %s\n", path);

	
	FILE *resource = fopen(path, "rb");

	if (resource == NULL)
	{
		file_not_found(sAccept);
		if (0 == stricmp(method, "GET"))
			send_not_found(sAccept);

		closesocket(sAccept);
		printf("file not found.\nclose ok.\n\n\n");
		return -1;
	}
	
	fseek(resource, 0, SEEK_SET);
	fseek(resource, 0, SEEK_END);
	long flen = ftell(resource);
	printf("File length: %ld\n", flen);
	fseek(resource, 0, SEEK_SET);
	
	file_ok(sAccept, flen);

	if (0 == stricmp(method, "GET"))
	{
		if (0 == send_file(sAccept, resource))
			printf("File send ok.\n");
		else
			printf("File send fail.\n");
	}
	fclose(resource);

	closesocket(sAccept);
	printf("Close ok.\n\n\n");

	return 0;

}

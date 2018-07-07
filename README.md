## simple_chat
一个带GUI的简单聊天室程序。
 - 语言：Python2.7
 - GUI库：Tkinter
 - 测试环境：Windows10
 - 实现：
	1. 服务器端使用select处理并发连接
	2. 客户端使用多线程处理消息的接受和发送
	3. 客户端和服务器端使用两个socket连接，分别用于传送聊天消息和在线用户列表

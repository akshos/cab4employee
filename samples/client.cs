using System;
using System.IO;
using System.Net.Sockets;
class HelloWorld {
  static void Main() {
      TcpClient cs = new TcpClient();
      cs.Connect("192.168.43.72", 1235);
      Stream serverStream = cs.GetStream();
      Console.WriteLine("Connected !!!! ......");
      StreamReader sr= new StreamReader(serverStream);
      StreamWriter sw= new StreamWriter(serverStream);
      sw.AutoFlush=true;
      sw.Write("companyinterface");
      string recv= sr.ReadLine();
      Console.WriteLine(recv);
      //"Client Socket Program - Server Connected ...";
  }
}

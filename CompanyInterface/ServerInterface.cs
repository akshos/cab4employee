
using System;
using System.IO;
using System.Net.Sockets;

namespace serverInterface{

    public class ServerInterface
    {
        TcpClient cs;
        Stream serverStream;
        StreamWriter sw;
        StreamReader sr;
        string outmsg;
        string recv;

        public void connect(){
            this.cs = new TcpClient();
            cs.ReceiveBufferSize = 1024;
            this.cs.Connect("192.168.2.33", 2345);
            this.serverStream = this.cs.GetStream();
            this.sw = new StreamWriter(serverStream);
            this.sr = new StreamReader(serverStream);
            this.sw.AutoFlush=true; 
        }

        public bool authenticate(string username, string password) {
        try{

                outmsg = "companyinterface login " + username + " " + password;
                sw.Write(outmsg);
                recv = sr.ReadLine();
                if (recv=="done")
                  return true;
                else
                  return false;
          }
        catch{
          Console.WriteLine("error");
          return false;
          }
      }
    }
  }

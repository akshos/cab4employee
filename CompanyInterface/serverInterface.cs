
using System;
namespace serverInterface{
    class interface{

        TcpClient cs;
        StreamWriter sw;
        StreamReader sr;
        string outmsg;
        string recv;
        public bool connect(){
          TcpClient cs = new TcpClient();
          cs.Connect("192.168.43.72", 1235);
          Stream serverStream = cs.GetStream();
          sw = new StreamWriter(serverStream);
          sr= new StreamReader(serverStream);
          sw.AutoFlush=true;
        }
        public bool authenticate(string username, string password) {
        try{

                outmsg= "companyinterface "+username+" "+password;
                sw.Write(outmsg);
                recv= sr.ReadLine();
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

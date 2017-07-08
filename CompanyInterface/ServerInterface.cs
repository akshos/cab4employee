
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
        string inmsg;

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
                inmsg = sr.ReadLine();//contains data recieved from server
                Console.WriteLine(inmsg);

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

      public bool addEmployee(string eid, string first_name, string last_name, string date_of_reg, string contact_number, string account_id, string time_in, string time_out){
          try{
            outmsg="addemployee "+eid+" "+first_name+" "+last_name+" "+date_of_reg+" "+contact_number+" "+account_id+" "+time_in+" "+time_out;
            sw.Write(outmsg);
            recv = sr.ReadLine();
                Console.WriteLine(recv);
                if (recv == "done")
                    return true;
                else if (recv == "EC1")
                    return false;
                else
                    return false;
          }
          catch{
            if (!cs.Connected)
              {Console.WriteLine("Not connected.");
               connect();
             }
             else
             {
                    Console.WriteLine("Error has occured ");
           }
                return false;
          }

      }
    }
  }

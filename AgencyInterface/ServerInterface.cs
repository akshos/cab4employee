
using System;
using System.IO;
using System.Net.Sockets;

namespace serverInterface
{

    public class ServerInterface
    {
        TcpClient cs;
        Stream serverStream;
        StreamWriter sw;
        StreamReader sr;
        string outmsg;
        string recv;
        string inmsg;

        public void connect()
        {
            this.cs = new TcpClient();
            cs.ReceiveBufferSize = 1024;
            this.cs.Connect("192.168.1.8", 2345);
            this.serverStream = this.cs.GetStream();
            this.sw = new StreamWriter(serverStream);
            this.sr = new StreamReader(serverStream);
            this.sw.AutoFlush = true;
        }



        public bool authenticate(string username, string password)
        {
            try
            {
                outmsg = "agencyinterface login " + username + " " + password;
                Console.WriteLine(username + " " + password);
                sw.Write(outmsg);
                recv = sr.ReadLine();
                //outmsg = sr.ReadLine();
                Console.WriteLine(inmsg);
                if (recv == "done")
                    return true;
                else
                    return false;
            }
            catch
            {
                Console.WriteLine("error");
                return false;
            }
        }

        public bool addCab(string cid, string c_model, string maxpassengers)
        {
            try
            {
                outmsg = "addemployee " + cid + " " + c_model + " " + maxpassengers;
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
            catch
            {
                if (!cs.Connected)
                {
                    Console.WriteLine("Not connected.");
                    connect();
                }
                else
                {
                    Console.WriteLine("Error has occured ");
                }
                return false;
            }

        }

        public String getCabFeedback(){
          outmsg = "cabfeedback "
          sw.Write(outmsg);
          recv=sr.ReadLine();
          Console.WriteLine(recv);
          inmsg=sr.ReadLine();
          Console.WriteLine(inmsg);
          if (recv == "done")
              return true;
          else if (recv == "EC1")
              return false;
          else
              return false;
        }
        public String getDriverFeedback(){
          outmsg = "driverfeedback "
          sw.Write(outmsg);
          recv=sr.ReadLine();
          Console.WriteLine(recv);
          inmsg=sr.ReadLine();
          Console.WriteLine(inmsg);
          if (recv == "done")
              return true;
          else if (recv == "EC1")
              return false;
          else
              return false;
        }

        public String getAllocationsFromServer()
        {
            outmsg = "getallocations";
            sw.Write(outmsg);
            recv = sr.ReadLine();
            Console.WriteLine(recv);
            return recv;
        }

    }

}

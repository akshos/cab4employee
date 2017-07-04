

public static bool insert(TcpClient cs, string username, string password) {
  try{
      Stream serverStream = cs.GetStream();
      StreamWriter sw = new StreamWriter(serverStream);
      StreamReader sr= new StreamReader(serverStream);
      sw.AutoFlush=true;
      string outmsg= "companyinterface "+username+" "+password;
      sw.Write(outmsg);
      string recv= sr.ReadLine();
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

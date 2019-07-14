using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using CookComputing.XmlRpc;
using System.Linq;



[XmlRpcUrl("http://localhost:55999/RPC2")]
public interface IGetValues : IXmlRpcProxy
{
    [XmlRpcMethod("get_os")]
    string testMyClient();

    [XmlRpcMethod("return_all_sports")]
    string GetSportValues();
}





public class CookClient {

    public string GetOS()
    {
        IGetValues proxy = XmlRpcProxyGen.Create<IGetValues>();
        string ret = proxy.testMyClient();
        Debug.Log(ret.ToString());
        
        return ret;
    }
    public string GetSportValues()
    {
        IGetValues proxy = XmlRpcProxyGen.Create<IGetValues>();
        string ret = proxy.GetSportValues();
        return ret;
    }

    // Use this for initialization
    void Start () {
        //IGetValues proxy = XmlRpcProxyGen.Create<IGetValues>();

       // string ret = proxy.testMyClient();
    }
	
	// Update is called once per frame
	void Update () {
		
	}
}

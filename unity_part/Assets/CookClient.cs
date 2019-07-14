using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using CookComputing.XmlRpc;
using System.Linq;


[XmlRpcUrl("http://localhost:8000/RPC2")]
public interface IGetValues : IXmlRpcProxy
{
    [XmlRpcMethod("get_os")]
    string testMyClient();

    [XmlRpcMethod("return_all_sports")]
    List<string> GetSportValues();
}





public class CookClient {

    public string GetOS()
    {
        IGetValues proxy = XmlRpcProxyGen.Create<IGetValues>();
        string ret = proxy.testMyClient();
        Debug.Log(ret.ToString());
        return ret;
    }
    public List<string> GetSportValues()
    {
        IGetValues proxy = XmlRpcProxyGen.Create<IGetValues>();
		List<string> ret = proxy.GetSportValues().ToList();
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

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using CookComputing.XmlRpc;

[XmlRpcUrl("http://localhost:8000/RPC2")]
public interface ISumAndDiff : IXmlRpcProxy
{
	[XmlRpcMethod("get_os")]
	string testMyClient();
}



public class ClientCook : MonoBehaviour {
	public Text text;

	// Use this for initialization
	void Start () {
		ISumAndDiff proxy = XmlRpcProxyGen.Create<ISumAndDiff>();

		string ret = proxy.testMyClient();
		Debug.Log (ret.ToString ());
		text.text = ret.ToString ();
	}

	// Update is called once per frame
	void Update () {

	}
}
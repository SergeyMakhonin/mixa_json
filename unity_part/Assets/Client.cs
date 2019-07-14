
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using CookComputing.XmlRpc;


public class Client : MonoBehaviour
{
    private const int PORT = 8000;
    private const string ServerIP = "192.168.0.163";
    private const int BYTE_SIZE = 1204;

    private byte reliableChannel;
    private const int maxusers = 10;
    private int hostId;
    private byte error;

    private bool isStarted;
    
    

    public void Init()
    {
        NetworkTransport.Init();

        ConnectionConfig cc = new ConnectionConfig();
        reliableChannel = cc.AddChannel(QosType.Reliable);

        HostTopology topo = new HostTopology(cc, maxusers);

        hostId = NetworkTransport.AddHost(topo, 0);
        NetworkTransport.Connect(hostId, ServerIP, PORT, 0, out error);

        if ((NetworkError)error != NetworkError.Ok)
        {
            //Output this message in the console with the Network Error
            Debug.Log("There was this error : " + (NetworkError)error);
        }
        isStarted = true;

    }
    public void Shutdown()
    {
        isStarted = false;
        NetworkTransport.Shutdown();

    }

    public void UpdateMessage()
    {
        if (!isStarted)
            return;

        int recHostId;
        int ConnectionId;
        int channelId;

        byte[] recBuffer = new byte[BYTE_SIZE];
        int dataSize;

        NetworkTransport.Receive(out recHostId, out ConnectionId, out channelId, recBuffer, recBuffer.Length, out dataSize, out error);
        
    }
    // Start is called before the first frame update
    void Start()
    {
        DontDestroyOnLoad(gameObject);
        Init();
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(isStarted.ToString());
    }
}

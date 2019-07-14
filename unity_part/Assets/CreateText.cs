using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class CreateText : MonoBehaviour
{
    public void CreateTxtFile(string airname, string content)
    {
        string path = Application.dataPath + "/" + airname + ".txt";

        if(!File.Exists(path))
        {
            File.WriteAllText(path, content);
        }
        File.WriteAllText(path, content);

    } 
    // Start is called before the first frame update
    void Start()
    {

        string air = "Air1";
        string contents = "1.9";

        CreateTxtFile(air, contents);

    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Dropdownmgr : MonoBehaviour
{

    public List<string> options = new List<string>();
    public Dropdown dropdown;
    public string selectedname;
    //public bool changed = true;
    
    public void Dropdown_IndexChanged(int index)
    {
        selectedname = options[index];
        //changed = true;

    }
    


    // Start is called before the first frame update
    
}

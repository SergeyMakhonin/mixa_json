using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;


public class MyDataMgr : MonoBehaviour
{

    public CookClient gv = new CookClient();
    public Dropdown sportdd;
    public Dropdownmgr sportmgr;
    public List<string> sportlist = new List<string>();
    public string selectedsport;

    public Dropdown leaguedd;
    public Dropdownmgr leaguemgr;
    public List<string> leaguelist = new List<string>();
    public string selectedleague;

    public Dropdown eventdd;
    public Dropdownmgr eventmgr;
    public List<string> eventlist = new List<string>();
    public string selectedevent;

    public Dropdown bettypedd;
    public Dropdownmgr bettypemgr;
    public List<string> bettypelist = new List<string>();
    public string selectedbettype;

    public Dropdown betdd;
    public Dropdownmgr betmgr;
    public List<string> betlist = new List<string>();
    public string selectedbet;

    public Text selectedodd;
    public Text os;
    public string odd;

    public void PopulateList(Dropdown dropdown, List<string> options)
    {
        dropdown.AddOptions(options);
    }

    public List<string> Lister(string line)
    {
        List<string> ret = line.Split(',').ToList();
        return ret;
    }

    public void SportValueChanged(Dropdown dropdown)
    {
        ////запросить у сервера leaguelist по selectedsport
        

        selectedsport = sportmgr.selectedname;
        Debug.Log(selectedsport);
        Debug.Log(sportmgr.selectedname);
        Debug.Log("requesting leagues");
        leaguemgr.options = leaguelist;
        //очистить все dropdown
        leaguedd.ClearOptions();
        eventdd.ClearOptions();
        bettypedd.ClearOptions();
        betdd.ClearOptions();

        PopulateList(leaguedd, leaguelist);
    }

    public void LeagueValueChanged(Dropdown dropdown)
    {
        ////запросить у сервера eventlist по selectedleague
        selectedleague = leaguemgr.selectedname;
        Debug.Log(selectedleague);
        Debug.Log(leaguemgr.selectedname);
        Debug.Log("requesting events");
        //очистить списки
        eventdd.ClearOptions();
        bettypedd.ClearOptions();
        betdd.ClearOptions();
    }

    // Start is called before the first frame update
    void Start()
    {

        

        sportmgr = sportdd.GetComponent<Dropdownmgr>();
        leaguemgr = leaguedd.GetComponent<Dropdownmgr>();
        eventmgr = eventdd.GetComponent<Dropdownmgr>();
        bettypemgr = bettypedd.GetComponent<Dropdownmgr>();
        betmgr = betdd.GetComponent<Dropdownmgr>();

        sportdd.onValueChanged.AddListener(delegate { SportValueChanged(sportdd); });
        leaguedd.onValueChanged.AddListener(delegate { LeagueValueChanged(leaguedd); });


        Debug.Log(gv.GetOS().ToString());
        
        
    }

    // Update is called once per frame
    void Update()
    {
        
        if(sportdd.options.Count == 0 && String.IsNullOrEmpty(selectedsport) )
        {
            //запросить у сервера sportlist

            sportlist = Lister(gv.GetSportValues());

            Debug.Log("requesting sports");

            sportmgr.options = sportlist;
            PopulateList(sportdd, sportlist);

            sportmgr.selectedname = sportlist[0];
            selectedsport = sportmgr.selectedname;
            

        }


    }
}

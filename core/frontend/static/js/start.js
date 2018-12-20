function seltype(varID) {
    oCssSet = document.getElementById("sel_opt");
    oTest = document.getElementById("tab_div1");
    oTestsel = document.getElementById("test_sel");
    oVal = document.getElementById("div_val");
    oCssSet.innerHTML = "";
    $("#div_val").hide();
    $("#tab_div1").hide();
    //oTest.innerHTML = "";
    //Reset the test_set
    /*while (oTest.firstChild) {
        oTest.removeChild(oTest.firstChild);
    }*/
    
    //Try to remove comment if there are
    try {
        oTnotes = document.getElementById("t_notes");
        oTnotes.remove()
    }
    catch(err) {
        console.log(err);
    }
    
    $.ajax({
        type: "POST",
        url: "test_type",
        data: {selType: varID.value},
        success: function (data) {
            oCssSet.disabled = false;
            
            $.each(data, function (index) {
                
                if (index == 0) {
                    var opt1 = document.createElement("option");
                    opt1.value = 1;
                    opt1.innerHTML = '-- select an option --';
                    opt1.disabled = false;
                    oCssSet.appendChild(opt1);
                } 
                
                var opt = document.createElement("option");
                opt.value = data[index].selID;
                opt.innerHTML = data[index].selDescr;
                               
                oCssSet.appendChild(opt);
                
            });

        }
    });
}

function AddOptions(VarID) {

    oType = document.getElementById("sel_type");
    oType.insertBefore(new Option('', ''), oType.firstChild);
    oTsel = document.getElementById("test_sel");
    oTtabs = document.getElementById("test_tabs");
    oCss1 = document.getElementById("div_val");
    oCss2 = GetElementInsideContainer("div_val", "div_sched");
    //oCssBtn = GetElementInsideContainer("div_val", "div_btn");
    oCssBtn = document.getElementById("div_btn");
    oCssSet = document.getElementById("sel_opt");
    tmain = document.getElementById("tab_div1");
    tdata = document.getElementById("tab_div2");
    drst = document.getElementById("div_rst");
    trst1 = document.getElementById("rst1");
    trst2 = document.getElementById("rst2");
    trst3 = document.getElementById("rst3");
    if (tdata == null) {
                location.reload();
    }
    console.log(tdata);
    //tdata = GetElementInsideContainer("tab_div1", "tab_div2");
    //Create button run
    var buttonMgm = document.createElement("input");
    buttonMgm.type = "button";
    buttonMgm.value = "START";
    buttonMgm.className = "btn btn-primary";
    buttonMgm.onclick = function () {
        testBtn(VarID, oType.value);
    }
    /*//Button for see html tab after start test
    var buttonHtml = document.createElement("input");
    buttonHtml.type = "button";
    buttonHtml.value = "INSPECT";
    buttonHtml.className += "btn btn-default btn-sm";
    buttonHtml.onclick = function () {
        inspectHTML(VarID);
    }*/
    document.getElementById("overlay_get").style.display = "block";
    console.log('varid is:'+VarID.value);
    $.ajax({
        type: "POST",
        url: "ajax",
        data: {mainID: VarID.value, selType: oType.value},
        success: function (data) {
            //oCssSet.innerHTML = "";
            oCssBtn.innerHTML = "";
            while (tmain.firstChild) {
                tmain.removeChild(tmain.firstChild);
            }
            if (tdata != null) {
                while (tdata.firstChild) {
                    tdata.removeChild(tdata.firstChild);
                }
            } else {
                tdata = document.getElementById("tab_div2");
            }

            var ul_tab = document.createElement("UL");
            ul_tab.className += "nav nav-tabs";

            var isgroup = 0;
            var tabpane = "tab-pane active";
            var liclass = "active";
            $("#div_val").show();
            $("#tab_div1").show();
            if (oType.value == "ST") {
                $("#div_sched").show();
            } else {
                $("#div_sched").hide();
            }

            //First if there is a testset description delete it
            try {
                oTsel.removeChild(optNotes);
                }
            catch(err) {
                console.log(err);
            }

            $.each(data, function (index) {

                                
                if (index == 0) {

                    var li_tab = document.createElement("LI");
                    li_tab.className += liclass;

                    var createA = document.createElement('a');
                    var createAText = document.createTextNode("Variables");
                    createA.setAttribute('href', "#tab_" + data[index].OptionMain);
                    createA.setAttribute('data-toggle', "tab");
                    createA.appendChild(createAText);
                    li_tab.appendChild(createA);

                    ul_tab.appendChild(li_tab);
                    tmain.appendChild(ul_tab);
                    var sub_data = document.createElement("div");
                    sub_data.className = tabpane;
                    //sub_data.setAttribute("id", "tab_" + data[index].OptionMain);
                    sub_data.setAttribute("id", "tab_1");
                    if (tdata != null) {
                        tdata.appendChild(sub_data);
                        tmain.appendChild(tdata);
                    }


                    isgroup = data[index].OptionMain;
                    tabpane = "tab-pane";
                    liclass = "";
                    
                    
                    if (oType.value == "ST") {
                        //If there is a t_main description create a readonly textarea for display it 
                        console.log("Descr: "+data[index].OptionNote);
                        if (data[index].OptionNote != undefined) {
                            optNotes = document.createElement("SPAN");
                            optNotes.setAttribute("id", "t_notes");
                            optNotes.setAttribute('class', 'label label-default');
                            optNotes.innerHTML = data[index].OptionNote;
                            oTsel.appendChild(optNotes);   
                        }
                    }
                }
                
                //Because if is undefine is related to rst values for preview in json return response
                if (data[index].OptionID)
                {
                    tart11 = document.createElement('input', '', 'form-control');
                    tart11.setAttribute('type', 'text');
                    tart11.id = data[index].OptionKey;
                    tart11.setAttribute('class',"form-control");
                    tart11.value = data[index].OptionVal;
                    var createVarText = document.createElement("SPAN");
                    createVarText.setAttribute('class', 'label label-warning');
                    createVarText.innerHTML = data[index].OptionDescr + " - " + data[index].OptionKey;
                    //var createVarText = document.createTextNode(data[index].OptionDescr+"-> "+data[index].OptionKey+"-> ");
                    var createSpace = document.createTextNode("  ");
                    var br = document.createElement("BR");
                    tart11.defaultValue = data[index].OptionVal;
                    //Create all elements for make select in text (scalar,rand int and rand string
                    var dsel1 = document.createElement("div");
                    dsel1.setAttribute('class',"input-group input-group-sm");
                    var dsel2 = document.createElement("div");
                    dsel2.setAttribute('class',"input-group-btn");
                    var butsel = document.createElement("button");
                    butsel.type = "button";
                    butsel.id = 'bs_'+data[index].OptionKey;
                    butsel.innerHTML = "Scalar ";
                    butsel.value = "SC";
                    butsel.className = "btn btn-warning dropdown-toggle";
                    butsel.setAttribute('data-toggle',"dropdown");
                    var spambtn = document.createElement("SPAN");
                    spambtn.setAttribute('class',"fa fa-caret-down");
                    butsel.appendChild(spambtn);
                    ulsel = document.createElement("UL");
                    ulsel.setAttribute('class',"dropdown-menu");
                    lisel1 = document.createElement("LI");
                    asel1 = document.createElement("A");
                    asel1.innerHTML = "Scalar";
                    lisel1.appendChild(asel1);
                    lisel2 = document.createElement("LI");
                    asel2 = document.createElement("A");
                    asel2.innerHTML = "Random (Num)";
                    lisel2.appendChild(asel2);
                    lisel3 = document.createElement("LI");
                    asel3 = document.createElement("A");
                    asel3.innerHTML = "Random (String)";
                    lisel3.appendChild(asel3);
                    ulsel.appendChild(lisel1);
                    ulsel.appendChild(lisel2);
                    ulsel.appendChild(lisel3);
                    dsel2.appendChild(butsel);
                    dsel2.appendChild(ulsel);
                    dsel1.appendChild(dsel2);
                    dsel1.appendChild(tart11);
                    asel1.onclick = function () {
                        butsel.innerHTML = "Scalar ";
                        document.getElementById(data[index].OptionKey).value = "";
                        document.getElementById(data[index].OptionKey).placeholder = "Enter the value of the variable";
                        document.getElementById('bs_'+data[index].OptionKey).value = "SC";
                    }
                    asel2.onclick = function () {
                        butsel.innerHTML = "Random (Num) ";
                        //Clear data and display help text
                        document.getElementById(data[index].OptionKey).value = "";
                        document.getElementById(data[index].OptionKey).placeholder = "Enter the number range (ex: 0-200)";
                        document.getElementById('bs_'+data[index].OptionKey).value = "RN";
                    }
                    asel3.onclick = function () {
                        butsel.innerHTML = "Random (String) ";
                        document.getElementById(data[index].OptionKey).value = "";
                        document.getElementById(data[index].OptionKey).placeholder = "Enter the length of the string (ex: 10)\n";
                        document.getElementById('bs_'+data[index].OptionKey).value = "RS";

                    }
                    //--------------------------------------------------------------
                    vard = document.getElementById("tab_" + data[index].OptionMain);
                    vard = document.getElementById("tab_1");
                    vard.appendChild(createVarText);
                    vard.appendChild(createSpace);
                    vard.appendChild(dsel1);
                    vard.appendChild(br);
                    opdescr = document.createTextNode(data[index].OptionDescr);
                } else {
                    if (oType.value == "ST") {
                        drst.style.display = 'inline-block';
                        trst1.innerText = "";
                        trst2.innerText = "";
                        trst3.innerText = "";
                        trst1.innerText = data[index].r_settings;
                        trst2.innerText = data[index].r_case;
                        trst3.innerText = data[index].r_key;
                    } else {
                        drst.style.display = 'none';
                    }
                }


            });

            oTtabs.appendChild(tmain);
            oTsel.appendChild(oCssSet);
            oCss1.appendChild(oCss2);
            oCssBtn.appendChild(buttonMgm);

        }
    });
}

//Func for create inspection of selected template in home
function inspectHTML(objID) {
    alert(objID.value);
}


$(document).ajaxStop(function () {
    //alert('STOP');
    
    document.getElementById("overlay_get").style.display = "none";
});

function testBtn(VarID, t_type) {

    document.getElementById("overlay").style.display = "block";
    //var divScan = GetElementInsideContainer("tab_div1","tab_div2");
    var divScan = document.getElementById("tab_div2");
    var ancestor = divScan,
        descendents = ancestor.getElementsByTagName('*');
    oCssSet = document.getElementById("sel_opt");
    console.log("Ocss.val--->"+oCssSet.value);

    var row = [];
    var col = [];
    var uuid = guid();

    if (t_type == "ST") {
        Schedsel = document.getElementById("sched_type");
        Schedval = document.getElementById("sched_val");
    } else {
        Schedsel = "once";
        Schedval = "";
    }

    console.log(" Sched: " + Schedsel.value + " val: " + Schedval.value)

    for (i = 0; i < descendents.length; i++) {
        e = descendents[i];
        row.push(e.id)
        col.push(e.value)
    }

    var res = row.map((v, i) => [v, col[i]]);
    //res.splice(-1,1);
    var res = res.filter(function(x){
        return (x[0] !== (undefined || null || ''));
    });
    console.log(res);
    /*res.forEach(function(item, index, array) {
        if (item[0].length == 0) {
            console.log(item, index);
            //res.splice(index,1);
        }
    });*/

    //Stringhify the array for pass to python and then decode it
    var json_string = JSON.stringify(res);
    window.location.href = '/active#act_th';

    $.ajax({
        type: "POST",
        url: "start",
        data: {
            mainID: VarID.value,
            ttype: t_type,
            des: json_string,
            sched_sel: Schedsel.value,
            sched_val: Schedval.value,
            group_val: oCssSet.value,
            t_id: uuid
        },
        success: function (data) {
            //document.getElementById("overlay").style.display = "none";
        },
        complete: function (data) {
            document.getElementById("overlay").style.display = "none";
            if (document.getElementById('tab_threads') == null) {
                window.location.href = '/';
            }
        }
    });
}


function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}

function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}

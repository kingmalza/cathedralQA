function seltype(varID) {
    oCssSet = document.getElementById("sel_opt");
    oTest = document.getElementById("tab_div1");
    oVal = document.getElementById("div_val");
    oCssSet.innerHTML = "";
    $("#div_val").hide();
    $("#tab_div1").hide();
    //oTest.innerHTML = "";
    //Reset the test_set
    /*while (oTest.firstChild) {
        oTest.removeChild(oTest.firstChild);
    }*/
    $.ajax({
        type: "POST",
        url: "test_type",
        data: {selType: varID.value},
        success: function (data) {
            oCssSet.disabled = false;

            $.each(data, function (index) {
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
    tmain = document.getElementById("tab_div1");
    tdata = document.getElementById("tab_div2");
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
                }


                tart11 = document.createElement('input', '', 'form-control');
                tart11.setAttribute('type', 'text');
                tart11.id = data[index].OptionKey;
                tart11.value = data[index].OptionVal;
                var createVarText = document.createElement("SPAN");
                createVarText.setAttribute('class', 'label label-warning');
                createVarText.innerHTML = data[index].OptionDescr+" - "+data[index].OptionKey;
                //var createVarText = document.createTextNode(data[index].OptionDescr+"-> "+data[index].OptionKey+"-> ");
                var createSpace = document.createTextNode("  ");
                var br = document.createElement("BR");
                tart11.defaultValue = data[index].OptionVal;
                vard = document.getElementById("tab_" + data[index].OptionMain);
                vard = document.getElementById("tab_1");
                vard.appendChild(createVarText);
                vard.appendChild(createSpace);
                vard.appendChild(tart11);
                vard.appendChild(br);
                opdescr = document.createTextNode(data[index].OptionDescr);

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

function testBtn(VarID, t_type) {

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

//Global varc(BP) for know witch one button for record portion display was used
var t_sect = 1

function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}


  $(document).ajaxStop(function () {
      //alert('STOP');
      document.getElementById("overlay").style.display = "none";
      document.getElementById("overlay_proc").style.display = "none";
  });


function refHistory(j_ord, j_sign, j_search, is_search) {
    var stat_h = document.getElementById("stat_load");
    //j_search = document.getElementById("txthis").value;
    j_search = null;
    if (j_ord == null){
        j_ord = '-id';
    }
    if (j_sign == null){
        j_sign = '-';
    }
    if (j_search == null || j_search == 0){
        j_search = 'noSearch';
    }
    if (is_search == null){
        is_search = 0;
    }
    //alert(j_ord+"--"+j_sign+"--"+j_search+"--"+is_search);


    //Label for test type
    l_ttype="";

    //FIRST WE REFRESH TH TOP ELEMENTS
    t_box1 = document.getElementById("h_box1");
    t_box2 = document.getElementById("h_box2");
    t_box3 = document.getElementById("h_box3");
    t_box4 = document.getElementById("h_box4");
    t_box1.innerHTML = "";
    t_box2.innerHTML = "";
    t_box3.innerHTML = "";
    t_box4.innerHTML = "";

    //NOW THE HISTORY TABLE
    t_body = document.getElementById("h_tab");

    //HERE WE GENERATE FOOTER GROUPPING BUTTON FROM TOTAL ROW/20
    t_group = document.getElementById("ul_group");

    //TIMELINE ELEMENTS
    t_line = document.getElementById("tline");
    t_lineH1 = GetElementInsideContainer("tl_tit", "tl_h4");

    //SET WARNING FOR LOADING VISIBLE
    //stat_h.style.visibility = 'visible';

    $.ajax({
        type: "POST",
        url: "hrefresh",
        data: {tab_slice: t_sect, tab_ord: j_ord, tab_search: j_search, isearch: is_search},
        success: function (data) {
            //Var for check if a row is double or not
            var noDouble = "";
            t_body.innerHTML = "";
            //stat_h.style.visibility = 'hidden';
            if (data) {
                t_group.innerHTML = "";
                //dlen = (data + '').length;
                dlen = data[data.length-1];
                //dlen = data[index].OptionNumT;
                //Create footer elements for multiple of 20

                //var multipler = dlen.size / 20;
                var multipler = dlen / 20;
                console.log('len->'+dlen+'-data->'+data+'-mul-->'+multipler);
                for (i = 0; i < multipler; i++) {
                    var li_0 = document.createElement("LI");
                    newlink = document.createElement('a');
                    newlink.innerHTML = i + 1;
                    li_0.appendChild(newlink)
                    t_group.appendChild(li_0);
                }

            }

            if (data[0].TotData != undefined) {
                t_box1.innerHTML = data[0].TotData;
                t_box2.innerHTML = data[0].wData;
                t_box3.innerHTML = data[0].PercPass+"%";
                t_box4.innerHTML = data[0].PercFail+"%";
            } else {
                t_box1.innerHTML = '0';
                t_box2.innerHTML = '0';
                t_box3.innerHTML = "0%";
                t_box4.innerHTML = "0%";
            }


            $.each(data, function (index) {

                if (index == 0) {
                    var t_tr0 = document.createElement("TR");
                    var t_td0 = document.createElement("TD");
                    t_td0.innerHTML = 'ID'.bold();
                    t_td0.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-id','+');
                        } else {
                            refHistory('id','-');
                        };
                    };
                    var t_td1 = document.createElement("TD");
                    t_td1.innerHTML = 'Test Group'.bold();
                    t_td1.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_tgroup','+');
                        } else {
                            refHistory('thread_tgroup','-');
                        };
                    };
                    var t_td2 = document.createElement("TD");
                    t_td2.innerHTML = 'Test Type'.bold();
                    t_td2.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_ttype','+');
                        } else {
                            refHistory('thread_ttype','-');
                        };
                    };
                    var t_td10 = document.createElement("TD");
                    t_td10.innerHTML = 'Test Name'.bold();
                    t_td10.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-id_test__test_main','+');
                        } else {
                            refHistory('id_test__test_main','-');
                        };
                    };
                    var t_td11 = document.createElement("TD");
                    t_td11.innerHTML = 'Schedule'.bold();
                    t_td11.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-ithread_stype','+');
                        } else {
                            refHistory('thread_stype','-');
                        };
                    };
                    var t_td12 = document.createElement("TD");
                    t_td12.innerHTML = 'Schedule Value'.bold();
                    t_td12.setAttribute('class', 'sorting');
                    t_td12.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_sval','+');
                        } else {
                            refHistory('thread_sval','-');
                        };
                    };
                    var t_td13 = document.createElement("TD");
                    t_td13.innerHTML = 'Thread Name'.bold();
                    t_td13.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_main','+');
                        } else {
                            refHistory('thread_main','-');
                        };
                    };
                    var t_td13_run = document.createElement("TD");
                    t_td13_run.innerHTML = 'Run Type'.bold();
                    t_td13_run.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_runtype','+');
                        } else {
                            refHistory('thread_runtype','-');
                        };
                    };
                    var t_td3 = document.createElement("TD");
                    t_td3.innerHTML = 'Start'.bold();
                    t_td3.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_startd','+');
                        } else {
                            refHistory('thread_startd','-');
                        };
                    };
                    var t_td4 = document.createElement("TD");
                    t_td4.innerHTML = 'Stop'.bold();
                    t_td4.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-thread_stopd','+');
                        } else {
                            refHistory('thread_stopd','-');
                        };
                    };
                    var t_td4time = document.createElement("TD");
                    t_td4time.innerHTML = 'Elapsed'.bold();
                    t_td4time.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-id_time__elapsed_t','+');
                        } else {
                            refHistory('id_time__elapsed_t','-');
                        };
                    };
                    var t_td5 = document.createElement("TD");
                    t_td5.innerHTML = 'User'.bold();
                    t_td5.onclick = function() {
                        if(j_sign == '-') {
                            refHistory('-id_test__user_id','+');
                        } else {
                            refHistory('id_test__user_id','-');
                        };
                    };
                    var t_td6 = document.createElement("TD");
                    t_td6.innerHTML = 'col1';
                    var t_td7 = document.createElement("TD");
                    t_td7.innerHTML = 'Passed';
                    var t_td8 = document.createElement("TD");
                    t_td8.innerHTML = 'Failures';
                    var t_td9 = document.createElement("TD");
                    t_td9.innerHTML = 'Cycles';
                    var t_td14 = document.createElement("TD");
                    t_td14.innerHTML = 'TAG';
                    t_td14.setAttribute('id', 'tag_h');

                    t_tr0.appendChild(t_td0);
                    t_tr0.appendChild(t_td10);
                    t_tr0.appendChild(t_td2);
                    t_tr0.appendChild(t_td1);
                    t_tr0.appendChild(t_td11);
                    t_tr0.appendChild(t_td12);
                    t_tr0.appendChild(t_td13);
                    t_tr0.appendChild(t_td13_run);
                    t_tr0.appendChild(t_td3);
                    t_tr0.appendChild(t_td4);
                    t_tr0.appendChild(t_td4time);
                    t_tr0.appendChild(t_td5);
                    //t_tr0.appendChild(t_td6);
                    t_tr0.appendChild(t_td7);
                    t_tr0.appendChild(t_td8);
                    t_tr0.appendChild(t_td9);
                    t_tr0.appendChild(t_td14);
                    t_body.appendChild(t_tr0);

                    //Hide tag column, don't remove it, is for identification purposes
                    document.getElementById('tag_h').style.display = 'none';

                }
                if (data[index].tID != undefined) {
                    //FIRST CHECK IF THERE ARE DOUBLE VALUES AND DISPLAY JUST UNIQUE
                    //if (noDouble.trim() != data[index].OptionMain.trim()) {
                        //label for test type
                        if (data[index].OptionType == '') {
                            l_ttype = 'NODATA';
                        } else {
                            l_ttype = data[index].OptionType;
                        }
                        /*
                        switch (data[index].OptionType) {
                            case 'ST':
                                l_ttype = "SINGLE";
                                break;
                            case 'TA':
                                l_ttype = "TAG";
                                break;
                            case 'PA':
                                l_ttype = "PROJECT";
                                break;
                            case 'TG':
                                l_ttype = "TEST GROUP";
                                break;
                            default:
                                l_ttype = 'NODATA';
                        }
                        */
                        //Create head and data table
                        var t_tr0 = document.createElement("TR");
                        t_tr0.style.borderStyle = 'solid';
                        t_tr0.id = data[index].OptionMain;
                        var t_td0 = document.createElement("TD");
                        t_td0.innerHTML = data[index].tID;
                        var t_td1 = document.createElement("TD");
                        var td1_span = document.createElement("SPAN")
                        if (data[index].OptionGroup == "NoGroup") {
                            td1_span.setAttribute('class', 'label label-default');
                        } else {
                            td1_span.setAttribute('class', 'label label-primary');
                        }
                        td1_span.innerHTML = data[index].OptionGroup;
                        t_td1.appendChild(td1_span);
                        var t_td2 = document.createElement("TD");
                        var td2_span = document.createElement("SPAN");
                        if (l_ttype != 'NODATA') {
                            td2_span.setAttribute('class', 'label label-warning');
                        } else {
                            td2_span.setAttribute('class', 'label pull-right bg-red');
                        }
                        td2_span.innerHTML = l_ttype;
                        t_td2.appendChild(td2_span);
                        var t_td11 = document.createElement("TD");
                        t_td11.innerHTML = data[index].OptionStype;
                        var t_td12 = document.createElement("TD");
                        t_td12.innerHTML = data[index].OptionSval;
                        var t_td13 = document.createElement("TD");
                        t_td13.innerHTML = data[index].OptionMain;
                        var t_td13_run = document.createElement("TD");
                        t_td13_run.innerHTML = data[index].OptionRun;
                        var t_td10 = document.createElement("TD");
                        t_td10.innerHTML = data[index].tTest;
                        var t_td3 = document.createElement("TD");
                        t_td3.innerHTML = data[index].OptionSdate;
                        var t_td4 = document.createElement("TD");
                        if (data[index].OptionStopdate == "None") {
                            var td4_span = document.createElement("SPAN");
                            td4_span.setAttribute('class', 'label label-warning');
                            td4_span.innerHTML = "SCHEDULED TERMINATION";
                            t_td4.appendChild(td4_span);
                        } else {
                            t_td4.innerHTML = data[index].OptionStopdate;
                        }
                        var t_td4time = document.createElement("TD");
                        t_td4time.innerHTML = data[index].OptionTime;
                        var t_td5 = document.createElement("TD");
                        t_td5.innerHTML = data[index].OptionUser;
                        var t_td6 = document.createElement("TD");
                        t_td6.innerHTML = data[index].OptionTest;
                        var t_td7 = document.createElement("TD");
                        //Calculate the success percentage data
                        if (data[index].OptionPass + data[index].OptionFail != 0) {
                            var ssuc = Math.round(((data[index].OptionPass) * 100) / (data[index].OptionPass + data[index].OptionFail));
                            var sfail = Math.round(((data[index].OptionFail) * 100) / (data[index].OptionPass + data[index].OptionFail));
                        } else {
                            var ssuc = 0;
                            var sfail = 0;
                        }

                        var td7_span = document.createElement("SPAN");
                        td7_span.setAttribute('class', 'badge bg-green');
                        td7_span.innerHTML = ssuc+"%";
                        t_td7.appendChild(td7_span);
                        var t_td8 = document.createElement("TD");
                        var td8_span = document.createElement("SPAN");
                        td8_span.setAttribute('class', 'badge bg-red');
                        td8_span.innerHTML = sfail+"%";
                        t_td8.appendChild(td8_span);
                        var t_td9 = document.createElement("TD");
                        var td9_span = document.createElement("SPAN");
                        td9_span.setAttribute('class', 'badge bg-light-blue');
                        td9_span.innerHTML = data[index].OptionNumT;
                        t_td9.appendChild(td9_span);
                        var t_td14 = document.createElement("TD");
                        t_td14.innerHTML = data[index].OptionUUID;
                        t_td14.setAttribute('style', 'display: none');

                    t_tr0.appendChild(t_td0);
                    t_tr0.appendChild(t_td10);
                    t_tr0.appendChild(t_td2);
                    t_tr0.appendChild(t_td1);
                    t_tr0.appendChild(t_td11);
                    t_tr0.appendChild(t_td12);
                    t_tr0.appendChild(t_td13);
                    t_tr0.appendChild(t_td13_run);
                    t_tr0.appendChild(t_td3);
                    t_tr0.appendChild(t_td4);
                    t_tr0.appendChild(t_td4time);
                    t_tr0.appendChild(t_td5);
                    //t_tr0.appendChild(t_td6);
                    t_tr0.appendChild(t_td7);
                    t_tr0.appendChild(t_td8);
                    t_tr0.appendChild(t_td9);
                    t_tr0.appendChild(t_td14);
                    t_body.appendChild(t_tr0);

                    for (i = 0; i < data[index].SubLen; i++) {
                        //console.log(data[index]['SubThread'][i].SubVar);
                        //Create head and data table for child (multi executed elements)
                        var t_tr0 = document.createElement("TR");
                        t_tr0.style.borderStyle = 'hidden';
                        t_tr0.style.height = '80%';
                        var t_td0 = document.createElement("TD");
                        //t_td0.innerHTML = data[index].tID;
                        var t_td1 = document.createElement("TD");
                        /*var td1_span = document.createElement("SPAN")
                        if (data[index].OptionGroup == "NoGroup") {
                            td1_span.setAttribute('class', 'label label-default');
                        } else {
                            td1_span.setAttribute('class', 'label label-primary');
                        }
                        td1_span.innerHTML = data[index].OptionGroup;
                        t_td1.appendChild(td1_span);*/
                        var t_td2 = document.createElement("TD");
                        /*var td2_span = document.createElement("SPAN");
                        if (l_ttype != 'NODATA') {
                            td2_span.setAttribute('class', 'label label-warning');
                        } else {
                            td2_span.setAttribute('class', 'label pull-right bg-red');
                        }
                        td2_span.innerHTML = l_ttype;
                        t_td2.appendChild(td2_span);*/
                        var t_td11 = document.createElement("TD");
                        //t_td11.innerHTML = 'TEST';
                        var t_td12 = document.createElement("TD");
                        t_td12.style.background="#ECF0F5";
                        //t_td12.innerHTML = data[index].SubVar;
                        var t_td13 = document.createElement("TD");
                        t_td13.innerHTML = 'Child';
                        t_td13.style.color = "black";
                        t_td13.style.background="#ECF0F5";
                        var t_td10 = document.createElement("TD");
                        //t_td10.innerHTML = 'TEST';
                        var t_td3_run = document.createElement("TD");
                        t_td3_run.innerHTML = data[index]['SubThread'][i].SubRun;
                        t_td3_run.style.color = "black";
                        t_td3_run.style.background="#ECF0F5";
                        var t_td3 = document.createElement("TD");
                        t_td3.innerHTML = data[index]['SubThread'][i].SubDataStart.slice(0,-13);
                        t_td3.style.color = "black";
                        t_td3.style.background="#ECF0F5";
                        var t_td4 = document.createElement("TD");
                        if (data[index].OptionStopdate == "None") {
                            /*var td4_span = document.createElement("SPAN");
                            td4_span.setAttribute('class', 'label label-warning');
                            td4_span.innerHTML = "SCHEDULED TERMINATION";
                            t_td4.appendChild(td4_span);*/
                            t_td4.innerHTML = "SCHEDULED TERMINATION";
                        } else {
                            t_td4.innerHTML = data[index]['SubThread'][i].SubDataStop.slice(0,-13);
                        }
                        t_td4.style.color = "black";
                        t_td4.style.background="#ECF0F5";
                        var t_td4time = document.createElement("TD");
                        t_td4time.innerHTML = data[index]['SubThread'][i].SubTime;
                        t_td4time.style.color = "black";
                        t_td4time.style.background="#ECF0F5";
                        var t_td5 = document.createElement("TD");
                        t_td5.innerHTML = data[index].OptionUser;
                        t_td5.style.color = "black";
                        t_td5.style.background="#ECF0F5";
                        var t_td6 = document.createElement("TD");
                        t_td6.innerHTML = data[index].OptionTest;
                        t_td6.style.color = "black";
                        t_td6.style.background="#ECF0F5";
                        var t_td7 = document.createElement("TD");
                        //Calculate the success percentage data
                        /*if (data[index].OptionPass + data[index].OptionFail != 0) {
                            var ssuc = Math.round(((data[index].OptionPass) * 100) / (data[index].OptionPass + data[index].OptionFail));
                            var sfail = Math.round(((data[index].OptionFail) * 100) / (data[index].OptionPass + data[index].OptionFail));
                        } else {
                            var ssuc = 0;
                            var sfail = 0;
                        }*/

                        var td7_span = document.createElement("SPAN");
                        td7_span.setAttribute('class', 'badge bg-green');
                        t_td7.innerHTML = data[index]['SubThread'][i].SubPass;
                        t_td7.appendChild(td7_span);
                        t_td7.style.color = "black";
                        t_td7.style.background="#ECF0F5";
                        var t_td8 = document.createElement("TD");
                        var td8_span = document.createElement("SPAN");
                        td8_span.setAttribute('class', 'badge bg-red');
                        t_td8.innerHTML = data[index]['SubThread'][i].SubFail;
                        t_td8.style.color = "black";
                        t_td8.style.background="#ECF0F5";
                        t_td8.appendChild(td8_span);
                        var t_td9 = document.createElement("TD");
                        var td9_span = document.createElement("SPAN");
                        td9_span.setAttribute('class', 'badge bg-light-blue');
                        t_td9.innerHTML = "1";
                        t_td9.style.color = "black";
                        t_td9.style.background="#ECF0F5";
                        t_td9.appendChild(td9_span);
                        var t_td14 = document.createElement("TD");
                        t_td14.innerHTML = data[index].OptionUUID;
                        t_td14.setAttribute('style', 'display: none');

                        t_tr0.appendChild(t_td0);
                        t_tr0.appendChild(t_td10);
                        t_tr0.appendChild(t_td2);
                        t_tr0.appendChild(t_td1);
                        t_tr0.appendChild(t_td11);
                        t_tr0.appendChild(t_td12);
                        t_tr0.appendChild(t_td13);
                        t_tr0.appendChild(t_td3_run);
                        t_tr0.appendChild(t_td3);
                        t_tr0.appendChild(t_td4);
                        t_tr0.appendChild(t_td4time);
                        t_tr0.appendChild(t_td5);
                        //t_tr0.appendChild(t_td6);
                        t_tr0.appendChild(t_td7);
                        t_tr0.appendChild(t_td8);
                        t_tr0.appendChild(t_td9);
                        t_tr0.appendChild(t_td14);
                        t_body.appendChild(t_tr0);
                    }


                }


           });

            var rows = t_body.rows; // or table.getElementsByTagName("tr");
            lab_proc = document.createElement("SPAN");
            lab_proc.setAttribute("id", "id_lproc");
            lab_proc.setAttribute("class", "label label-default");
            for (var i = 0; i < rows.length; i++) {
                rows[i].onclick = (function () { // closure
                    var cnt = i; // save the counter to use in the function
                    return function () {
                        t_line.style.visibility = 'visible';
                        lab_proc.innerHTML = this.cells[15].innerHTML;
                        t_lineH1.innerHTML = "TIMELINE FOR PROC. ID: " //+ this.cells[0].innerHTML;
                        t_lineH1.appendChild(lab_proc);
                        c_hold = this.cells[15].innerHTML;
                        //Now populate the t assignement area if there is anything
                        divchat = document.getElementById("chat-box");
                        document.getElementById("ccont").style.height = "0px";

                        while (divchat.firstChild) {
                          divchat.removeChild(divchat.firstChild);
                        }
                        $.ajax({
                            type: "POST",
                            url: "getass",
                            data: {'uTag':this.cells[15].innerHTML},
                            success: function (data) {

                                $.each(data, function (index) {

                                  document.getElementById("ccont").style.height = "250px";
                                  dch1 = document.createElement("div");
                                  dch1.setAttribute("class", "item");
                                  dch1.style.padding = "5px";
                                  dimg1 = document.createElement("img");
                                  dimg1.setAttribute("class", data[index].uclass);
                                  dimg1.setAttribute("src", "/static/dist/img/user4-128x128.jpg");
                                  dp1 = document.createElement("p");
                                  dp1.setAttribute("class", "message");
                                  dp1.innerHTML = data[index].anotes;
                                  dp1_1 = document.createElement("label");
                                  dp1_1.setAttribute("class", "name");
                                  dp1_1.innerHTML = data[index].usass+" -> "+data[index].usfor;
                                  dp1_1_1 = document.createElement("small");
                                  dp1_1_1.setAttribute("class", "text-muted pull-right");
                                  dp1_1_1.innerHTML = data[index].dop;
                                  dp1_1_1_1 = document.createElement("i");
                                  dp1_1_1_1.setAttribute("class", "fa fa-clock-o");
                                  //No clock icon
                                  //dp1_1_1.appendChild(dp1_1_1_1);
                                  dp1_1.appendChild(dp1_1_1);

                                  dp1.appendChild(dp1_1);

                                  dch1.appendChild(dimg1);
                                  dch1.appendChild(dp1);
                                  divchat.appendChild(dch1);

                                });

                            }
                        });
                        document.getElementById("overlay_proc").style.display = "block";
                        window.location.href = '/#tl_tit';
                        getTlineHist(c_hold, 'history');
                    }
                })(i);
            }

            var alink = t_group.getElementsByTagName("a");
            for (var i = 0; i < alink.length; i++) {
                alink[i].onclick = function fun() {
                    t_sect = this.innerHTML;
                    document.getElementById("overlay_proc").style.display = "block";
                    window.location.href = '/#c_head';
                    refHistory(j_ord,j_sign,j_search);

                }

            }
            //oCss1.appendChild(oCssSet);

        }
        });

    //If someone click the table c_old populate and the tree func is called every tab refresh time
    /*if (c_hold) {
     getTline(c_hold);
     }*/

    //setTimeout(refHistory, 10000)

}

function filterHis(tval) {
    refHistory("-id","-",tval,1);
}

function refFile() {


    //NOW THE FILE TABLE
    t_body = document.getElementById("h_file");

    //HERE WE GENERATE FOOTER GROUPPING BUTTON FROM TOTAL ROW/20
    t_group = document.getElementById("ul_group");

    //TIMELINE ELEMENTS
    t_line = document.getElementById("tline");
    t_lineH1 = GetElementInsideContainer("tl_tit", "tl_h4");

    $.ajax({
        type: "POST",
        url: "frefresh",
        data: {},
        success: function (data) {
            t_body.innerHTML = "";
            if (data) {
                t_group.innerHTML = "";
                //dlen = (data + '').length;
                dlen = data.length;
                //Create footer elements for multiple of 20
                var multipler = dlen / 20;
                console.log(multipler);
                for (i = 0; i < multipler; i++) {
                    var li_0 = document.createElement("LI");
                    newlink = document.createElement('a');
                    newlink.innerHTML = i + 1;
                    li_0.appendChild(newlink)
                    t_group.appendChild(li_0);
                }

            }



            $.each(data, function (index) {

                if (index == 0) {
                    var t_trh0 = document.createElement("TR");
                    var t_tdh0 = document.createElement("TD");
                    t_tdh0.innerHTML = 'ID'.bold();
                    var t_tdh1 = document.createElement("TD");
                    t_tdh1.innerHTML = 'Description'.bold();
                    var t_tdh2 = document.createElement("TD");
                    t_tdh2.innerHTML = 'Single File'.bold();
                    var t_tdh3 = document.createElement("TD");
                    t_tdh3.innerHTML = 'Datetime'.bold();
                    var t_tdh4 = document.createElement("TD");
                    t_tdh4.innerHTML = 'Folder'.bold();
                    var t_tdh5 = document.createElement("TD");
                    t_tdh5.innerHTML = 'Exception'.bold();


                    t_trh0.appendChild(t_tdh0);
                    t_trh0.appendChild(t_tdh1);
                    t_trh0.appendChild(t_tdh2);
                    t_trh0.appendChild(t_tdh3);
                    t_trh0.appendChild(t_tdh4);
                    t_trh0.appendChild(t_tdh5);

                    t_body.appendChild(t_trh0);

                }

                //Create head and data table
                var t_tr0 = document.createElement("TR");
                var t_td0 = document.createElement("TD");
                t_td0.innerHTML = data[index].fID;
                var t_td1 = document.createElement("TD");
                t_td1.innerHTML = data[index].fDescr;
                var t_td2 = document.createElement("TD");
                t_td2.innerHTML = data[index].fDoc;
                var t_td3 = document.createElement("TD");
                t_td3.innerHTML = data[index].fData;
                var t_td4 = document.createElement("TD");
                t_td4.innerHTML = data[index].fDpath;
                var t_td5 = document.createElement("TD");
                t_td5.innerHTML = data[index].fDmessage;
                if (data[index].fDmessage) {
                   t_tr0.style.backgroundColor = "red";
                }


                t_tr0.appendChild(t_td0);
                t_tr0.appendChild(t_td1);
                t_tr0.appendChild(t_td2);
                t_tr0.appendChild(t_td3);
                t_tr0.appendChild(t_td4);
                t_tr0.appendChild(t_td5);

                t_body.appendChild(t_tr0);


            });

            //oCss1.appendChild(oCssSet);

        }
    });

    //If someone click the table c_old populate and the tree func is called every tab refresh time
    /*if (c_hold) {
     getTline(c_hold);
     }*/

    //setTimeout(refHistory, 10000)

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//Function for add an event in jra_histiry abs
function postJraEvent(id_ev, th_id, t_pid, j_issue, j_comm, j_file) {
    //main ul for contain dynamic constructors
    //t_ultl = GetElementInsideContainer("divtl", "ultl");
    //t_ultl = document.getElementById("ultl");
    //t_btn = document.getElementById("btngrp");
    j_error = document.getElementById("laberr");
    var j_is;
    var j_com;
    j_is = document.getElementById("txt2-"+t_pid).value;
    j_com = document.getElementById("txt3-"+t_pid).value;
    if (j_is == "" || j_com == "") {
        alert("Fields Issue and Comment have to be filled in order to submit your data to jira.");
        return false;
    } else {
        $(document).ready(function () {
            var csrftoken = getCookie('csrftoken');
            //alert(csrftoken);
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
        });


        $.ajax({
            type: "POST",
            url: "/",
            data: {
                evid: id_ev,
                tid: th_id,
                tpid: t_pid,
                jissue: j_issue,
                jcom: j_comm,
                jfile: j_file,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function (data) {
                $.each(data, function (index) {
                    //If some error returned from ajax display it in label error (make css red bold ecc ecc)
                });
            }
        });
    }
}


function empty(inpval) {
    var j_is;
    var j_com;
    j_is = document.getElementById("txt2-"+inpval).value;
    j_com = document.getElementById("txt3-"+inpval).value;
    if (j_is == "") {
        alert("Enter a Valid Issue");
        return false;
    };
    if (j_com == "") {
        alert("Enter a Comment relate to your submission");
        return false;
    };
}


//Function for create an populate timeline
function fil_filters(f_name) {

    sel_call = document.getElementById(f_name);
    sel_call.options.length = 0;
    var x = document.createElement("OPTION");
    x.text = "..All";
    x.value = "..All";
    sel_call.appendChild(x);

    $.ajax({
            type: "POST",
            url: "filter_data",
            data: {
                selid: f_name
            },
            success: function (data) {
                $.each(data, function (index) {
                    var x = document.createElement("OPTION");
                    x.text = data[index].sDescr;
                    x.value = data[index].sDescr;
                    sel_call.appendChild(x);

                });

            }
        });

}


function SelUsers() {

  uluser = document.getElementById('sel_user');
  uluser.options.length = 0;
    var x = document.createElement("OPTION");
    x.text = "..All";
    x.value = "..All";
    uluser.appendChild(x);

  $.ajax({
      type: "POST",
      url: "getuser",
      data: {},
      success: function (data) {

          $.each(data, function (index) {
              var x = document.createElement("OPTION");
              x.text = data[index].uUsername;
              x.value = data[index].uUsername;
              uluser.appendChild(x);
          });


      }
  });

}

//function called from Filter button in history home
function startFilter() {
    sData = document.getElementById('reservation');
    if (sData.value.length > 0) {
        alert("OKK");
    } else {
        alert("Insert a data range");
    }
}

//Function for create an populate timeline
function getTlineHist(t_stag, f_view) {
    //main ul for contain dynamic constructors
    //t_ultl = GetElementInsideContainer("divtl", "ultl");
    t_ultl = document.getElementById("ultl");
    t_btn = document.getElementById("btngrp");

  $.ajax({
        type: "POST",
        url: "tline_mgm",
        data: {tTag: t_stag, fView: f_view},
        success: function (data) {
            //First clear the displayed timeline
            $('#ultl').empty();
            $.each(data, function (index) {
                //Red container
                var li1 = document.createElement("LI");
                li1.setAttribute("class", "time-label");
                var span1 = document.createElement("SPAN");
                span1.setAttribute("class", "bg-red");
                span1.innerHTML = data[index].t_exec;
                li1.appendChild(span1);
                //End red container
                //First Item
                var li2 = document.createElement("LI");
                var i2 = document.createElement("I");
                i2.setAttribute("class", "fa fa-envelope bg-blue");
                li2.appendChild(i2);
                var div2 = document.createElement("div");
                div2.setAttribute("class", "timeline-item");
                var span2 = document.createElement("SPAN");
                span2.setAttribute("class", "time");
                var i22 = document.createElement("I");
                i22.setAttribute("class", "fa fa-clock-o");
                span2.innerHTML = "12:20";
                span2.appendChild(i22);
                var h32 = document.createElement("H3")
                h32.setAttribute("class", "timeline-header");
                h32.innerHTML = "Titolo h3";
                var div21 = document.createElement("div");
                div21.setAttribute("class", "timeline-body");
                div21.innerHTML = "Bla bla bla many more text";
                var div22 = document.createElement("div");
                div22.setAttribute("class", "timeline-footer");
                var a2 = document.createElement("A");
                a2.setAttribute("class", "btn btn-primary btn-xs");
                a2.innerHTML = "Button";
                var a21 = document.createElement("A");
                a21.setAttribute("class", "btn btn-danger btn-xs");
                a21.innerHTML = "Button2";
                div22.appendChild(a2);
                div22.appendChild(a21);
                div2.appendChild(span2);
                div2.appendChild(h32);
                div2.appendChild(div21);
                div2.appendChild(div22);
                li2.appendChild(div2);
                //End First item
                //Second Item
                var li3 = document.createElement("LI");
                var i3 = document.createElement("I");
                i3.setAttribute("class", "fa fa-user bg-aqua");
                var div3 = document.createElement("div");
                div3.setAttribute("class", "timeline-item");
                var span3 = document.createElement("SPAN");
                span3.setAttribute("class", "time");
                var h3 = document.createElement("H3")
                h3.setAttribute("class", "timeline-header no-border");
                h3.innerHTML = data[index].t_user+" launch test";
                div3.appendChild(span3);
                div3.appendChild(h3);
                li3.appendChild(i3);
                li3.appendChild(div3);
                //End second item
                //Third item
                var li4 = document.createElement("LI");
                var i4 = document.createElement("I");
                i4.setAttribute("class", "fa fa-comments bg-yellow");
                var div4 = document.createElement("div");
                div4.setAttribute("class", "timeline-item");
                var span4 = document.createElement("SPAN");
                span4.setAttribute("class", "time");
                var i42 = document.createElement("I");
                //i42.setAttribute("class", "fa fa-clock-o");
                span4.innerHTML = data[index].th_id;
                span4.appendChild(i42);
                var h34 = document.createElement("H3")
                h34.setAttribute("class", "timeline-header");
                h34.innerHTML = "Variables and Log for: "+data[index].t_main;
                var div41 = document.createElement("div");
                div41.setAttribute("class", "timeline-body");
                textLog = document.createElement('LABEL');
                textLog.innerHTML = data[index].t_var;
                div41.appendChild(textLog);
                var div42 = document.createElement("div");
                div42.setAttribute("class", "timeline-footer");
                var a4 = document.createElement("A");
                a4.setAttribute("class", "btn btn-log btn-flat btn-xs");
                a4.setAttribute("href", "javascript:window.open('/static/out/"+data[index].t_pid+"/log.html')");
                a4.innerHTML = "Log details";
                var a5 = document.createElement("A");
                a5.setAttribute("class", "btn btn-alert btn-flat btn-xs");
                a5.setAttribute("href", "javascript:window.open('/static/out/"+data[index].t_pid+"/output.xml')");
                a5.innerHTML = "Download XML";
                //If there is Jira parameters integration
                if (data[index].t_jira) {
                    var lij1 = document.createElement("LI");
                    var ij1 = document.createElement("I");
                    ij1.setAttribute("class", "fa fa-cogs bg-green");
                    var divj1 = document.createElement("div");
                    divj1.setAttribute("class", "timeline-item");
                    var spanj1 = document.createElement("SPAN");
                    spanj1.setAttribute("class", "time");
                    var hj1 = document.createElement("H3")
                    hj1.setAttribute("class", "timeline-header");
                    hj1.innerHTML = "Jira history events";
                    //Write here previous jira insertion
                    jlab_h1 = document.createElement("LABEL");
                    jlab_h1.setAttribute("id", "labh1");
                    //jlab_h1.innerHTML = data[index].j_int.j_issue;
                    var divj2 = document.createElement("div");
                    divj2.setAttribute("class", "timeline-body");
                    //Here i do another ajax call checking if there are history modification in jira for that thread_main
                    var tabj = document.createElement("TABLE");
                    tabj.setAttribute("class", "minimalistBlack");
                    $.ajax({
                        type: "POST",
                        url: "jirapost",
                        data: {thId: data[index].th_id},
                        success: function (data) {
                            if ($.trim(data)) {
                                //Create header
                                var thj = document.createElement("THEAD");
                                var trh = document.createElement("TR");
                                var thh1 = document.createElement("TH");
                                thh1.innerHTML = 'Issue';
                                var thh2 = document.createElement("TH");
                                thh2.innerHTML = 'Comment';
                                var thh3 = document.createElement("TH");
                                thh3.innerHTML = 'With File';
                                var thh4 = document.createElement("TH");
                                thh4.innerHTML = 'Date Time';
                                var thh5 = document.createElement("TH");
                                thh5.innerHTML = 'Errors';
                                trh.appendChild(thh1);
                                trh.appendChild(thh2);
                                trh.appendChild(thh3);
                                trh.appendChild(thh4);
                                trh.appendChild(thh5);
                                thj.appendChild(trh);
                                tabj.appendChild(thj);
                            }
                            $.each(data, function (index) {
                                //Insert in table jira history data rows
                                var trj = document.createElement("TR");
                                //If error contain something row become coulored
                                if (data[index].j_err != "") {
                                    trj.style.backgroundColor = "#FF9147";
                                }
                                var tdj1 = document.createElement("TD");
                                var tdj2 = document.createElement("TD");
                                var tdj3 = document.createElement("TD");
                                var tdj4 = document.createElement("TD");
                                var tdj5 = document.createElement("TD");
                                tdj1.innerHTML = data[index].j_issue;
                                tdj2.innerHTML = data[index].j_com;
                                tdj3.innerHTML = data[index].j_file;
                                tdj4.innerHTML = data[index].j_date;
                                tdj5.innerHTML = data[index].j_err;
                                trj.appendChild(tdj1);
                                trj.appendChild(tdj2);
                                trj.appendChild(tdj3);
                                trj.appendChild(tdj4);
                                trj.appendChild(tdj5);
                                tabj.appendChild(trj);
                            });
                        }
                    });
                    divj2.appendChild(tabj);
                    if (data[index].j_set != "") {
                        //JIRA EVENT SUBSCRIPTION FORM START
                        var divj3 = document.createElement("div");
                        divj3.setAttribute("class", "timeline-body");
                        var divj3_2 = document.createElement("div");
                        divj3_2.setAttribute("class", "col-md-6");
                        var divj3_3 = document.createElement("div");
                        divj3_3.setAttribute("class", "box box-primary");
                        //Now i create form for jira event submission
                        var divjh = document.createElement("div");
                        divjh.setAttribute("class", "box-header");
                        var jh3t = document.createElement("H3");
                        jh3t.setAttribute("class", "box-title");
                        jh3t.innerHTML = "Submit to jira";
                        divjh.appendChild(jh3t);
                        divj3_3.appendChild(divjh);

                        var jfrm = document.createElement("FORM");
                        jfrm.method = "post";

                        var divjf1 = document.createElement("div");
                        divjf1.setAttribute("class", "box-body");
                        var divjf2 = document.createElement("div");
                        divjf2.setAttribute("class", "form-group");
                        jlab1 = document.createElement("LABEL");
                        jlab1.innerHTML = "Jira Issue";
                        jtx2 = document.createElement("INPUT");
                        jtx2.setAttribute("id", "txt2-"+data[index].t_pid);
                        jtx2.setAttribute("class", "form-control");
                        divjf2.appendChild(jlab1);
                        divjf2.appendChild(jtx2);
                        divjf1.appendChild(divjf2);
                        var divjf3 = document.createElement("div");
                        divjf3.setAttribute("class", "form-group");
                        jlab2 = document.createElement("LABEL");
                        jlab2.innerHTML = "Comment";
                        jtx3 = document.createElement("TEXTAREA");
                        jtx3.setAttribute("id", "txt3-"+data[index].t_pid);
                        jtx3.setAttribute("class", "form-control");
                        divjf3.appendChild(jlab2);
                        divjf3.appendChild(jtx3);
                        divjf1.appendChild(divjf3);
                        var divjf4 = document.createElement("div");
                        divjf4.setAttribute("class", "checkbox");
                        jlab3 = document.createElement("LABEL");
                        jlab3.innerHTML = "Attach log file";
                        jlab3.setAttribute("style", "width:16%; display:inline-block; padding-left:0px;");
                        jtx5 = document.createElement("INPUT");
                        jtx5.setAttribute("type", "checkbox");
                        jtx5.checked = true;
                        jtx5.setAttribute("id", "txt5-"+data[index].t_pid);
                        jtx5.setAttribute("style", "width:5%; display:inline-block;");
                        divjf4.appendChild(jlab3);
                        divjf4.appendChild(jtx5);
                        divjf1.appendChild(divjf4);
                        var divjf5 = document.createElement("div");
                        divjf5.setAttribute("class", "box-footer");
                        var jbut1 = document.createElement("INPUT");
                        jbut1.setAttribute("type", "submit");
                        jbut1.setAttribute("class", "btn btn-primary");
                        jbut1.innerHTML = "Submit to jira";
                        jbut1.onclick = function() { alert('The information was sent to the Jira server. Check the result in the aida thread details.'); };
                        divjf5.appendChild(jbut1);
                        divjf1.appendChild(divjf5);
                        jfrm.appendChild(divjf1);
                        divj3_3.appendChild(jfrm);
                        divj3_2.appendChild(divj3_3);
                        divj3.appendChild(divj3_2);

                        jfrm.addEventListener ("submit", function() {
                            postJraEvent(data[index].t_id, data[index].th_id, data[index].t_pid, document.getElementById('txt2-'+data[index].t_pid).value,document.getElementById('txt3-'+data[index].t_pid).value,document.getElementById('txt5-'+data[index].t_pid).checked);
                        });
                    }
                    divj1.appendChild(spanj1);
                    divj1.appendChild(hj1);
                    divj1.appendChild(divj2);
                    divj1.appendChild(divj3);
                }
                div42.appendChild(a4);
                div42.appendChild(a5);
                div4.appendChild(span4);
                div4.appendChild(h34);
                div4.appendChild(div41);
                div4.appendChild(div42);
                li4.appendChild(i4);
                li4.appendChild(div4);

                //End Third item
                t_ultl.appendChild(li1);
                //t_ultl.appendChild(li2);
                t_ultl.appendChild(li3);
                t_ultl.appendChild(li4);
                if (data[index].t_jira) {
                    lij1.appendChild(ij1);
                    lij1.appendChild(divj1);
                    t_ultl.appendChild(lij1);
                }
                //alert(data[index].t_exec);
                p_proc = data[index].t_pid;
            });
        //Create the buttons in tline head for raw html and other
            try {
            $('#btngrp').empty();
        var btnLeft2 = document.createElement("A");
        btnLeft2.setAttribute("class", "btn btn-warning btn-flat btn-xs");
        btnLeft2.setAttribute("href", "javascript:window.open('/static/out/"+p_proc+"/"+p_proc+"_TC.html')");
        btnLeft2.innerHTML = "Test Structure";
        t_btn.appendChild(btnLeft2);
        }
            catch(err) {
                console.log(err.message);
            }
        }
    });

}

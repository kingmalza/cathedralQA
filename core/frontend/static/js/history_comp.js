//Global varc(BP) for know witch one button for record portion display was used
var t_sect = 1

function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}


function refHistory(j_ord, j_sign, j_search, is_search) {
    j_search = document.getElementById("txthis").value;
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


    $.ajax({
        type: "POST",
        url: "hrefresh",
        data: {tab_slice: t_sect, tab_ord: j_ord, tab_search: j_search, isearch: is_search},
        success: function (data) {
            t_body.innerHTML = "";
            if (data) {
                t_group.innerHTML = "";
                //dlen = (data + '').length;
                dlen = data[data.length-1];
                //Create footer elements for multiple of 20
                
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
                    t_tr0.appendChild(t_td3);
                    t_tr0.appendChild(t_td4);
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
                    //label for test type
                console.log('OptionType-->'+data[index].OptionType);
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
                var t_td5 = document.createElement("TD");
                t_td5.innerHTML = data[index].OptionUser;
                var t_td6 = document.createElement("TD");
                t_td6.innerHTML = data[index].OptionTest;
                var t_td7 = document.createElement("TD");
                //Calculate the success percentage data
                if (data[index].OptionPass + data[index].OptionFail != 0) {
                    var ssuc = ((data[index].OptionPass) * 100) / (data[index].OptionPass + data[index].OptionFail);
                    var sfail = ((data[index].OptionFail) * 100) / (data[index].OptionPass + data[index].OptionFail);
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
                t_tr0.appendChild(t_td3);
                t_tr0.appendChild(t_td4);
                t_tr0.appendChild(t_td5);
                //t_tr0.appendChild(t_td6);
                t_tr0.appendChild(t_td7);
                t_tr0.appendChild(t_td8);
                t_tr0.appendChild(t_td9);
                t_tr0.appendChild(t_td14);
                t_body.appendChild(t_tr0);
                }


           });

            var rows = t_body.rows; // or table.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {
                rows[i].onclick = (function () { // closure
                    var cnt = i; // save the counter to use in the function
                    return function () {
                        t_line.style.visibility = 'visible';
                        t_lineH1.innerHTML = "TIMELINE FOR PROC. ID: " + this.cells[0].innerHTML;
                        c_hold = this.cells[13].innerHTML;
                        getTlineHist(c_hold);
                    }
                })(i);
            }

            var alink = t_group.getElementsByTagName("a");
            for (var i = 0; i < alink.length; i++) {
                alink[i].onclick = function fun() {
                    t_sect = this.innerHTML;
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


//Function for create an populate timeline
function getTlineHist(t_stag) {
    //main ul for contain dynamic constructors
    //t_ultl = GetElementInsideContainer("divtl", "ultl");
    t_ultl = document.getElementById("ultl");
    t_btn = document.getElementById("btngrp");


  $.ajax({
        type: "POST",
        url: "tline_mgm",
        data: {tTag: t_stag},
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
                i42.setAttribute("class", "fa fa-clock-o");
                span4.innerHTML = "12:20";
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
                a4.setAttribute("class", "btn btn-warning btn-flat btn-xs");
                a4.setAttribute("href", "javascript:window.open('/static/out/"+data[index].t_pid+"/log.html')");
                a4.innerHTML = "Log details";
                div42.appendChild(a4);
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
                //alert(data[index].t_exec);
                p_proc = data[index].t_pid;
            });
        //Create the buttons in tline head for raw html and other
        $('#btngrp').empty();
        var btnLeft2 = document.createElement("A");
        btnLeft2.setAttribute("class", "btn btn-warning btn-flat btn-xs");
        btnLeft2.setAttribute("href", "javascript:window.open('/static/out/"+p_proc+"/"+p_proc+"_TC.html')");
        btnLeft2.innerHTML = "RAW Html";
        t_btn.appendChild(btnLeft2);
        }
    });

}



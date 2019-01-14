//Global (Bad practiche) var used in refTable for check if a row was clicked
var c_hold;
var p_proc;
//Global for interactive live graph
var data = [], totalPoints = 100, intstart = 0;

/*var imported = document.createElement('script');
imported.src = '/static/plugins/sparkline/jquery.sparkline.min.js';
document.head.appendChild(imported);*/

function selSched(selVal) {

    sVal = document.getElementById("sched_val");
    sVal.value = '';
    sVal.style.backgroundColor = "";
    sVal.placeholder = "Schedule data input";
    sVal.disabled = true;
    if (selVal.value == 'everymin' || selVal.value == 'everyday' || selVal.value == 'everyhour') {
        sVal.style.backgroundColor = "yellow";
        if (selVal.value == 'everymin') {
            sVal.disabled = false;
            sVal.placeholder = "Insert minutes amount e.g. 10, 20, 40 ecc";
        } else if (selVal.value == 'everyday') {
            sVal.disabled = false;
            sVal.placeholder = "Insert day hour e.g. 10:30";
        } else if (selVal.value == 'everyhour') {
            sVal.innerHTML="";
            sVal.disabled = true;
            sVal.placeholder = "No data need, run every hou from now";
        } else {
            sVal.placeholder = "No data need";
            sVal.disabled = true;
        }
    }
}

function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}


$(document).ajaxStop(function () {
    //alert('STOP');
    document.getElementById("overlay_proc").style.display = "none";
    document.getElementById("overlay").style.display = "none";
});


function refTable() {
    //j_search = document.getElementById("txthish").value;
    j_search = null;
    j_sord = document.getElementById("txtsord").value;
    issearch = document.getElementById("txtsign").value;

    if (j_sord == null || j_sord == "") {
        j_sord = 'OptionID';
    }
    if (j_search == null || j_search == 0) {
        j_search = 'noSearch';
    }
    if (issearch == null) {
        issearch = '-';
    }
    //console.log(j_sord);

    //alert(j_search+"--"+j_sord+"--"+issearch);

    t_threads = document.getElementById("tab_threads");
    //Activate timeline for specific thread on active thread onclick in table
    t_line = document.getElementById("tline");
    t_lineH1 = GetElementInsideContainer("tl_tit", "tl_h4");
    t_graph = document.getElementById("int_div");
    t_launch = document.getElementById("t_launch");

    $.ajax({
        type: "POST",
        url: "trefresh",
        data: {tab_ord: j_sord, tab_search: j_search, isearch: issearch},
        success: function (data) {
            t_threads.innerHTML = "";
            var t_count = 0;
            $.each(data, function (index) {

                if (index == 0) {
                    var t_tr0 = document.createElement("TR");
                    var t_td0 = document.createElement("TD");
                    t_td0.innerHTML = 'ID'.bold();
                    t_td0.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionID';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionID';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td9 = document.createElement("TD");
                    t_td9.innerHTML = 'Test Name'.bold();
                    t_td9.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionName';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionName';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td10 = document.createElement("TD");
                    t_td10.innerHTML = 'Test Type'.bold();
                    t_td10.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionType';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionType';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td11 = document.createElement("TD");
                    t_td11.innerHTML = 'Test Group'.bold();
                    t_td11.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionGroup';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionGroup';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td12 = document.createElement("TD");
                    t_td12.innerHTML = 'Schedule Type'.bold();
                    t_td12.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionSched';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionSched';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td13 = document.createElement("TD");
                    t_td13.innerHTML = 'Schedule Value'.bold();
                    t_td13.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionSchedVal';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionSchedVal';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td1 = document.createElement("TD");
                    t_td1.innerHTML = 'Thread'.bold();
                    t_td1.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionID';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionID';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td2 = document.createElement("TD");
                    t_td2.innerHTML = 'Status'.bold();
                    t_td2.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionStatus';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionStatus';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td3 = document.createElement("TD");
                    t_td3.innerHTML = 'TAG'.bold();
                    t_td3.setAttribute('id', 'tag_h');
                    t_td3.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionUUID';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionUUID';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td4 = document.createElement("TD");
                    t_td4.innerHTML = 'Start'.bold();
                    t_td4.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionSdate';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionSdate';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td5 = document.createElement("TD");
                    t_td5.innerHTML = 'User'.bold();
                    t_td5.onclick = function () {
                        if (issearch == '-') {
                            document.getElementById("txtsord").value = 'OptionUser';
                            document.getElementById("txtsign").value = '+';
                            refTable();
                        } else {
                            document.getElementById("txtsord").value = 'OptionUser';
                            document.getElementById("txtsign").value = '-';
                            refTable();
                        }
                        ;
                    };
                    var t_td6 = document.createElement("TD");
                    t_td6.innerHTML = 'Pid';
                    var t_td7 = document.createElement("TD");
                    t_td7.innerHTML = 'Cycles';
                    var t_td8 = document.createElement("TD");
                    t_td8.innerHTML = 'Going';

                    t_tr0.appendChild(t_td0);
                    t_tr0.appendChild(t_td9);
                    t_tr0.appendChild(t_td10);
                    t_tr0.appendChild(t_td11);
                    t_tr0.appendChild(t_td12);
                    t_tr0.appendChild(t_td13);
                    t_tr0.appendChild(t_td1);
                    t_tr0.appendChild(t_td2);
                    t_tr0.appendChild(t_td3);
                    t_tr0.appendChild(t_td4);
                    t_tr0.appendChild(t_td5);
                    t_tr0.appendChild(t_td6);
                    t_tr0.appendChild(t_td7);
                    t_tr0.appendChild(t_td8);

                    t_threads.appendChild(t_tr0);

                    //Hide tag column, don't remove it, is for identification purposes
                    document.getElementById('tag_h').style.display = 'none';

                }

                t_count = t_count + 1;
                //Create head and data table
                var t_tb = document.createElement('tbody');
                var t_tr = document.createElement("TR");
                var t_td0 = document.createElement("TD");
                t_td0.innerHTML = data[index].tID;
                var t_td9 = document.createElement("TD");
                t_td9.innerHTML = data[index].OptionName;
                var t_td10 = document.createElement("TD");
                t_td10.innerHTML = data[index].OptionType;
                var t_td11 = document.createElement("TD");
                t_td11.innerHTML = data[index].OptionGroup;
                var t_td12 = document.createElement("TD");
                t_td12.innerHTML = data[index].OptionSched;
                var t_td13 = document.createElement("TD");
                t_td13.innerHTML = data[index].OptionSchedVal;
                var t_td1 = document.createElement("TD");
                t_td1.innerHTML = data[index].OptionID;
                var t_td2 = document.createElement("TD");
                t_td2.innerHTML = data[index].OptionUUID;
                t_td2.setAttribute('style', 'display: none');
                var t_td3 = document.createElement("TD");
                t_td3.innerHTML = data[index].OptionSdate;
                var t_td4 = document.createElement("TD");
                t_td4.innerHTML = data[index].OptionUser;
                var t_td5 = document.createElement("TD");
                var td5_span = document.createElement("SPAN");
                td5_span.setAttribute('class', 'label label-success');
                td5_span.innerHTML = data[index].OptionStatus;
                t_td5.appendChild(td5_span);
                var t_td6 = document.createElement("TD");
                t_td6.innerHTML = data[index].OptionTest;
                var t_td7 = document.createElement("TD");
                var td7_span = document.createElement("SPAN");
                td7_span.setAttribute('class', 'badge bg-light-blue');
                td7_span.innerHTML = data[index].OptionNumT;
                t_td7.appendChild(td7_span);
                var t_td8 = document.createElement("TD");
                var g_span_data = document.createElement("SPAN");
                g_span_data.setAttribute('class', 'sparktristate');
                g_span_data.id = "inL";
                var t = document.createTextNode(data[index].InlineData);
                g_span_data.appendChild(t);
                t_td8.appendChild(g_span_data);
                t_tr.appendChild(t_td0);
                t_tr.appendChild(t_td9);
                t_tr.appendChild(t_td10);
                t_tr.appendChild(t_td11);
                t_tr.appendChild(t_td12);
                t_tr.appendChild(t_td13);
                t_tr.appendChild(t_td1);
                t_tr.appendChild(t_td5);
                t_tr.appendChild(t_td2);
                t_tr.appendChild(t_td3);
                t_tr.appendChild(t_td4);
                t_tr.appendChild(t_td6);
                t_tr.appendChild(t_td7);
                t_tr.appendChild(t_td8);

                //t_tb.appendChild(t_trh);
                t_tb.appendChild(t_tr);
                t_threads.appendChild(t_tb);
                //document.getElementById('tag_hv').style.display = 'none';
                //Launch the function for render inline graph
                drawDocSparklines(data[index].InlineData);

            });

            if (t_count > 0) {
                //Start graph creation only if isn't already started
                if (intstart == 0) {
                    //Create interactively the graph node
                    var int1 = document.createElement("DIV");
                    int1.style.height = "300px";
                    int1.id = "interactive"
                    t_graph.appendChild(int1);
                    intstart = 1;
                    goInteractive();
                }
            } else {
                if (t_graph.hasChildNodes()) {
                    t_graph.removeChild(t_graph.childNodes[0]);
                }
                intstart = 0;
            }

            var rows = t_threads.rows; // or table.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {
                rows[i].onclick = (function () { // closure
                    var cnt = i; // save the counter to use in the function
                    return function () {
                        task_det(this.cells[0].innerHTML, this.cells[8].innerHTML);
                        t_line.style.visibility = 'visible';
                        t_lineH1.innerHTML = "LAST FIVE TIMELINE EVENTS FOR PROC. ID: " + this.cells[0].innerHTML;
                        c_hold = this.cells[8].innerHTML;
                        document.getElementById("overlay_proc").style.display = "block";
                        getTline(c_hold,'active');
                    }
                })(i);
            }
            //oCss1.appendChild(oCssSet);

        }
    });

    //If someone click the table c_old populate and the tree func is called every tab refresh time
    if (c_hold) {
        getTline(c_hold,'active');
    }

    setTimeout(refTable, 5000)

}

//-----GRAPH FUNCTIONS----------
//Launch the function for render the inline graph PASS/FAIL
function drawDocSparklines(dataIn) {

    $(".sparkline").each(function () {
        var $this = $(this);
        //$this.sparkline('html', $this.data());
        $("#inL").sparkline('html', dataIn);
    });

    $('.sparktristate').sparkline('html', {type: 'tristate'});

}

function getRandomData() {

    if (data.length > 0)
        data = data.slice(1);

    // Do a random walk
    while (data.length < totalPoints) {

        var prev = data.length > 0 ? data[data.length - 1] : 50,
            y = prev + Math.random() * 10 - 5;

        if (y < 0) {
            y = 0;
        } else if (y > 100) {
            y = 100;
        }

        data.push(y);
    }

    // Zip the generated y values with the x values
    var res = [];
    for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]]);
    }

    return res;
}

function goInteractive() {

    var interactive_plot = $.plot("#interactive", [getRandomData()], {
        grid: {
            borderColor: "#f3f3f3",
            borderWidth: 1,
            tickColor: "#f3f3f3"
        },
        series: {
            shadowSize: 0, // Drawing is faster without shadows
            color: "#3c8dbc"
        },
        lines: {
            fill: true, //Converts the line chart to area chart
            color: "#3c8dbc"
        },
        yaxis: {
            min: 0,
            max: 100,
            show: true
        },
        xaxis: {
            show: true
        }
    });

    var updateInterval = 500; //Fetch data ever x milliseconds
    var realtime = "on"; //If == to on then fetch data every x seconds. else stop fetching
    function update() {

        interactive_plot.setData([getRandomData()]);

        // Since the axes don't change, we don't need to call plot.setupGrid()
        interactive_plot.draw();
        if (realtime === "on")
            setTimeout(update, updateInterval);
    }

    //INITIALIZE REALTIME DATA FETCHING
    if (realtime === "on") {
        update();
    }
    //REALTIME TOGGLE
    $("#realtime .btn").click(function () {
        if ($(this).data("toggle") === "on") {
            realtime = "on";
        }
        else {
            realtime = "off";
        }
        update();
    });
}

//----------END GRAPH-----------


//Function for create an populate timeline
function getTline(t_stag, f_view) {
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
                h3.innerHTML = data[index].t_user + " launch test";
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
                span4.innerHTML = "";
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
                a4.setAttribute("href", "javascript:window.open('/static/out/" + data[index].t_pid + "/log.html')");
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
            btnLeft2.setAttribute("href", "javascript:window.open('/static/out/" + p_proc + "/" + p_proc + "_TC.html')");
            btnLeft2.innerHTML = "RAW Html";
            t_btn.appendChild(btnLeft2);
        }
    });

}

function countElem() {

    tc_count = document.getElementById("tcnum");
    ta_count = document.getElementById("tanum");
    tk_count = document.getElementById("tknum");

    $.ajax({
        type: "POST",
        url: "elemcount",
        data: {},
        success: function (data) {
            tc_count.innerHTML = "";
            ta_count.innerHTML = "";
            tk_count.innerHTML = "";
            $.each(data, function (index) {
                tc_count.innerHTML = data[index].TCnum;
                ta_count.innerHTML = data[index].TAnum;
                tk_count.innerHTML = data[index].TKnum;
            });


        }
    });

    setTimeout(countElem, 10000)

}

function task_det(dataID, threadUUid) {


    oBtnt = document.getElementById("stop_btn");
    oBtnt.onclick = function () {
        stopThread(threadUUid);
    }

}

function stopThread(tDet) {
    document.getElementById("overlay_stop").style.display = "block";
    //DeActivate timeline for specific thread on active thread onclick in table
    t_line = document.getElementById("tline");
    console.log("TDET: "+tDet)

    $.ajax({
        type: "POST",
        url: "thread_stopper",
        data: {tData: tDet},
        success: function (data) {
            //oThread.innerHTML = "";
            $.each(data, function (index) {
                oThread.value = data[index].thethread;
                if (data[index].userKo) {
                    alert("User not authorized!")
                }
            });

        },
        complete: function (data) {
            t_line.style.visibility = 'hidden';
            document.getElementById("overlay_stop").style.display = "none";
        }
    });
}


        
  
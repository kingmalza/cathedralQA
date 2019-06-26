function seltemp() {
    oCtemplates = document.getElementById("t_select");


    $.ajax({
        type: "POST",
        url: "test_type",
        data: {selType: "ST"},
        success: function (data) {
            //oCssSet.style.visibility = visible;

            $.each(data, function (index) {


                var opt = document.createElement("option");
                opt.value = data[index].selID;
                opt.innerHTML = data[index].selDescr;

                oCtemplates.appendChild(opt);

            });

        }
    });
}


function get_tab() {

    oTabData = document.getElementById("tab_body");

    $.ajax({
        type: "POST",
        url: "getassist",
        data: {t_status: "E"},
        success: function (data) {

            $.each(data, function (index) {

                var tr_exp = document.createElement("TR");
                var td_exp_1 = document.createElement("TD");
                var td_exp_2 = document.createElement("TD");
                var td_exp_3 = document.createElement("TD");
                var td_exp_3_e = document.createElement("TD");
                var td_exp_4 = document.createElement("TD");
                var td_exp_5 = document.createElement("TD");

                var t_td9 = document.createElement("SPAN");
                t_td9.setAttribute('class', 'label label-default');
                t_td9.innerHTML = data[index].rl_id;
                td_exp_1.appendChild(t_td9);
                td_exp_1.value = data[index].rl_id;
                td_exp_2.value = data[index].rl_desc;
                td_exp_2.innerHTML = data[index].rl_desc;
                td_exp_3.value = data[index].rl_dt;
                td_exp_3.innerHTML = data[index].rl_dt;
                td_exp_3_e.value = data[index].rl_dt_end;
                td_exp_3_e.innerHTML = data[index].rl_dt_end;
                td_exp_4.value = data[index].rl_status;
                var t_td7 = document.createElement("SPAN");
                if (data[index].rl_status == 'P') {
                    t_td7.setAttribute('class', 'label label-warning');
                    t_td7.innerHTML = 'PENDING';
                    td_exp_4.appendChild(t_td7);
                } else if (data[index].rl_status == 'A') {
                    t_td7.setAttribute('class', 'label label-primary');
                    t_td7.innerHTML = 'APPROVED';
                    td_exp_4.appendChild(t_td7);
                } else if (data[index].rl_status == 'R') {
                    t_td7.setAttribute('class', 'label pull-right bg-red');
                    t_td7.innerHTML = 'REJECTED';
                    td_exp_4.appendChild(t_td7);
                } else if (data[index].rl_status == 'E') {
                    t_td7.setAttribute('class', 'label label-default');
                    t_td7.innerHTML = 'ENDED';
                    td_exp_4.appendChild(t_td7);
                } else {
                    td_exp_4.innerHTML = 'UNKNOWN';
                }

                td_exp_5.value = data[index].rl_scredits;
                var t_td8 = document.createElement("SPAN");
                t_td8.setAttribute('class', 'badge bg-green');
                t_td8.innerHTML = data[index].rl_scredits;;
                td_exp_5.appendChild(t_td8);


                tr_exp.appendChild(td_exp_1);
                tr_exp.appendChild(td_exp_2);
                tr_exp.appendChild(td_exp_3);
                tr_exp.appendChild(td_exp_3_e);
                tr_exp.appendChild(td_exp_4);
                tr_exp.appendChild(td_exp_5);
                oTabData.appendChild(tr_exp);

            });

            var rows = oTabData.rows; // or table.getElementsByTagName("tr");
            for (var i = 0; i < rows.length; i++) {
                rows[i].onclick = (function () { // closure
                    var cnt = i; // save the counter to use in the function
                    return function () {
                        document.getElementById("p_det").style.display = "block";
                        window.location.href = '/tpublish#p_det';
                        //Start create management session
                        document.getElementById("t_det").innerHTML = this.cells[0].value;
                    }
                })(i);
            }

            }


    });
}

function clicktemp(tID) {

    oDetTempl = document.getElementById("t_details");
    //Relative to details area after template selection
    oDetDescr = document.getElementById("det_descr");
    oDetNotes = document.getElementById("det_notes");
    oDetDt = document.getElementById("det_dt");
    oDetType = document.getElementById("det_type");
    oDetID = document.getElementById("id_test");


    $.ajax({
        type: "POST",
        url: "test_single",
        data: {idTemp: tID},
        success: function (data) {
            oDetTempl.style.visibility = 'visible';

            $.each(data, function (index) {

                oDetDescr.innerHTML = "";
                oDetDescr.innerHTML = data[index].selDescr;
                oDetNotes.innerHTML = "";
                oDetNotes.innerHTML = data[index].OptionNote;
                //oDetDt.innerHTML = "";
                oDetDt.value = data[index].OptionDt;
                oDetType.value = "";
                oDetType.value = data[index].OptionTtype;
                oDetID.value = tID;

            });

        }
    });
}


function isempty() {
    var r_1;
    var r_2;
    var r_3;


    r_1 = document.getElementById("t_select");
    r_2 = document.getElementById("t_descr");
    r_cover = document.getElementById("t_cover");
    r_price = document.getElementById("t_price");
    r_3 = document.getElementById("t_terms");

    if((r_1.value == "Please select...") || (r_2.value == "") || (r_3.checked == false)) {
        alert("Please fill in all the form fields including the terms of use to proceed with the publication");
        return false;
    } else {

        //Start exporting template
        $.ajax({
        type: "POST",
        url: "export_templ",
        data: {idTempl: document.getElementById("id_test").value,
            tDescr: r_2.value,
            tCover: r_cover.value,
            tPrice: r_price.value},
        success: function (data) {
            $.each(data, function (index) {

                } );

            }
        });
    }

}



function activate() {

    var a_1;

    a_1 = document.getElementById("act_code");


    if(a_1.value == "") {
        alert("Please enter the activation number received by email");
        return false;
    }

}


function redirect() {
  window.location.replace("https://cathedral.ai/licensing/");
  return false;
}
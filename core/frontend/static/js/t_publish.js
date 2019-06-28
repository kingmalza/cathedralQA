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

                //Hidden td for retreive in click
                var td_h_1 = document.createElement("TD");
                var td_h_2 = document.createElement("TD");

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
                t_td8.innerHTML = data[index].rl_scredits;
                td_exp_5.appendChild(t_td8);

                td_h_1.value = data[index].rl_sdescr
                if (data[index].rl_sdescr.length > 15) {
                    td_h_1.innerHTML = data[index].rl_sdescr.substr(0, 15) + "\u2026";
                } else {
                    td_h_1.innerHTML = data[index].rl_sdescr;
                }
                td_h_2.value = data[index].rl_scover;
                td_h_2.innerHTML = data[index].rl_scover;


                tr_exp.appendChild(td_exp_1);
                tr_exp.appendChild(td_exp_2);
                tr_exp.appendChild(td_exp_3);
                tr_exp.appendChild(td_exp_3_e);
                tr_exp.appendChild(td_exp_4);
                tr_exp.appendChild(td_exp_5);

                tr_exp.appendChild(td_h_1);
                tr_exp.appendChild(td_h_2);

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
                        document.getElementById("t_det_e").innerHTML = this.cells[6].value;
                        document.getElementById("t_cov_e").value = this.cells[7].value.trim();
                        if (this.cells[4].value == 'A') {
                            document.getElementById("t_price_e").disabled = true;
                        } else {
                             if (this.cells[4].value == 'E' || this.cells[4].value == 'R') {
                                document.getElementById("t_mod_but").style.visibility = 'hidden';
                             } else {
                                 document.getElementById("t_mod_but").style.visibility = 'visible';
                             }
                            document.getElementById("t_price_e").disabled = false;
                        }
                        document.getElementById("t_price_e").value = this.cells[5].value;

                        //Change message in callout regarding the template status
                        //First clena div
                        e = document.getElementById("pub_msg");
                        var child = e.lastElementChild;
                        while (child) {
                            e.removeChild(child);
                            child = e.lastElementChild;
                        }

                        var th_4 = document.createElement("H4");
                        var p_1 = document.createElement("P");

                        if (this.cells[4].value.trim() == 'E') {
                            th_4.innerHTML = "template rejected";
                            p_1.innerHTML = "Perche ta set mia bu";
                        } else if (this.cells[4].value.trim() == 'P') {
                           th_4.innerHTML = "template Pending";
                           p_1.innerHTML = "We are waiting to review your template";
                        }
                        e.appendChild(th_4);
                        e.appendChild(p_1);
                    }
                })(i);
            }

            }
    });
}


function pend(a_type) {

    idT = document.getElementById("t_det").innerHTML;
    t_descr = document.getElementById("t_det_e").value;
    t_cover = document.getElementById("t_cov_e").value;
    t_credit = document.getElementById("t_price_e").value;
    if (a_type == 'end') {
        conf_msg = 'Are you sure you want to END this template pubblication?';
    } else {
        conf_msg = 'Are you sure you want to UPDATE this template pubblication data?'
    }


        if (confirm(conf_msg)) {
            if ((document.getElementById("t_det_e").value !="" && t_cover != "" && t_credit != "")||(a_type == 'end')) {
                $.ajax({
                    type: "POST",
                    url: "end_templ",
                    data: {
                        idTemp: idT,
                        atype: a_type,
                        tdescr: t_descr,
                        tcover: t_cover,
                        tcredit: t_credit
                    },
                    success: function (data) {
                        //oDetTempl.style.visibility = 'visible';

                        $.each(data, function (index) {
                            alert(data[index].res);
                            window.location.href = '/tpublish';
                        });

                    }
                });
            } else {
                alert("Please fill all form fields for update subscription.");
                return false;
            }
        }
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
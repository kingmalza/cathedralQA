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
                    t_td7.setAttribute('class', 'label label-danger');
                    t_td7.innerHTML = 'REJECTED';
                    td_exp_4.appendChild(t_td7);
                } else if (data[index].rl_status == 'E') {
                    t_td7.setAttribute('class', 'label label-default');
                    t_td7.innerHTML = 'ENDED';
                    td_exp_4.appendChild(t_td7);
                } else {
                    td_exp_4.innerHTML = 'UNKNOWN';
                }


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
                        document.getElementById("t_det_e").innerHTML = this.cells[5].value;
                        document.getElementById("t_cov_e").value = this.cells[6].value.trim();
                        if (this.cells[4].value == 'A') {
                            document.getElementById("t_mod_but").style.visibility = 'visible';
                        } else {
                             if (this.cells[4].value == 'E' || this.cells[4].value == 'R') {
                                document.getElementById("t_mod_but").style.visibility = 'hidden';
                             } else {
                                 document.getElementById("t_mod_but").style.visibility = 'visible';
                             }
                        }

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

                        var snotes = "";

                        if (this.cells[4].value.trim() == 'E') {
                            th_4.innerHTML = "TEMPLATE ENDED";
                            p_1.innerHTML = "This template is not active on the Cathedral marketplace and can no longer be managed because it is terminated by the user.<br>To be able to publish it again on the marketplace it is necessary to carry out a new publication procedure.";
                        } else if (this.cells[4].value.trim() == 'P') {
                           th_4.innerHTML = "APPROVAL PENDING";
                           p_1.innerHTML = "The template is being approved by the technical staff of Cathedral.<br>You can modify or end the publication of the template at any time.";
                        } else if (this.cells[4].value.trim() == 'A') {
                           th_4.innerHTML = "TEMPLATE ACTIVE ON MARKETPLACE";
                           p_1.innerHTML = "The template is currently active and can be purchased from the Cathedral marketplace.<br>You can modify the publication data of the template but the template will return to Pending status for validation by the Cathedral staff and will not be present on the marketplace until further approval.";
                        } else if (this.cells[4].value.trim() == 'R') {
                            //Ajax call for retreice rejected notes
                            $.ajax({
                                type: "POST",
                                url: "getassist",
                                data: {t_status: this.cells[0].value},
                                success: function (data) {
                                    //oCssSet.style.visibility = visible;

                                    $.each(data, function (index) {

                                        var snotes = data[index].rl_staffn;
                                        th_4.innerHTML = "PUBLICATION REJECTED";
                                        p_1.innerHTML = "The publication of the template has been rejected for the following reason:<br><strong>"+snotes+"</strong>";

                                    });

                                }
                            });

                        } else {
                            th_4.innerHTML = "...OTHER";
                           p_1.innerHTML = "The selected template is being investigated by the Cathedral staff.";
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
    if (a_type == 'end') {
        conf_msg = 'Are you sure you want to END this template pubblication?';
    } else {
        conf_msg = 'Are you sure you want to UPDATE this template pubblication data?'
    }


        if (confirm(conf_msg)) {
            if ((document.getElementById("t_det_e").value !="" && t_cover != "")||(a_type == 'end')) {
                $.ajax({
                    type: "POST",
                    url: "end_templ",
                    data: {
                        idTemp: idT,
                        atype: a_type,
                        tdescr: t_descr,
                        tcover: t_cover,
                        tadvimg: document.getElementById("t_adv_img").value,
                        tadvdesc: document.getElementById("t_adv_desc").value.substring(0,200),
                        tadvurl: document.getElementById("t_adv_url").value
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


function HTMLEncode(str) {
    var i = str.length,
        aRet = [];

    while (i--) {
        var iC = str[i].charCodeAt();
        if (iC < 65 || iC > 127 || (iC>90 && iC<97)) {
            aRet[i] = '&#'+iC+';';
        } else {
            aRet[i] = str[i];
        }
    }
    return aRet.join('');
}

function isempty() {

    var r_1;
    var r_2;
    var r_3;
    var r_err="";
    var r_lic="";


    r_1 = document.getElementById("t_pre");
    r_2 = document.getElementById("t_step");
    r_3 = document.getElementById("t_exp");
    r_4 = document.getElementById("t_desc");

    r_5 = document.getElementById("t_terms");

    if((r_1.value == "") || (r_2.value == "") || (r_3.value == "") || (r_4.value == "") || (r_5.checked == false)) {
        alert("Please fill in all the form fields including the terms of use to proceed with the request");
        return false;
    } else {
            //Start exporting template
            $.ajax({
            type: "POST",
            url: "ask_templ",
            data: {idLic: document.getElementById("licnum").value,
                tType: document.getElementById("t_type").value,
                tPre: r_1.value.substring(0, 1000),
                tSteps: r_2.value.substring(0, 1000),
                tExpect: r_3.value.substring(0, 1000),
                tCode: HTMLEncode(document.getElementById("t_code").value).substring(0, 1000),
                tDesc: r_4.value.substring(0, 1000)
            },
                success: function (data) {

                    if (data == "OK"){
                        alert('The request to create your template has been correctly inserted in our database. Our staff will proceed to the evaluation of your data. As soon as the approval process is completed your new template will be inserted into our Cathedral Studio new Marketplace Templates update newsletter.');
                        window.location.href = '/tassist';
                    } else {
                        alert('Something went wrong! Check the correctness of the data in your request or contact our technical support for assistance.');
                        window.open('https://cathedral.ai/#contactus','_blank');
                    }
                },
                error: function(jqxhr, status, exception) {
                    alert('Error '+exception);
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
  window.location.replace("https://cathedral.ai/register/");
  return false;
}
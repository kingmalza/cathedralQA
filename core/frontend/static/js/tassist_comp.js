function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}

$(document).ajaxStop(function () {
    //alert('STOP');
    try {
      document.getElementById("overlay_tass").style.display = "none";
    }
    catch(err) {
      
    }
});


function submitHandler(e) {
    document.getElementById("iform").submit();
    //e.preventDefault();
}


function importLine() {


    $.ajax({
        type: "POST",
        url: "import_templ/",
        data: {},
        success: function (data) {


        }
    });
}


function createLine() {

    try {
        t_main = document.getElementById("tass");
        t_main.innerHTML = "";
    }
    catch(err) {
        t_main = null;
    }



    $.ajax({
        type: "POST",
        url: "getassist",
        data: {},
        success: function (data) {

            var templ_count = 0;


                $.each(data, function (index) {

                    var div_inf1 = document.createElement("div");
                    div_inf1.setAttribute('class', 'col-md-4');
                    div_inf1.style.paddingBottom = '40px';
                    var div_inf2 = document.createElement("div");
                    div_inf2.setAttribute('class', 'box2 box-info');
                    div_inf2.setAttribute('id','dcoll');
                    var div_inf3 = document.createElement("div");
                    div_inf3.setAttribute('class', 'box-header');


                    //var div_row = document.createElement("div");
                    //div_row.setAttribute('class', 'row');
                    //div_row.style.paddingBottom = '30px';
                    //First create box info

                    //var createH = document.createElement('a');
                    //createH.setAttribute('href', '/static/out/'+data[index].rl_html+'/'+data[index].rl_html+'_TC.html');
                    //createH.target = "_blank";
                    var buthtview = document.createElement("button");
                    buthtview.type = "button";
                    buthtview.className = "btn btn-default";
                    buthtview.setAttribute('id','myBtn');
                    buthtview.setAttribute('name', data[index].rl_id);
                    //buthtview.addEventListener("click", function(){modal.style.display = "block";});
                    var ibut = document.createElement("I");
                    ibut.setAttribute('class', 'fa fa-search');
                    buthtview.appendChild(ibut);
                    //buthtview.onclick = function() {document.getElementById('myModal').style.display = 'block';};
                    buthtview.onclick = function() {get_t_data(this.name);};
                    //createH.appendChild(buthtview);
                    var h3_1 = document.createElement("h3");
                    h3_1.innerHTML = data[index].rl_desc;
                    h3_1.setAttribute('class', 'box-title');
                    h3_1.style.paddingLeft = '10px';
                    div_inf3.appendChild(buthtview);
                    div_inf3.appendChild(h3_1);
                    var div_inf3_1 = document.createElement("div");
                    div_inf3_1.setAttribute('class', 'box-tools pull-right');
                    var div_inf3_1_1 = document.createElement("div");
                    if (data[index].rl_already == "Y") {
                        div_inf3_1_1.setAttribute('class', 'label bg-aqua');
                        var text_div3 = document.createTextNode("INSTALLED");
                    } else {
                        templ_count = templ_count+1;
                        div_inf3_1_1.setAttribute('class', 'label pull-right bg-green');
                        var text_div3 = document.createTextNode("NEW");
                    }
                    div_inf3_1_1.appendChild(text_div3);
                    div_inf3_1.appendChild(div_inf3_1_1);
                    div_inf3.appendChild(div_inf3_1);
                    div_inf2.appendChild(div_inf3);

                    var div_inf2b = document.createElement("div");
                    div_inf2b.setAttribute('class', 'box-body');
                    div_inf2b.style.height = '50%';
                    var text_inf2b = document.createTextNode(data[index].rl_sdescr);
                    div_inf2b.appendChild(text_inf2b);
                    div_inf2.appendChild(div_inf2b);


                    //Div for display data like category, download numbers ecc
                    var div_inf2b_data = document.createElement("div");
                    div_inf2b_data.setAttribute('class', 'box-body');
                    div_inf2b_data.style.height = '20%';
                    var div_inf2b_data_r = document.createElement("div");
                    div_inf2b_data_r.setAttribute('class', 'row');
                    var div_inf2b_data_r1 = document.createElement("div");
                    div_inf2b_data_r1.setAttribute('class', 'col-md-4');
                    var span1 = document.createElement("SPAN");
                    /*span1.setAttribute('class', 'label label-warning');
                    span1.innerHTML=data[index].rl_scover.toUpperCase();
                    div_inf2b_data_r1.appendChild(span1);*/
                    var div_inf2b_data_r2 = document.createElement("div");
                    div_inf2b_data_r2.setAttribute('class', 'col-md-4');
                    var div_inf2b_data_r3 = document.createElement("div");
                    div_inf2b_data_r3.setAttribute('class', 'col-md-4');
                    div_inf2b_data_r3.style.textAlign = 'right';
                     var span3 = document.createElement("CODE");
                     //span3.setAttribute('class', 'label label-success');
                     span3.innerHTML = '#'+data[index].rl_scover.toUpperCase();
                    /*if(data[index].rl_scredits <= 2) {
                        span3.setAttribute('class', 'label label-success');
                        if (data[index].rl_scredits == 1) {
                            span3.innerHTML = data[index].rl_scredits + ' Credit';
                        } else {
                            span3.innerHTML = data[index].rl_scredits + ' Credits';
                        }
                    } else if (data[index].rl_scredits > 2 && data[index].rl_scredits <= 6) {
                        span3.setAttribute('class', 'label label-primary');
                        span3.innerHTML = data[index].rl_scredits + ' Credits';
                    } else {
                       span3.setAttribute('class', 'label label-danger');
                       span3.innerHTML = data[index].rl_scredits + ' Credits';
                    }*/

                    div_inf2b_data_r3.appendChild(span3);

                    div_inf2b_data_r.appendChild(div_inf2b_data_r1);
                    div_inf2b_data_r.appendChild(div_inf2b_data_r2);
                    div_inf2b_data_r.appendChild(div_inf2b_data_r3);
                    div_inf2b_data.appendChild(div_inf2b_data_r);
                    div_inf2.appendChild(div_inf2b_data);

                    var div_inf2c = document.createElement("div");
                    div_inf2c.setAttribute('class', 'box-footer');
                    var impform = document.createElement("FORM");
                    impform.setAttribute("id", "iform");
                    impform.method = "post";
                    //impform.action = "JavaScript:importLine()";
                    impform.action = "/import_templ/";
                    impform.addEventListener("submit", submitHandler);
                    //Create hidden ID input
                    var IDinput = document.createElement("input");
                    IDinput.setAttribute("type", "hidden");
                    IDinput.setAttribute("id", "idimp");
                    IDinput.setAttribute("name", "idimp");
                    IDinput.setAttribute("value", data[index].rl_id);
                    var IDprice = document.createElement("input");
                    IDprice.setAttribute("type", "hidden");
                    IDprice.setAttribute("id", "tprice");
                    IDprice.setAttribute("name", "tprice");
                    IDprice.setAttribute("value", data[index].rl_scredits);
                    var buthtml = document.createElement("input");
                    buthtml.type = "submit";
                    buthtml.value = "IMPORT THIS TEMPLATE";
                    buthtml.className = "btn btn-block btn-primary btn-lg";
                    impform.appendChild(IDinput);
                    impform.appendChild(IDprice);
                    impform.appendChild(buthtml);
                    div_inf2c.appendChild(impform);
                    div_inf2.appendChild(div_inf2c);

                    div_inf1.appendChild(div_inf2);
                    //div_row.appendChild(div_inf1);

                    try {
                        t_main.appendChild(div_inf1);
                    }
                    catch(err) {
                        console.log("From main");
                    }
                    //End box info

                });

            document.getElementById("asnum").innerHTML = templ_count;

        }
    });
}


function removeElement(elementId) {
    // Removes an element from the document
    var element = document.getElementById(elementId);
    element.parentNode.removeChild(element);
}


function get_t_data(id_teml) {

    try {
        removeElement('myModal');
    } catch (e) {}

  $.ajax({
        type: "POST",
        url: "mpdata",
        data: {idt: id_teml},
        success: function (data) {
            $.each(data, function (index) {

                    //Modal window for display template details
                    var div_supermodal = document.createElement("div");
                    div_supermodal.setAttribute('class', 'modal');
                    div_supermodal.setAttribute('id','myModal');
                    div_supermodal.style.display = 'block';

                    var div_modal = document.createElement("div");
                    div_modal.setAttribute('class', 'modal-content');

                    var div_modal_h = document.createElement("div");
                    div_modal_h.setAttribute('class', 'modal-header');
                    var span_modal_h = document.createElement("span");
                    span_modal_h.setAttribute('class', 'close');
                    span_modal_h.innerHTML = '&times;';
                    //span_modal_h.addEventListener("click", function(){document.getElementById('myModal').style.display = "none";});
                    var h2_modal_h = document.createElement("h2");
                    h2_modal_h.innerHTML = data[index].TTITLE;
                    div_modal_h.appendChild(span_modal_h);
                    div_modal_h.appendChild(h2_modal_h);

                    var div_modal_b = document.createElement("div");
                    var div_html = document.createElement("div");
                    var div_callout = document.createElement("div");
                    div_html.style.paddingBottom = '20px';
                    var div_h3 = document.createElement("div");
                    div_h3.style.backgroundColor = '#ecf0f5';
                    div_h3.style.paddingLeft = '5px';
                    div_modal_b.setAttribute('class', 'modal-body');
                    var p_modal_b = document.createElement("p");
                    p_modal_b.innerHTML = data[index].TDESCRL;
                    var p_lic_b = document.createElement("p");
                    p_lic_b.setAttribute('id','mylic');
                    p_lic_b.innerHTML = data[index].LICN;
                    var h_modal_b = document.createElement("H3");
                    h_modal_b.innerHTML = "Test Template Structure";
                    div_h3.appendChild(h_modal_b);
                    div_modal_b.appendChild(p_lic_b);
                    if (data[index].SID != null) {
                        div_html.innerHTML = data[index].THTML;
                    } else {
                        div_html.innerHTML = data[index].THTML+"<div id='text-demo'><div class='login-box-body'><p class='login-box-msg'><strong><font color='green'>SUCCESS!</font></strong></p><br><strong>The registration request of your aida account was successful.</strong><br><br>Our staff will take care of your request and will proceed in the shortest possible time to carry out all the necessary operations to allow you to use aida without restrictions.<br><br>As soon as the registration procedure is complete you will receive an email to the address you specify in registration proces containing all the necessary data Using your new aida environment, if you do not receive the activation email within 24 hours, try checking your spam box.<br><br><br><div><a href='#' onclick=window.location.href='https://cathedral.ai/gocard/'+document.getElementById('mylic').innerText><button class='btn btn-block btn-success btn-lg'>GO TO AIDA PROJECT HOMEPAGE</button></a></div></div></div>";
                    }
                    div_modal_b.appendChild(p_modal_b);
                    div_modal_b.appendChild(div_h3);
                    div_modal_b.appendChild(div_html);

                    /*
                    var div_modal_f = document.createElement("div");
                    div_modal_f.setAttribute('class', 'modal-footer');
                    var h3_modal_f = document.createElement("h3");
                    h3_modal_f.innerHTML = 'Modal footer';
                    div_modal_f.appendChild(h3_modal_f);*/

                    div_modal.appendChild(div_modal_h);
                    div_modal.appendChild(div_modal_b);
                    //div_modal.appendChild(div_modal_f);
                    div_supermodal.appendChild(div_modal);
                    document.getElementById('dcoll').appendChild(div_supermodal);
                    span_modal_h.addEventListener("click", function(){document.getElementById('myModal').style.display = "none";});
                    //End modal window
            });

        }
    });
}


function openHtml(id_teml) {
  window.open('/static/out/'+id_teml+'/'+id_teml+'_TC.html', '_blank');
}

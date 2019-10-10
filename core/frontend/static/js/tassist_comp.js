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


//check an URL is valid or broken
function ckUrl(purl) {
    var request = new XMLHttpRequest();
    var status;
    var statusText;
    request.open("GET", purl, true);
    request.send();
    request.onload = function(){
        status = request.status;
        statusText = request.statusText;
    }
    if(status == 200) //if(statusText == OK)
        {
            return 'OK';
        } else{
            return 'FAIL';
        }
}


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


function createLine(f_text="", f_sel="ALL") {

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
        data: {"stext":f_text,
        "ssel":f_sel},
        success: function (data) {

            var templ_count = 0;


                $.each(data, function (index) {

                    var div_inf1 = document.createElement("div");
                    div_inf1.setAttribute('class', 'col-md-4');
                    div_inf1.style.paddingBottom = '40px';
                    div_inf1.style.paddingTop = '25px';
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
                    var h3_strong = document.createElement("STRONG")
                    h3_strong.innerText = data[index].rl_desc;
                    h3_1.appendChild(h3_strong);
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
                    var span_inf2b = document.createElement("P");
                    span_inf2b.innerHTML = data[index].rl_sdescr;
                    div_inf2b.appendChild(span_inf2b);
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
            if (data.length == 0) {
                alert('No data found for this filter criteria. Please try another combination.')
                document.getElementById('se_text').innerHTML = '';
                document.getElementById('se_text').value = '';
                createLine();
            }

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

                    //Part relative to credits if present
                    var div_crh = document.createElement("div");
                    div_crh.setAttribute('class', 'box-body chat');
                    div_crh.style.paddingTop = "10px";
                    if (data[index].ADSDESC != null && data[index].ADSURL != null) {
                        div_crh.style.display = "auto";
                    } else {
                        div_crh.style.display = "none";
                    }

                    var lab_crh = document.createElement("LABEL");
                    lab_crh.innerHTML = 'This Template is Powered by:';
                    lab_crh.style.fontStyle = "italic";
                    lab_crh.style.color = "#999";

                    var div_critem = document.createElement("div");
                    div_critem.setAttribute('class', 'item');
                    div_critem.style.padding = "5px";
                    div_critem.style.backgroundColor = "rgb(236, 240, 245)";
                    div_critem.style.borderRadius = "10px";

                    var img_critem = document.createElement("IMG");
                    //check an URL is valid or broken
                    vlink = ckUrl(data[index].ADSIMG);
                    if(vlink == 'OK')
                    {
                        img_critem.src = data[index].ADSIMG;
                    }
                    else{
                       img_critem.src = 'https://cathedral.ai/static/img/nocredit.png';
                    }


                    img_critem.height = '50';
                    img_critem.width = '50';
                    img_critem.setAttribute('class', 'online');

                    var p_critem = document.createElement("P");
                    p_critem.setAttribute('class', 'message');
                    var a_critem = document.createElement("A");
                    a_critem.setAttribute('class', 'name');
                    a_critem.href = data[index].ADSURL;
                    a_critem.setAttribute('target', '_blank');
                    var p_ina = document.createElement("P");
                    p_ina.style.margin = "0px 0px 0px";
                    p_ina.innerHTML = data[index].ADSURL;
                    var p_out = document.createElement("P");
                    p_out.innerHTML = data[index].ADSDESC;

                    a_critem.appendChild(p_ina);

                    p_critem.appendChild(a_critem);
                    p_critem.appendChild(p_out);

                    div_critem.appendChild(img_critem);
                    div_critem.appendChild(p_critem);

                    div_crh.appendChild(lab_crh);
                    div_crh.appendChild(div_critem);

                    //END Credits

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
                    p_lic_b.style.color = '#FFF';
                    var h_modal_b = document.createElement("H3");
                    h_modal_b.innerHTML = "Test Template Structure";
                    div_h3.appendChild(h_modal_b);
                    div_modal_b.appendChild(p_lic_b);
                    if (data[index].SID != null) {
                        div_html.innerHTML = data[index].THTML;
                    } else {
                        div_html.innerHTML = data[index].THTML+"<div id='text-demo' style='box-shadow: 8px 8px #888888'><div class='login-box-body'><p class='login-box-msg'><strong><font color='green'>ALMOST DONE!</font></strong></p><br><strong>You only need just one step to activate your access to the CathedralStudio marketplace</strong><br><br>Register your license to use the cathedral marketplace, you can access new test cases every day to import and use directly in your Cathedral suite in order to optimize your company testing strategy, saving time and increasing the quality of the your products.<br><br>Importing and managing the Cathedral professional tests is quick and easy, click on the ACTIVATE NOW button below, enter the required data and you will have immediate access from your environment to the entire present and future test templates database.<br><br><br><div><a href='#' onclick=window.location.href='https://cathedral.ai/gocard/'+document.getElementById('mylic').innerText><button class='btn btn-block btn-success btn-lg'>ACTIVATE NOW</button></a></div></div></div>";
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
                    div_modal.appendChild(div_crh);
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

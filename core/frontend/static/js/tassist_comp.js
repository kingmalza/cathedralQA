function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}

$(document).ajaxStop(function () {
    //alert('STOP');
    document.getElementById("overlay_tass").style.display = "none";
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

                    //var div_row = document.createElement("div");
                    //div_row.setAttribute('class', 'row');
                    //div_row.style.paddingBottom = '30px';
                    //First create box info
                    var div_inf1 = document.createElement("div");
                    div_inf1.setAttribute('class', 'col-md-4');
                    div_inf1.style.paddingBottom = '40px';
                    var div_inf2 = document.createElement("div");
                    div_inf2.setAttribute('class', 'box2 box-info');
                    var div_inf3 = document.createElement("div");
                    div_inf3.setAttribute('class', 'box-header');
                    var createH = document.createElement('a');
                    createH.setAttribute('href', '/static/out/'+data[index].rl_html+'/'+data[index].rl_html+'_TC.html');
                    createH.target = "_blank";
                    var buthtview = document.createElement("button");
                    buthtview.type = "button";
                    buthtview.className = "btn btn-default";
                    var ibut = document.createElement("I");
                    ibut.setAttribute('class', 'fa fa-search');
                    buthtview.appendChild(ibut);
                    createH.appendChild(buthtview);
                    var h3_1 = document.createElement("h3");
                    h3_1.innerHTML = data[index].rl_desc;
                    h3_1.setAttribute('class', 'box-title');
                    h3_1.style.paddingLeft = '10px';
                    div_inf3.appendChild(createH);
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
                    div_inf2b.style.height = '70%';
                    var text_inf2b = document.createTextNode(data[index].rl_notes);
                    div_inf2b.appendChild(text_inf2b);
                    div_inf2.appendChild(div_inf2b);

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
                    var buthtml = document.createElement("input");
                    buthtml.type = "submit";
                    buthtml.innerHTML = "IMPORT THIS TEMPLATE";
                    buthtml.className = "btn btn-block btn-primary btn-sm";
                    impform.appendChild(IDinput);
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


function openHtml(id_teml) {
  window.open('/static/out/'+id_teml+'/'+id_teml+'_TC.html', '_blank');
}
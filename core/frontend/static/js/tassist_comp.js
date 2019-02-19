function GetElementInsideContainer(containerID, childID) {
    var elm = document.getElementById(childID);
    var parent = elm ? elm.parentNode : {};
    return (parent.id && parent.id === containerID) ? elm : {};
}


function createLine() {

    t_main = document.getElementById("tass");
    t_main.innerHTML = "";



    $.ajax({
        type: "POST",
        url: "getassist",
        data: {},
        success: function (data) {

            $.each(data, function (index) {

                //var div_row = document.createElement("div");
                //div_row.setAttribute('class', 'row');
                //div_row.style.paddingBottom = '30px';
                //First create box info
                var div_inf1 = document.createElement("div");
                div_inf1.setAttribute('class', 'col-md-4');
                div_inf1.style.paddingBottom = '30px';
                var div_inf2 = document.createElement("div");
                div_inf2.setAttribute('class', 'box2 box-info');
                var div_inf3 = document.createElement("div");
                div_inf3.setAttribute('class', 'box-header');
                var h3_1 = document.createElement("h3");
                h3_1.innerHTML = data[index].rl_desc;
                h3_1.setAttribute('class', 'box-title');
                div_inf3.appendChild(h3_1);
                var div_inf3_1 = document.createElement("div");
                div_inf3_1.setAttribute('class', 'box-tools pull-right');
                var div_inf3_1_1 = document.createElement("div");
                div_inf3_1_1.setAttribute('class', 'label bg-aqua');
                var text_div3 = document.createTextNode("Label");
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
                var createA = document.createElement('a');
                createA.setAttribute('href', '/static/out/'+data[index].rl_html+'/'+data[index].rl_html+'_TC.html');
                createA.target = "_blank";
                var buthtml = document.createElement("button");
                buthtml.type = "button";
                buthtml.innerHTML = "HTML Structure ";
                buthtml.className = "btn btn-block btn-default btn-sm";
                createA.appendChild(buthtml)
                div_inf2c.appendChild(createA);
                div_inf2.appendChild(div_inf2c);

                div_inf1.appendChild(div_inf2);
                //div_row.appendChild(div_inf1);
                t_main.appendChild(div_inf1);
                //End box info

            });


        }
    });
}

function openHtml(id_teml) {
  window.open('/static/out/'+id_teml+'/'+id_teml+'_TC.html', '_blank');
}
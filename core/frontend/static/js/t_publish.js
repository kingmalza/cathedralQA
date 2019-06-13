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

function clicktemp(tID) {

    oDetTempl = document.getElementById("t_details");
    //Relative to details area after template selection
    oDetDescr = document.getElementById("det_descr");
    oDetNotes = document.getElementById("det_notes");
    oDetDt = document.getElementById("det_dt");
    oDetType = document.getElementById("det_type");


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
                oDetDt.innerHTML = "";
                oDetDt.innerHTML = data[index].OptionDt;
                oDetType.innerHTML = "";
                oDetType.innerHTML = data[index].OptionTtype;

            });

        }
    });
}


function isempty() {
    var r_1;
    var r_2;
    var r_3;


    r_1 = document.getElementById("t_select").value;
    r_2 = document.getElementById("t_descr").value;
    r_3 = document.getElementById("t_terms").value;

    alert(r_1.value+'--'+r_3.value);



}
/*
if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}
try {
    $ = django.jQuery;
}
catch(err) {
  console.log('$ already done -> '+err.message);
}

console.log("Dentro e fuori in admin.js");
$(document).ready(function() {
  console.log("Dentro in admin.js");
    $("select[name='main_id']").change(function() {
        $("select['test_id']").val('');
    });
});*/

​document.onclick = function(){
 // your code
 console.log("Dentro in admin.js");
}​
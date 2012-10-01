function college_reg()
{
    data=$("#reg input,#reg select").serializeObject();
    reg_html = document.getElementById("reg").innerHTML
    var loading_text = new Array('P','r','o','c','e','s','s','i','n','g')
    for (i=0; i<10; i=i+1) {
        if (reg_html[i] != loading_text[i]) {
            $("#reg").prepend("Processing please wait..<br><img src='/static/img/loading.gif'>");
            break;
        }
    }

    Dajaxice.users.college_register(Dajax.process,{'form':data});
}
function reg_done(data)
{
    switch(data)
    {
    case 0:
        alert("Please enter valid details!");
        break;
    case 1:
		var obj = document.getElementById("id_college");
        obj.options[obj.options.length] = new Option($("#id_name").attr('value')+", "+$("#id_city").attr('value')+", "+$("#id_state").attr('value'), obj.options.length,false,true);
        $("#reg").html("");
        $("#msg").show();                
        break;
    case 2:
        alert("Record exists");
    }

}
$(document).ready(function(){
    html="<td><div id='msg'>Register New College</div><div id='reg'></div></td>";
    $("table tr:eq(6)").append(html);
});
$(document).ready(function(){
   $("#msg").click(function(){
        $(this).hide();
        $("#reg").prepend("Loading please wait..<br><img src='/static/img/loading.gif'>");
        Dajaxice.users.college_register(Dajax.process);            
   });
 });
function close_reg(){
    $("#reg").html("");
    $("#msg").show();
}

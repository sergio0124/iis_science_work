let submit = document.getElementById("regression_submit");
let select_1 = document.getElementById("regression_select_1");
let select_2 = document.getElementById("regression_select_2");


submit.addEventListener('click', function(){
    let cluster_select1 = "";
    if(document.body.contains(select_1)){
        cluster_select1 = select_1.value;
    }
    let cluster_select2 = "";
    if(document.body.contains(select_2)){
        cluster_select2 = select_2.value;
    }

    newUrl = "http://127.0.0.1:5000/regression?column1=" + cluster_select1 + "&column2=" + cluster_select2 + "";
    window.location.replace(newUrl);
})
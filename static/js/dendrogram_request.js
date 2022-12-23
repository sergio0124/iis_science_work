let submit = document.getElementById("dendrogram_submit");
let select = document.getElementById("dendrogram_select");
let number = document.getElementById("dendrogram_number");


submit.addEventListener('click', function(){
    let cluster_number = 4;
    if(document.body.contains(number)){
        cluster_number = Number(number.value);
    }
    let cluster_select = "single";
    if(document.body.contains(select)){
        cluster_select = select.value;
    }

    newUrl = "http://127.0.0.1:5000/dendrogram?method=" + cluster_select + "&count=" + cluster_number + "";
    window.location.replace(newUrl);
})

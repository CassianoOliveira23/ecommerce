var url = new URL(document.URL);
var items = document.getElementsByClassName("order-item")


for(i=0; i < items.length; i++){
    items[i]
    url.searchParams.set("order", items[i].value); 
    items[i].value = url.href;
}

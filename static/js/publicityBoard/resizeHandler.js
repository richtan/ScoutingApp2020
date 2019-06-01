function adjustElements() {
    document.getElementById("iframeDiv").style.top = document.getElementById("tabs").getBoundingClientRect().bottom - 5 + "px";
    if(window.innerHeight < window.innerWidth){
        document.getElementById("topDiv").style.top = (window.innerHeight - document.getElementById('topDiv').offsetHeight)/3 + "px";
    }
}

adjustElements();
window.onload = adjustElements;
window.onresize = adjustElements;
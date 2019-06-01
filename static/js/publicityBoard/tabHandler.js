

function changeTab(tab, iframeId) {

    if (tab != document.getElementById('selected')) {
        document.getElementById('selected').id = '';
        tab.id = 'selected';
        for(element of document.getElementsByTagName('iframe')) {
            element.style.display = 'none';
        }
        document.getElementById(iframeId).style.display = 'initial';

        
    }
    
}
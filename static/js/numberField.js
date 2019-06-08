var buttons = document.getElementsByTagName("button");
for (let button of buttons) {
    if(button.className == "sub") {
        button.addEventListener("click", function() {
            var field = button.nextSibling.nextSibling.children[0];
            var nextValue = parseInt(field.value) - 1;
            if(nextValue >= field.min && nextValue <= field.max) {
                field.value = nextValue;
            }
        });
    } else if(button.className == "add") {
        button.addEventListener("click", function() {
            var field = button.previousSibling.previousSibling.children[0]
            var nextValue = parseInt(field.value) + 1;
            if(nextValue >= field.min && nextValue <= field.max) {
                field.value = nextValue;
            }
        });
    }
}
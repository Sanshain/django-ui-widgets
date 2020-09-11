function urlFieldPreFill(event){
    if (event.inputType === 'deleteContentBackward') return;
    if (!event.target.value.startsWith('http')){
        event.target.value = 'https://' + event.target.value;
    }
}
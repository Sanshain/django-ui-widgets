function debounce(f, ms) {

    let isCooldown = false;
    return function() {
        if (isCooldown) return;

        f.apply(this, arguments);
        isCooldown = true;

        setTimeout(() => isCooldown = false, ms);
    };

}


// all obsolete:
/**
 * 
 */
const dutySymbols = {
    '+':'plus',
    '#':'sharp'
}

function replace_duty_chars(text){
    for(let symbol in dutySymbols){
        text = text.replace(RegExp('\\'+symbol, 'g'), dutySymbols[symbol]);
    }
    return text;
}
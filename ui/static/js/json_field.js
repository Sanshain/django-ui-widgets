/**
 * 
 * @param {string} key - id элемента, содержащего json ключ
 */
function del_key(event, key){

    let input = document.getElementById(key);
    if (input instanceof HTMLInputElement){

        let elems = [
            document.getElementById(key),
            document.querySelector('label[for="'+ key +'"]'),
            event.target
        ]
    
        for (let elem of elems) elem.parentElement.removeChild(elem);   
    }
    else if(input instanceof HTMLSelectElement){
        
        let options = input.querySelectorAll('option');
        for (let i = 0; i < options.length; i++) {
            const option = options[i];
            if (option.selected){

                option.parentElement.removeChild(option);
                let hidden_input = input.parentElement.querySelector('input[name="'+input.id + "__" + i+'"');
                hidden_input.parentElement.removeChild(hidden_input);
            }            
        }

    }


    /*
    for (let elem of elems) elem.style.opacity = '0';

    setTimeout(function(){
        
        for (let elem of elems) elem.parentElement.removeChild(elem);   
    }, 1000); //*/
}


function append_value(event){

    let modal = modalCreate();
    modal.style.paddingTop = '4em';

    let close = document.createElement('div');    
    let valMod = document.createElement('input');
    let accept = document.createElement('div'); 
        
    valMod.placeholder = 'Значение'    
    accept.innerText = 'Добавить'    
    accept.className = 'keyvalue_accept';
    close.className = 'new_key_cancel';
    valMod.onkeydown = function(e){
        
        if(e.key == 'Enter') accept.click()
    }

    close.onclick = function(){
        
        modal.style.opacity = '0';
        setTimeout(()=>{

            modal.parentElement.removeChild(modal);
        }, 1000)        
    }

    accept.onclick = function(){
     
        if (valMod.value.length == 0) return;
        select = event.target.parentElement.querySelector('select');
        let options = select.querySelectorAll('option');
        
        let newOption = document.createElement('option')
        newOption.value = valMod.value;
        newOption.innerText = valMod.value;
        select.appendChild(newOption);

        let input = document.createElement('input');
        input.name = select.id + '__' + options.length;            
        input.value = valMod.value;
        input.style.display = 'none';

        select.parentElement.appendChild(input);
        close.onclick();
    }

    let elems = [close, valMod, accept];
    for (const elem of elems) {
        modal.appendChild(elem);
    }

    setTimeout(()=>{
        modal.style.opacity = '1';
        valMod.focus();
    })

}

/**
 * Добавляет поле ключ-занчение верхнего уровня
 * @param {*} event 
 */
function add_json_field(event){


    var modal = modalCreate();
    
    function button_close(){
        
        modal.style.opacity = '0';
        setTimeout(()=>{

            modal.parentElement.removeChild(modal);
        }, 1000)        
    }

    let close = document.createElement('div');
    let keyMod = document.createElement('input');
    let valMod = document.createElement('input');
    let accept = document.createElement('div');


    keyMod.placeholder = 'Ключ';         
    valMod.placeholder = 'Значение'
    valMod.onkeydown = (e) => { if(e.key == 'Enter') accept.click() }
    
    accept.innerText = 'Добавить'    
    accept.className = 'keyvalue_accept';
    accept.onclick = function(){

        if (keyMod.value.length == 0 || valMod.value.length == 0) {

            alert('Введите корректные данные');return;
        }

        let root_key = event.target.parentElement.previousElementSibling.innerText.toLowerCase().slice(0, -1);
        let kv_row = document.createElement('div');
        let keyElem = document.createElement('label');
        let valElem = document.createElement('input');

        keyElem.name = valElem.name = valElem.id = root_key + '__' + keyMod.value;
        keyElem.innerText = keyMod.value;
        valElem.value = valMod.value;
        valElem.type = 'text';
        valElem.className = 'jsn_value';
        valElem.style.backgroundColor = '#eeeeee';
        keyElem.className = 'jsn_label';
        
        kv_row.style.marginTop = '2px';
        kv_row.appendChild(keyElem);
        kv_row.appendChild(valElem);
        event.target.parentElement.insertBefore(kv_row, event.target);

        button_close();
    }

    close.className = 'new_key_cancel';
    close.onclick = button_close;
    
    let elems = [close, keyMod, valMod, accept];
    for (const elem of elems) {
        modal.appendChild(elem);
    }

    setTimeout(()=>{
        modal.style.opacity = '1';
        keyMod.focus();
    })
}

window.addEventListener('load', function(){
    var selects = document.querySelectorAll('.jsn_array')
    for (const selectElem of selects) {
        
        let options = selectElem.querySelectorAll('option');
        for (let i = 0; i < options.length; i++) {
            
            const option = options[i];
            let input = document.createElement('input');
            input.name = selectElem.id + '__' + i;            
            input.value = option.value;
            input.style.display = 'none';

            selectElem.parentElement.appendChild(input);
        }


    }
})

function modalCreate() {

    var modal = document.createElement('div');
    modal.className = 'modal';
    document.body.appendChild(modal);
    modal.style.display = 'block';
    return modal;
}

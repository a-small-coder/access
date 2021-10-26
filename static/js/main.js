console.log("uenty nfu!");
/*
    select - id_pay_way
    select - id_needed_product
    input - id_needed_quantity
    input - id_needed_cost
    select - id_given_product
    input - id_given_quantity
    input - id_given_cost
*/

// form elements
var payWaySelect = document.getElementById("id_pay_way"),
    neededProductSelect = document.getElementById("id_needed_product"),
    neededQuantityInput = document.getElementById("id_needed_quantity"),
    neededCostInput = document.getElementById("id_needed_cost"),
    givenProductSelect = document.getElementById("id_given_product"),
    givenQuantityInput = document.getElementById("id_given_quantity"),
    givenCostInput = document.getElementById("id_given_cost");

// support data
let elementVisibleState = {
    visible: 'inherit',
    disable: 'none'
}
let expectedPayWayData = ['', 'cash', 'cashless', 'credit', 'barter', 'sell']

// example product data
let products = [
    {},

    {
        name: "чеченька",
        quantity: 958,
        cost: 49.00,
    },
    {
        name: "булочка",
        quantity: 753,
        cost: 99.00,
    }
]


// show or hide "given" and "needed" fields 
function changeVisibleGivenFields(stateMod = 0){
    switch (stateMod) {
        case 0: // hide given fields and show needed fields
            showNeededFields(elementVisibleState.visible)
            showGivenFields(elementVisibleState.disable);
            break;
        case 1: // show given fields and show needed fields
            showNeededFields(elementVisibleState.visible)
            showGivenFields(elementVisibleState.visible);
            break;
        case 2: // show given fields and hide needed fields
            showNeededFields(elementVisibleState.disable)
            showGivenFields(elementVisibleState.visible);
            break;
        case 3: // hide given fields and hide needed fields
            showNeededFields(elementVisibleState.disable)
            showGivenFields(elementVisibleState.disable);
            break;
        default:
            break;
    }
}
// support functions for show or hide fields
// props: Type - string, support data - 'none', 'inherit
function showGivenFields(visiblity){
    givenProductSelect.parentNode.style.display = visiblity;
    givenQuantityInput.parentNode.style.display = visiblity;
    givenCostInput.parentNode.style.display = visiblity;
}
function showNeededFields(visiblity){
    neededProductSelect.parentNode.style.display = visiblity;
    neededQuantityInput.parentNode.style.display = visiblity;
    neededCostInput.parentNode.style.display = visiblity;
}

// delete all data from fields
function clearFields(){
    neededProductSelect.value = 0;
    neededQuantityInput.value = null;
    neededCostInput.value = null;
    givenProductSelect.value = 0;
    givenQuantityInput.value = null;
    givenCostInput.value = null;
}

function changeFieldsVisability(){
    clearFields();
    let isNeed = 3;  // hide all fields - when payWaySelect.value == ''
    if (payWaySelect != null){
        switch (payWaySelect.value) {
            case expectedPayWayData[4]:  // 'barter'
                isNeed = 1
                break;
            case expectedPayWayData[5]: // 'sell'
                isNeed = 2
                break;
            case expectedPayWayData[0]: // no way selected
                isNeed = 3
                break;
            default:
                isNeed = 0; // other - 'cash', 'cashless', 'credit'
                break;
        }
    }
    changeVisibleGivenFields(isNeed);
}

// checking fields's value
// props: DOM-fields (input field with product cost data, input field with product quantity data, select field with product types data)
function setNeedCost(cInputField, qInputField, pSelectField){
    let quantity = qInputField.value;
    let oneCost = getProductCost(pSelectField);
    if (quantity > 0 && oneCost != null){
        cInputField.value = quantity * oneCost;
    }
    else{
        cInputField.value = "";
    }

    console.log("quantity ", quantity);
    console.log("oneCost ", oneCost);
    console.log("needed_cost ", cInputField.value);
}
function getProductCost(pSelectField){
    if (pSelectField?.value > 0 ){
        let product = products[pSelectField.value]
        return product?.cost;
    }
    return null
}
function setQuantity(cInputField, qInputField, pSelectField){
    let allCost = cInputField.value;
    let oneCost = getProductCost(pSelectField);
    if (allCost > 0 && oneCost != null && oneCost > 0){
        qInputField.value = Math.floor(allCost / oneCost);
    }
    else{
        qInputField.value = "";
    }
    console.log("allCost ", allCost);
    console.log("oneCost ", oneCost);
    console.log("needed quantity ", qInputField.value);
}


// factories
function setNeedCostWithoutGivenFields(){
    setNeedCost(neededCostInput, neededQuantityInput, neededProductSelect);
}
function setQuantityWithoutGivenFields(){
    setQuantity(neededCostInput, neededQuantityInput, neededProductSelect);
}
function setNeedCostGivenFields(){
    setNeedCost(givenCostInput, givenQuantityInput, givenProductSelect);
}
function setQuantityGivenFields(){
    setQuantity(givenCostInput, givenQuantityInput, givenProductSelect);
}

// start program, (when page load)
document.addEventListener("DOMContentLoaded", function(){
    // presets
    clearFields();    
    changeVisibleGivenFields(3);
    neededProductSelect[0].style.display='none';
    givenProductSelect[0].style.display='none';

    // adding event listeners
    payWaySelect.addEventListener('change', changeFieldsVisability);

    neededQuantityInput.addEventListener('keyup', setNeedCostWithoutGivenFields);
    neededProductSelect.addEventListener('change', setNeedCostWithoutGivenFields);
    neededCostInput.addEventListener('keyup', setQuantityWithoutGivenFields);
    neededCostInput.addEventListener('focusout', setNeedCostWithoutGivenFields)

    givenQuantityInput.addEventListener('keyup', setNeedCostGivenFields);
    givenProductSelect.addEventListener('change', setNeedCostGivenFields);
    givenCostInput.addEventListener('keyup', setQuantityGivenFields);
    givenCostInput.addEventListener('focusout', setNeedCostGivenFields);
});

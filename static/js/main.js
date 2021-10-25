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


// show and disable "given" fields 
function changeVisibleGivenFields(stateMod = 0){
    let state
    stateMod ? state = elementVisibleState.visible : state = elementVisibleState.disable;
    givenProductSelect.parentNode.style.display = state;
    givenQuantityInput.parentNode.style.display = state;
    givenCostInput.parentNode.style.display = state;
}

function isNeedShowGivenFields(){
    let isNeed = false;
    if (payWaySelect != null){
        console.log("-",payWaySelect.value,"-");
        if (
            payWaySelect.value === expectedPayWayData[4] ||
            payWaySelect.value === expectedPayWayData[5]
        ){
            isNeed = true
            }
        else 
            isNeed = false
    }
    else 
        isNeed = false
    changeVisibleGivenFields(isNeed)
}

// checking fields value
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
    console.log("Для начала, скроем лишнее от чужих глаз");
    changeVisibleGivenFields();

    console.log("и будем наблюдать из тени...");
    payWaySelect.addEventListener('change', isNeedShowGivenFields);

    neededQuantityInput.addEventListener('keyup', setNeedCostWithoutGivenFields);
    neededProductSelect.addEventListener('change', setNeedCostWithoutGivenFields);
    neededCostInput.addEventListener('keyup', setQuantityWithoutGivenFields);
    neededCostInput.addEventListener('focusout', setNeedCostWithoutGivenFields)

    givenQuantityInput.addEventListener('keyup', setNeedCostGivenFields);
    givenProductSelect.addEventListener('change', setNeedCostGivenFields);
    givenCostInput.addEventListener('keyup', setQuantityGivenFields);
    givenCostInput.addEventListener('focusout', setNeedCostGivenFields);
});

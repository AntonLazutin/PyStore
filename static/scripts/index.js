let buttons = document.getElementsByClassName("cart_btn");


Array.from(buttons).forEach(function (button){

    button.addEventListener('click', function (){
        let action = this.dataset.action;

        console.log('Product: ', product);
        console.log('Action: ', action);
    })
})

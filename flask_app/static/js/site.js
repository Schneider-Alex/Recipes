// function getUsers(){
//     fetch('http://127.0.0.1:5000/saveusers')
//         .then(res =>  res.json())
//         .then(data => {
//             var errors = document.getElementById('errors');
//             errors.innerHTML= data
//             console.log(users)
//             }
//         )}

var myForm = document.getElementById('myForm');
myForm.onsubmit = function(e){
        e.preventDefault();
        var form = new FormData(myForm);
        console.log(form.get('user_name'))
        // this how we set up a post request and send the form data.
        fetch("http://127.0.0.1:5000/createusers", { method :'POST', body : form})
            .then(response => response.json())
            .then( data => console.log(data))
        

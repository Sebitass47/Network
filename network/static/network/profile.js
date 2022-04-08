document.addEventListener('DOMContentLoaded', function() {
    //Como usamos la misma plantilla para All posts y Profile hay que esconderlo o 
    //mostrarlo 
    
    hearts();

    var ancho = document.documentElement.clientWidth;
    if(ancho <= 991){
        document.querySelectorAll(".nav-item").forEach(element => element.style.display="none")
    }
    else{
        document.querySelector("#desplegable").style.display="none";
    }

    window.onresize=function(){  
        watchChangeSize();
    } 

    if (document.querySelector("#div_create")){
        document.querySelector("#div_create").style.display = 'none';
        document.querySelector("#alert-success").style.display = 'none';
        document.querySelector("#alert-danger").style.display = 'none';
    }
    
    
    if(document.querySelector("#content")){
        const new_post = document.querySelector("#content");
        const submit = document.querySelector("#submit-new");
    
        submit.disabled = true;
    
        new_post.onkeyup = () => {
            if (new_post.value.length > 0) {
                submit.disabled = false;
            }
            else {
                submit.disabled = true;
            }
        }
    }


    if (document.querySelector("#messages")){
        setTimeout(() => {
            document.querySelector("#messages").style.display = 'none';
        }, 5000);
    }


    if (document.querySelector("#profile")){
        document.querySelector("#profile").style.display = 'block';
        document.querySelector("#new_post").style.display = 'none';
         //Al presionar el botón de seguir lanza una peticion para seguir al usuario o dejar de seguirlo
        //Toda esta parte, es para seguir o dejar de seguir al usuario.
        if(document.querySelector("#follow")){
            button = document.querySelector("#follow"); 
            check(button.dataset.follow)
            button.onclick = function() {
            follow(this.dataset.follow);   
            }
        }
        
    }

    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === "button-edit"){
             edit(element.dataset.edit)
        }
        else if (element.className === "button-delete"){
            del(element.dataset.delete)
        }
        else if (element.className === "heart"){
            heart(element.dataset.heart)
        }
        else if (element.className === "bx bx-x"){
            document.querySelector("#div_create").style.display = 'none';
           }
        else if (element.id === "arrow"){
            navbar();
        }
    });
});

function follow(user){
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        `/follow/${user}`,
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',
        mode: 'same-origin',
    })
    .then(response => response.json())
    .then(result => {
        if (result.message === "Following"){
            document.querySelector("#follow").innerHTML = "Following";
        }
        else if(result.message === "Unfollow"){
            document.querySelector("#follow").innerHTML = "Follow";
        }
        else{
            document.querySelector("#alert-danger").style.display = 'block';
            document.querySelector("#alert-danger").innerHTML = "User not found";
            setTimeout(() => {
                document.querySelector("#alert-danger").style.display = 'none';
            }, 5000);
        }
    });
}

function check(user){
    fetch(`/follow/${user}`)
    .then(response => response.json())
    .then(result => {
        if (result.message === "Following"){
            document.querySelector("#follow").innerHTML = "Following";
        }
        else if(result.message === "Follow"){
            document.querySelector("#follow").innerHTML = "Follow";
        }
    })

}

function edit(post_id){

    document.querySelector("#div_create").style.display = 'flex';
    const edit = document.querySelector("#edit");
    const content = document.getElementById(post_id);
    const submit = document.querySelector("#submit-edit");


    edit.innerHTML = content.innerHTML
    submit.disabled = true;

    edit.onkeyup = () => {
        if (edit.value.length > 0) {
            submit.disabled = false;
        }
        else {
            submit.disabled = true;
        }
    }

    document.querySelector("#create").onsubmit = function(){

        const edit_post = document.querySelector("#edit").value
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const request = new Request(
            `/edit/${post_id}`,
            {headers: {'X-CSRFToken': csrftoken}}
        );


        fetch(request,{
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                content: edit_post
            })
        })
        .then(res => res.json())
        .then(res => {
          
            if (res.success) {
            //mensaje correcto
            document.querySelector("#div_create").style.display = 'none';
            content.innerHTML = edit_post;
            const alert = document.querySelector("#alert-success")
            alert.style.display = 'block';
            alert.innerHTML = res.success
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);

          }else{
            const alert = document.querySelector("#alert-danger")
            alert.style.display = 'block';
            alert.innerHTML = res.error
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
          }
        })
        return false;
    }
}


function heart(post_id){
    const number_hearts = document.querySelector(`#number_${post_id}`);
    const heart = document.querySelector(`#heart_drawing_${post_id}`);
   
    if (heart.innerHTML == "♡"){
        fetch(`/new_heart/${post_id}`)
        number_hearts.innerHTML = parseInt(number_hearts.innerHTML, 10) + 1;
        heart.innerHTML = "&#x2764";
  
      
    }
    else{
        fetch(`/new_heart/${post_id}`,{
            method: 'POST',
        })
        number_hearts.innerHTML = parseInt(number_hearts.innerHTML, 10) - 1;
        heart.innerHTML = "&#x2661";
    
    }
}

function hearts(){
    var identity = []
    x = document.querySelectorAll(".heart")
    x.forEach(element => identity.push(element.dataset.heart))
    fetch("/hearts",{
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
            content: identity
        })
    })
    .then(res => res.json())
    .then(res => {
        for (var element in res.result){
            if (res.result[element] === true) {
                document.querySelector(`#heart_drawing_${element}`).innerHTML = "&#x2764";
            }
        }
    });
}

function watchChangeSize (){
        // ancho / alto del área visible (DOM)
        // La diferencia entre offsetHeight (con borde) y clientHeight (sin borde) se refiere al artículo anterior     
    var offsetWid = document.documentElement.clientWidth;

    if(offsetWid <= 991){
        document.querySelectorAll(".nav-item").forEach(element => element.style.display="none")
        document.querySelector("#desplegable").style.display="flex";
    }
    else{
        document.querySelector("#desplegable").style.display="none";
        document.querySelectorAll(".nav-item").forEach(element => element.style.display="block")
    }

}

function navbar () {
        console.log("No se que pedo")
    var arrow = document.querySelector("#arrow")
    if (arrow.className === "bx bxs-chevron-down-circle"){
        console.log("mostrar elementos");
        document.querySelectorAll(".nav-item").forEach(element => element.style.display="block");
        arrow.className = "bx bxs-chevron-down-circle bx-rotate-180";

    }
    else{
        console.log("ocultar elementos");
        document.querySelectorAll(".nav-item").forEach(element => element.style.display="none");
        arrow.className = "bx bxs-chevron-down-circle";
        console.log("else");
    }
}

function del(post_id){
    fetch(`/delete/${post_id}`)
    .then(res => res.json())
    .then(res =>{
        if (res.success) {
            post = document.querySelector(`#post_${post_id}`);
            post.style.animationPlayState = "running";
            post.addEventListener("animationend", () => {
                post.remove();
            })
        }
        else {
            const alert = document.querySelector("#alert-danger")
            alert.style.display = 'block';
            alert.innerHTML = res.error
            setTimeout(() => {
                alert.style.display = 'none';
            }, 5000);
        }
    })
}
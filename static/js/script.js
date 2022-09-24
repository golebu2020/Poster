
let isOpen = false
function revealSettings(){
  console.log("This has been clicked")
  element = document.querySelector(".settings-pop")
  if(isOpen == false){
    element.style.display="flex"
    isOpen = true
  }else{
    element.style.display = "none"
    isOpen = false
  }
  
}

function changeProfile(){
  // console.log("An Error Ocurred")
  // document.getElementById("avater-change-image").src = "{{url_for('static', filename= 'male_pics.JPG')}}";
}

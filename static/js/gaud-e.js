function submitForm(formGenerate){
    console.log('submitForm : ', formGenerate);
    let gaudeLoading = document.getElementById("gaude-loading");
    console.log('gaudeLoading : ', gaudeLoading);
    
    let gaudeImgDefault = document.getElementById("gaude-img-default");
    console.log('gaudeImgDefault : ', gaudeImgDefault);
    
    gaudeImgDefault.classList.add("hidden")
    gaudeLoading.classList.remove("hidden")
    formGenerate.submit();
}
 let btnGenerate = document.getElementById("buttongenerate");
 let formGenerate = document.getElementById("formgenerate");

 btnGenerate.addEventListener("click", function(){
    console.log('submitForm : ', btnGenerate);
    submitForm(formGenerate);
    //btnGenerate.submit();
});
    

function submitForm(btnGenerate){
    console.log('submitForm : ', btnGenerate);
    let gaudeLoading = document.getElementById("gaude-loading");
    console.log('gaudeLoading : ', gaudeLoading);
    
    let gaudeImgDefault = document.getElementById("gaude-img-default");
    console.log('gaudeImgDefault : ', gaudeImgDefault);
    
    gaudeImgDefault.classList.add("hidden")
    gaudeLoading.classList.remove("hidden")
    btnGenerate.submit();
}
 let btnGenerate = document.getElementById("formgenerate");
    btnGenerate.addEventListener("click", function(){
    console.log('submitForm : ', btnGenerate);
    submitForm(btnGenerate);
    //btnGenerate.submit();
});
    

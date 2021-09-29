try{
    var myCarousel = document.getElementById('carouselExampleCaptions')
    var carouselIndex = 0;
    
    myCarousel.addEventListener('slid.bs.carousel', function (e) {
      // do something...
      carouselIndex = e.to;
      var cItems = document.getElementsByClassName("carousel-item");
      var numCancion = cItems[carouselIndex].attributes.value.value;
      document.getElementById("numCancion").value = numCancion;
      //console.log(typeof numCancion)
      //console.log(numCancion);
      //console.log("numCancion input value: ", document.getElementById("numCancion").value);
      //console.log(e.to);
    })
    
} catch (e){
    console.log(e);
}

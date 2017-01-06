function main()
{
    var types=document.querySelectorAll("p.type");
    var titles=document.querySelectorAll("p.title");
    var tags=document.querySelectorAll("p.tags");
    
    types.forEach(function(e,x){
        e.addEventListener("mouseenter",function(){
            titles[x].classList.add("tagmode");
            tags[x].classList.add("tagmode");                
        });

        e.addEventListener("mouseleave",function(){
            titles[x].classList.remove("tagmode");
            tags[x].classList.remove("tagmode");                
        });
    });
}

window.onload=main;

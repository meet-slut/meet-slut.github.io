# meet-slut.github.io

```
function padding0(num, len){
    return (Array(len).join(0) + num).slice(-len);
}
function load10(root, start, nums, steps=10){
    let div = document.getElementsByClassName("m-p-g__thumbs")[0];
    let end = nums > steps ? steps: nums;
    var data = [];
    for (let i=start; i<start+end; i++){
        data.push({});
        let origin = root + padding0(i, 4) + ".jpg";
        let thumb = root + padding0(i, 4) + "_300x0.jpg";
        data[i-start]["title"] = i+"";
        data[i-start]["thumbnail"] = padding0(i, 4) + "_300x0.jpg";
        data[i-start]["enlarged"] = padding0(i, 4) + ".jpg";
        let img1 = new Image();
        img1.onload = function(){data[i-start]["eWidth"]=img1.width; data[i-start]["eHeight"]=img1.height;}
        img1.src = origin;
        
        let img2 = new Image();
        img2.onload = function(){data[i-start]["tWidth"]=img2.width; data[i-start]["tHeight"]=img2.height;}
        img2.src = thumb;
        

        for(let ii=0; ii<=1000000; ii++){
            ii++;
        }
    }
    console.log(data);

}
var root = "https://img.xchina.xyz/photos/61cf6dec77eb1/";
load10(root, 1, 612, 1000);
```
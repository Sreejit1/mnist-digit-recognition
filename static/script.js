const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// White background
ctx.fillStyle = "white";
ctx.fillRect(0,0,280,280);

// Drawing settings
ctx.strokeStyle = "black";
ctx.lineWidth = 20;
ctx.lineCap = "round";
ctx.lineJoin = "round";

let drawing = false;

canvas.addEventListener("mousedown", () => drawing = true);

canvas.addEventListener("mouseup", () => {
    drawing = false;
    ctx.beginPath();
});

canvas.addEventListener("mousemove", draw);

function draw(e){

    if(!drawing) return;

    ctx.lineTo(e.offsetX,e.offsetY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(e.offsetX,e.offsetY);

}

function clearCanvas(){

    ctx.clearRect(0,0,280,280);

    ctx.fillStyle="white";
    ctx.fillRect(0,0,280,280);

    ctx.beginPath();

    document.getElementById("result").innerHTML="";

}

function predict(){

    let image = canvas.toDataURL("image/png");

    fetch("/predict",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            image:image
        })

    })

    .then(response=>response.json())

    .then(data=>{

        document.getElementById("result").innerHTML=
        "<h2>Prediction : "+data.digit+"</h2>"+
        "<h3>Confidence : "+data.confidence+"%</h3>";

    });

}
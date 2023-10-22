
var socket = io();
    socket.on('connect',()=>{
        socket.emit('event', "Client Connected");
    });
    socket.on('disconnect',()=>{
        socket.emit("event","Client Disconnected");
    })
document.getElementById("send").addEventListener("click",()=>{
    var num = Math.floor(Math.random()* 1000);
    //socket.emit('my event',{data: num})
    socket.emit('send',num) //Gui data tu client len server theo channel send
});
socket.on('receive',(data)=>{ 
    console.log("Receive from server: " + data)
    document.getElementById("receive").innerHTML = data //Nhan data tu server len client theo channel receive
})
/**
 * Created by yiner on 2017/5/1.
 */



function refresh (num) {

    // 新建XMLHttpRequest对象
    var request;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        request=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        request=new ActiveXObject("Microsoft.XMLHTTP");
    }

    request.onreadystatechange = function () {  // 状态发生变化时，函数被回调
        if (request.readyState === 4&&request.status === 200) { // 成功完成
            // 判断响应结果:
                // 成功，通过responseText拿到响应的文本:
            document.getElementById("show-here").innerHTML=request.responseText;
        }

    }

    request.open('get', '../lesson/ajax/response-text'+num+'.asp',true); // 发送请求:
    request.send();


}
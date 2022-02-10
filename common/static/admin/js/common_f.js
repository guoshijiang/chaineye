function GetCodeRister(obj) {
    console.log("aaaa")
  let phone = $("input[name='phone']").val();
  console.log("phone = ", phone)
  if (phone.length !== 11) {
      alert('手机号长度不够');
      return 0;
  }
  let url = window.location.href;
  var index = url.lastIndexOf("\/");
  var url_str = url.substring(0, index + 1);
  let req_url = url_str + 'sms_send?phone=' + phone;
  console.log(req_url)
  $.ajax({
      url: req_url,
      type: "GET",
      dataType: "json",
      success: function (result) {
          if(result.code === 200){
              msg = JSON.parse(result.result)
              if (msg.Code === 'OK') {
                  // 弹窗提示成功
                  $('#alertSuccess').show()
                  setTimeout(function(){
                    $('#alertSuccess').hide()
                  }, 2000)
                  // 倒计时60s后重新发送
                  $('#sendCodeBtn').hide()
                  $('#countTime').show()
                  let count = 60
                  let timer = setInterval(() => {
                    if (count > 0) {
                      count--
                      $('#countTime').text(`${count}s后重新发送`)
                    } else {
                      count = 60
                      clearInterval(timer)
                      $('#sendCodeBtn').show()
                      $('#countTime').hide()
                    }
                  },1000)
              } else {
                $('#alertError').show()
                setTimeout(function(){
                  $('#alertError').hide()
                }, 2000)
              }
          }
      }
  });
}
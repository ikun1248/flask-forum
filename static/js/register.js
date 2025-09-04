function EmailCaptchaClick(){
    $("#captcha-btn").click(function(event){
    event.preventDefault();
    var $this=$(this)
    var email= $("input[name='email']").val();
    $.ajax({
        url:'/auth/captcha/email?email='+email,
        method:'GET',
        success:function(result){
            var code=result['code'];
            $this.off("click")
            if(code==200){
                var countdown=60
                var timer=setInterval(function(){
                    $this.text(countdown+'s')
                    countdown--;
                    if(countdown<=0){
                        $this.text("获取验证码")
                        clearInterval(timer);
                        EmailCaptchaClick();
                    }
                },1000)
                alert("邮箱验证码发送成功")
            }
            else{
                alert(result['message']);
                EmailCaptchaClick();
            }
        },
        fail:function(error){
            console.log(error);
        }
    })
    });
}

$(function(){
    EmailCaptchaClick();
});
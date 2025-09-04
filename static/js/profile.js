document.getElementById("nickname-edit-btn").addEventListener('click',function(){
    document.getElementById("nickname-edit-form").style.visibility='visible'
    document.getElementById("nickname-display").style.display='none';
    this.style.display='none';
})

document.getElementById("nickname-cancel-btn").addEventListener('click',function(){
    document.getElementById("nickname-edit-form").style.visibility='hidden';
    document.getElementById("nickname-display").style.display="inline-block";
    document.getElementById("nickname-edit-btn").style.display='inline'
})

document.getElementById("gender-edit-btn").addEventListener('click',function(){
    document.getElementById("gender-edit-form").style.visibility='visible';
    document.getElementById("gender-display").style.display='none';
    this.style.display='none'
})

document.getElementById("gender-cancel-btn").addEventListener('click',function(){
    document.getElementById("gender-edit-form").style.visibility='hidden';
    document.getElementById("gender-display").style.display='inline-block';
    document.getElementById("gender-edit-btn").style.display='inline'
})

document.getElementById("address-edit-btn").addEventListener('click',function(){
    document.getElementById("address-edit-form").style.visibility='visible';
    document.getElementById("address-display").style.display='none';
    this.style.display='none'
})

document.getElementById("address-cancel-btn").addEventListener('click',function(){
    document.getElementById("address-edit-form").style.visibility='hidden';
    document.getElementById("address-display").style.display='inline-block';
    document.getElementById("address-edit-btn").style.display='inline'
})

let provinceSelectMap={};

fetch("/static/js/provinces.json")
    .then(response =>response.json())
    .then(data=>{
        provinceSelectMap=data;
        populateProvinces();
    })

function populateProvinces(){
    const provinceSelect=document.getElementById("province-select");
    for (const province in provinceSelectMap){
        const option=document.createElement("option");
        option.value=province;
        option.text=province;
        if(province==user.province)
        {
            option.selected=true;
        }

        provinceSelect.appendChild(option);
    }
    populateCities(user.province);
}

function populateCities(SelectedProvince) {
    const citySelect = document.getElementById('city-select');
    citySelect.innerHTML = '<option value="">选择城市</option>';
    provinceSelectMap[SelectedProvince].forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.text = city;
        if (city === user.city) {
            option.selected = true;
        }
        citySelect.appendChild(option);
    });
}

document.getElementById("province-select").addEventListener('change',function(){
    const selectedProvince=this.value;
    const citySelect=document.getElementById("city-select");

    citySelect.innerHTML='<option value="">选择城市</option>'

    if(provinceSelectMap[selectedProvince]){
        provinceSelectMap[selectedProvince].forEach(city=>{
            const option=document.createElement("option");
            option.value=city;
            option.text=city;
            citySelect.appendChild(option);
        });
    }
})

document.getElementById("security-tab").addEventListener('click',function(){
    document.getElementById("security-settings").style.display='block';
    document.getElementById("password-setting").style.display='none';
    document.getElementById("email-setting").style.display='none';
})

document.getElementById("password-edit-btn").addEventListener('click',function(){
    document.getElementById('security-settings').style.display='none';
    document.getElementById('password-setting').style.display='block';
})

document.getElementById("email-edit-btn").addEventListener('click',function(){
    document.getElementById('security-settings').style.display='none';
    document.getElementById('email-setting').style.display='block';
})

function EmailCaptchaClick(){
    $("#captcha-btn").click(function(event){
    event.preventDefault();
    console.log("按钮点击了");
    var $this=$(this)
    var email= $("input[name='new_email']").val();
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
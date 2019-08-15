$("#id_captcha_1").attr("placeholder","验证码");

// 实现动态刷新验证码
$('.captcha').click(function(){
         $.getJSON("/captcha/refresh/",
                  function(result){
             $('.captcha').attr('src', result['image_url']);
             $('#id_captcha_0').val(result['key'])
          });});

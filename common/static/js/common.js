$(function() {
    // $('#loginModal').modal({
    //     show: true
    // })
    $('.register-tab').click(function() {
        $(this).addClass('active')
        $('.login-tab').removeClass('active')
        $('.register-form').show()
        $('.password-login-form').hide()
        $('.code-login-form').hide()
    })
    $('.login-tab').click(function() {
        $(this).addClass('active')
        $('.register-tab').removeClass('active')
        $('.register-form').hide()
        $('.password-login-form').show()
        $('.code-login-form').hide()
    })
    $('.password-type').click(function() {
        $('.password-login-form').show()
        $('.code-login-form').hide()
    })
    $('.code-type').click(function() {
        $('.code-login-form').show()
        $('.password-login-form').hide()
    })
})

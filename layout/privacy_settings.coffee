PrivacySettings =
    createCookie: (name, value, days) ->
        date = new Date()
        if days
            date.setTime(date.getTime() + (days * 24 * 3600 * 1000))
            expires = "; expires=" + date.toGMTString()
        else
            expires = ""
        path = "; path=/"
        document.cookie = name + "=" + value + expires + path
        return

    acceptCookieLaw: ->
        this.createCookie('cookie_law_accepted', '1', 10*365)
        document.getElementById('PrivacyCookieLaw').style.display = 'none';
        return

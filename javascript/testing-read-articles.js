// ==UserScript==
// @name         News
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://localhost:8080/crawled/news/nz/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function fixImages (images, first) {
        for (var j = 0; j < images.length; j++) {
            var image = images.item(j)
            if (image.getAttribute('data-srcset') !== null && image.getAttribute('data-srcset').length > 0) {
                var datasrc = image.getAttribute('data-srcset')
                var parts = datasrc.split(' ')
                if (parts.length > 0) {
                    var holder = first ? parts[0] : parts[parts.length - 2]
                    var tokens = holder.split('/').reverse()
                    var src = []
                    for (var token of tokens) {
                        src.push(token)
                        if (token.indexOf('amazonaws.com') > 0) {
                            src.push('https://')
                            break
                        }
                    }
                    image.setAttribute('src', src.reverse().join('/'))
                }
            }
        }
    }

    // Article?
    var article = document.getElementById('article-content')
    if (article !== null) {
        article.className = ""
        var children = article.getElementsByTagName('div')
        for (var i = 0; i < children.length ; i++) {
            var elem = children.item(i)
            elem.style.display = 'inherit'
            elem.style.opacity = 100
        }
        var articleImages = document.getElementsByClassName('article-main').item(0).getElementsByTagName('img')
        fixImages(articleImages)
    } else {
        // Then try HomePage
        var homepageImages = document.getElementById('main').getElementsByTagName('img')
        fixImages(homepageImages)
    }
})();

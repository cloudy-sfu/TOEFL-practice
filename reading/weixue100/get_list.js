const divElements = document.querySelectorAll('div[id^="ztpo"]');
let articleLinks = [];
divElements.forEach(div => {
    const links = div.querySelectorAll('a[href*="/toefl/read/"]:not([href*="preview"]):not([href*="play"])');
    links.forEach(link => {
        if (!articleLinks.includes(link.getAttribute('href'))) {
            articleLinks.push(link.getAttribute('href'));
        }
    });
});
console.log(articleLinks);
// Bookmark, denote the minified script above is $minified_js_text
// javascript:(function(){$minified_js_text})();
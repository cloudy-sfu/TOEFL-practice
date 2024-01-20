const divElements = document.querySelectorAll('div[id^="ztpo"]');
let articleLinks = [];
divElements.forEach(div => {
    const links = div.querySelectorAll('a[href*="/toefl/listening/"]:not([href*="play"]):not([href*="ready"])');
    links.forEach(link => {
        if (!articleLinks.includes(link.getAttribute('href'))) {
            articleLinks.push(link.getAttribute('href'));
        }
    });
});
console.log(articleLinks);
articleLinks = articleLinks.filter((element, index) => {return index % 2 === 0});
// Bookmark, denote the minified script above is $minified_js_text
// javascript:(function(){ $minified_js_text })();
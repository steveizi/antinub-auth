$(document).ready(function () {
    var pageName = document.getElementById('_pageName');
    if (pageName !== null) { pageName = pageName.innerHTML; }
    else { pageName = ''; }
    if (pageName.length > 0) {
        $("li[data-link-name='" + pageName + "']").addClass('active');
    }
});

$(document).ready(function () {
    var pageName = document.getElementById('_subPageName');
    if (pageName !== null) { pageName = pageName.innerHTML; }
    else { pageName = ''; }
    if (pageName.length > 0) {
        $("a[data-link-name='" + pageName + "']").addClass('active');
    }
});
search_btn = document.getElementById('search-btn');

search_btn.addEventListener("click", function (e) {
    street_name = document.getElementById('street-name').value;
    window.location.href = '/search/streets/' + street_name;
});

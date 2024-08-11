
    function filterArticles(category) {
        var articles, i;
        articles = document.getElementsByClassName("article-item");

        for (i = 0; i < articles.length; i++) {
            if (category === 'all') {
                articles[i].style.display = "block";
            } else if (articles[i].classList.contains(category)) {
                articles[i].style.display = "block";
            } else {
                articles[i].style.display = "none";
            }
        }

        // Update the active tab
        var tabs = document.getElementsByClassName("tab-link");
        for (i = 0; i < tabs.length; i++) {
            tabs[i].classList.remove("active");
        }
        event.currentTarget.classList.add("active");
    }



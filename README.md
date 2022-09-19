# Schedule-Tracker

A simple countdown website to track your schedules at LAHS. Uses Python for backend (Flask for framework) and a tiny bit of JS to loop functions in HTML (I didn't feel like using AJAX). Works by sending JS fetch requests from HTML to a Flask endpoint which returns information regarding schedule.

Inspired from https://bell.plus

Features:
- Fully Python backend
- Themes
- Easily customizeable

Current pages:
- `/`
- `/settings`
- `/metadata`
- `/setcookie` POST
- `/getcookie`
- `/set_theme` POST

To create a new theme, go to `templates/settings.html` and add new option using `<option value = "name" selected = "selected">name</option>`. Then go to `static/` and create a new `.css` file with the same name that you specified when creating the option. Copy over the code from `static/dark.css`. Now just edit the css file to include the colars that you want. 
